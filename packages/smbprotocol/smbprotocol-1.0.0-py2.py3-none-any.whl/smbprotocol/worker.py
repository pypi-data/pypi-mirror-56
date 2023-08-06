# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Jordan Borean (@jborean93) <jborean93@gmail.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from __future__ import division

import atexit
import binascii
import hashlib
import hmac
import logging
import math
import multiprocessing
import os
import struct
import threading
import traceback

from collections import (
    OrderedDict,
)

from cryptography.hazmat.backends import (
    default_backend,
)

from cryptography.hazmat.primitives import (
    cmac,
)

from cryptography.hazmat.primitives.ciphers import (
    aead,
    algorithms,
)

from datetime import (
    datetime,
)

from smbprotocol import (
    MAX_PAYLOAD_SIZE,
    Commands,
)

from smbprotocol._text import (
    to_bytes,
    to_native,
)

from smbprotocol.exceptions import (
    NtStatus,
    SMBException,
)

from smbprotocol.negotiate import (
    Capabilities,
    Ciphers,
    Dialects,
    NegotiateContextType,
    SecurityMode,
    SMB2NegotiateResponse,
)

from smbprotocol.session import (
    SessionFlags,
    SMB2SessionSetupResponse,
)

from smbprotocol.structure import (
    EnumField,
    FlagField,
    BytesField,
    IntField,
    Structure,
)

from smbprotocol.transport import (
    Tcp,
)

from smbprotocol.tree import (
    ShareFlags,
    SMB2TreeConnectResponse,
)

try:
    from queue import Queue
except ImportError:  # pragma: no cover
    from Queue import Queue

log = logging.getLogger(__name__)

_WORKERS = []


class Smb2Flags(object):
    """
    [MS-SMB2] v53.0 2017-09-15

    2.2.1.2 SMB2 Packet Header - SYNC Flags
    Indicates various processing rules that need to be done on the SMB2 packet.
    """
    SMB2_FLAGS_SERVER_TO_REDIR = 0x00000001
    SMB2_FLAGS_ASYNC_COMMAND = 0x00000002
    SMB2_FLAGS_RELATED_OPERATIONS = 0x00000004
    SMB2_FLAGS_SIGNED = 0x00000008
    SMB2_FLAGS_PRIORITY_MASK = 0x00000070
    SMB2_FLAGS_DFS_OPERATIONS = 0x10000000
    SMB2_FLAGS_REPLAY_OPERATIONS = 0x20000000


class SMB2HeaderAsync(Structure):
    """
    [MS-SMB2] 2.2.1.1 SMB2 Packer Header - ASYNC
    https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-smb2/ea4560b7-90da-4803-82b5-344754b92a79

    The SMB2 Packet header for async commands.
    """

    def __init__(self):
        self.fields = OrderedDict([
            ('protocol_id', BytesField(
                size=4,
                default=b"\xfeSMB",
            )),
            ('structure_size', IntField(
                size=2,
                default=64,
            )),
            ('credit_charge', IntField(size=2)),
            ('channel_sequence', IntField(size=2)),
            ('reserved', IntField(size=2)),
            ('command', EnumField(
                size=2,
                enum_type=Commands,
            )),
            ('credit_request', IntField(size=2)),
            ('flags', FlagField(
                size=4,
                flag_type=Smb2Flags,
            )),
            ('next_command', IntField(size=4)),
            ('message_id', IntField(size=8)),
            ('async_id', IntField(size=8)),
            ('session_id', IntField(size=8)),
            ('signature', BytesField(
                size=16,
                default=b"\x00" * 16,
            )),
            ('data', BytesField())
        ])
        super(SMB2HeaderAsync, self).__init__()


class SMB2HeaderRequest(Structure):
    """
    [MS-SMB2] v53.0 2017-09-15

    2.2.1.2 SMB2 Packet Header - SYNC
    This is the header definition that contains the ChannelSequence/Reserved
    instead of the Status field used for a Packet request.
    """

    def __init__(self):
        self.fields = OrderedDict([
            ('protocol_id', BytesField(
                size=4,
                default=b"\xfeSMB",
            )),
            ('structure_size', IntField(
                size=2,
                default=64,
            )),
            ('credit_charge', IntField(size=2)),
            ('channel_sequence', IntField(size=2)),
            ('reserved', IntField(size=2)),
            ('command', EnumField(
                size=2,
                enum_type=Commands
            )),
            ('credit_request', IntField(size=2)),
            ('flags', FlagField(
                size=4,
                flag_type=Smb2Flags,
            )),
            ('next_command', IntField(size=4)),
            ('message_id', IntField(size=8)),
            ('process_id', IntField(size=4)),
            ('tree_id', IntField(size=4)),
            ('session_id', IntField(size=8)),
            ('signature', BytesField(
                size=16,
                default=b"\x00" * 16,
            )),
            ('data', BytesField())
        ])
        super(SMB2HeaderRequest, self).__init__()


class SMB2HeaderResponse(Structure):
    """
    [MS-SMB2] v53.0 2017-09-15

    2.2.1.2 SMB2 Packet Header - SYNC
    The header definition for an SMB Response that contains the Status field
    instead of the ChannelSequence/Reserved used for a Packet response.
    """

    def __init__(self):
        self.fields = OrderedDict([
            ('protocol_id', BytesField(
                size=4,
                default=b'\xfeSMB',
            )),
            ('structure_size', IntField(
                size=2,
                default=64,
            )),
            ('credit_charge', IntField(size=2)),
            ('status', EnumField(
                size=4,
                enum_type=NtStatus,
                enum_strict=False
            )),
            ('command', EnumField(
                size=2,
                enum_type=Commands
            )),
            ('credit_response', IntField(size=2)),
            ('flags', FlagField(
                size=4,
                flag_type=Smb2Flags,
            )),
            ('next_command', IntField(size=4)),
            ('message_id', IntField(size=8)),
            ('reserved', IntField(size=4)),
            ('tree_id', IntField(size=4)),
            ('session_id', IntField(size=8)),
            ('signature', BytesField(
                size=16,
                default=b"\x00" * 16,
            )),
            ('data', BytesField()),
        ])
        super(SMB2HeaderResponse, self).__init__()


class SMB2CancelRequest(Structure):
    """
    [MS-SMB2] 2.2.30 - SMB2 CANCEL Request
    https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-smb2/91913fc6-4ec9-4a83-961b-370070067e63

    The SMB2 CANCEL Request packet is sent by the client to cancel a previously sent message on the same SMB2 transport
    connection.
    """
    COMMAND = Commands.SMB2_CANCEL

    def __init__(self):
        self.fields = OrderedDict([
            ('structure_size', IntField(
                size=2,
                default=4,
            )),
            ('reserved', IntField(size=2)),
        ])
        super(SMB2CancelRequest, self).__init__()


class SMB2TransformHeader(Structure):
    """
    [MS-SMB2] v53.0 2017-09-15

    2.2.41 SMB2 TRANSFORM_HEADER
    The SMB2 Transform Header is used by the client or server when sending
    encrypted message. This is only valid for the SMB.x dialect family.
    """

    def __init__(self):
        self.fields = OrderedDict([
            ('protocol_id', BytesField(
                size=4,
                default=b"\xfdSMB"
            )),
            ('signature', BytesField(
                size=16,
                default=b"\x00" * 16
            )),
            ('nonce', BytesField(size=16)),
            ('original_message_size', IntField(size=4)),
            ('reserved', IntField(size=2, default=0)),
            ('flags', IntField(
                size=2,
                default=1
            )),
            ('session_id', IntField(size=8)),
            ('data', BytesField())  # not in spec
        ])
        super(SMB2TransformHeader, self).__init__()


class SessionKeys(object):

    def __init__(self, session_id, signing_key, encryption_key, decryption_key, force_encryption):
        """
        Used to communicate the session key from authentication which is then used by the worker process to create the
        signing and encryption keys for later messages.

        :param session_id: The session the keys relate to.
        :param signing_key: The key used to sign requests.
        :param encryption_key: The key used to encrypt requests.
        :param decryption_key: The key used to decrypt requests.
        :param force_encryption: Whether to force encryption on the share even if it allows plaintext messages.
        """
        self.session_id = session_id
        self.signing_key = signing_key
        self.encryption_key = encryption_key
        self.decryption_key = decryption_key
        self.force_encryption = force_encryption


class MessageWorker(multiprocessing.Process):

    def __init__(self, server, port=445, timeout=None, require_signing=True):
        """
        A MessageWorker process that is run for each connection that is set up. It is designed to offload message
        receiving and raw processing on to a separate process to avoid GIL issues with parallel work. When started it
        will start up the following.

        Main Process:
            Response recv thread: Reads the headers processed in the worker and fires the events on the Request
                objects.

        Worker Process:
            Socket recv thread: Reads the raw bytes on the socket and adds the messages to an internal queue.
            Header byte thread: Reads the internal queue from above and processes the messages to a Header obj.

        Calling .close() will close all of the above and end the connection to the server.

        :param server: The server to connect to.
        :param port: The port for the SMB listener on the server.
        :param timeout: The initial connection timeout.
        :param require_signing: Whether to force signing of messages even if the server does not require it.
        """
        global _WORKERS
        _WORKERS.append(self)

        self.server = server
        self.port = port
        self.timeout = timeout

        # Used on both main and worker process to manage the connection state.
        self.dialect = 0
        self.cipher = None
        self.sign = require_signing
        self.supports_multi_credit = False
        self.sessions = {}

        # The below are used only on the main process, no synchronisation to the worker process.
        self.t_exc = None
        self.outstanding_lock = threading.Lock()
        self.outstanding_requests = {}

        self._sequence_lock = threading.Lock()
        self._sequence_window = {
            'low': 0,
            'high': 1,
        }

        self._t_recv_main = threading.Thread(target=self._process_recv_header_thread,
                                            name="main-recv-header-%s:%s" % (self.server, self.port))
        self._t_recv_main.daemon = True

        # Internal queues used for IPC with the worker process.
        self._input_queue = multiprocessing.Queue()  # Queue to place raw message bytes to send to the worker process.
        self._output_queue = multiprocessing.Queue()  # Queue to place SMB2 header responses from worker process.

        super(MessageWorker, self).__init__()

    def start(self):
        self._t_recv_main.start()
        return super(MessageWorker, self).start()

    def run(self):
        # Dedicated thread to manage the raw socket input bytes and transform them into SMB2 headers.
        recv_queue = Queue()
        t_recv = threading.Thread(target=self._process_raw_recv_thread, args=(recv_queue,),
                                  name="worker-recv-msg-%s:%s" % (self.server, self.port))
        t_recv.daemon = True
        transport = Tcp(self.server, self.port, recv_queue, self.timeout)

        try:
            t_recv.start()

            while True:
                data = self._input_queue.get()

                if data is None:
                    return
                elif isinstance(data, SessionKeys):
                    self._post_process_session_keys(data)
                else:
                    transport.send(data)
        except Exception as e:
            # Place exception message to main process worker which sets self.t_exc.
            self._output_queue.put(("Worker input process", e, traceback.format_exc()))
        finally:
            # Close down the message processing thread.
            recv_queue.put(None)
            t_recv.join()

            # Close down the transport socket
            transport.close()

    def close(self):
        """
        Shutdown the worker process and close all connections and threads associated with it. Should only be called
        from the main process thread.
        """
        self._output_queue.put(None)  # Closes _process_recv_header_thread on the main process.
        self._t_recv_main.join()

        self._input_queue.put(None)  # Closes run() process and it's child threads.
        #if not self.join(timeout=5):
        #    self.terminate()
        #    raise Exception("terminated")

    def send(self, messages, session_id=None, tree_id=None, message_id=None, credit_request=None, related=False,
             async_id=None):
        """
        Send 1 or more messages to the server within 1 TCP request. Will fail if the size of the total length exceeds
        maximum allowed length of the transport. Should only be caled from the main process thread.

        :param messages: A list of messages to send to server.
        :param session_id: The Session Id associated with the message(s).
        :param tree_id: The Tree Id associated with the message(s).
        :param message_id: Override the Message Id set on the header, only used for cancel requests.
        :param credit_request: Specifies extra credits to be requests with the SMB header.
        :param related: Whether each message is related to each other, sets the Session, Tree, and File Id to the same
            value as the first message.
        :param async_id: The Async Id for the header, only used for cancel requests.
        :return: List<Request> for each message that was sent to the server.
        """
        # TODO: verify that the socket is still up and running.

        send_data = b""
        requests = []
        session = self.sessions.get(session_id, {})
        tree = session['trees'].get(tree_id, {}) if session else {}

        total_requests = len(messages)
        for i, message in enumerate(messages):
            if i == total_requests - 1:
                next_command = 0
                padding = b""
            else:
                # each compound message must start at the 8-byte boundary
                msg_length = 64 + len(message)
                mod = msg_length % 8
                padding_length = 8 - mod if mod > 0 else 0
                next_command = msg_length + padding_length
                padding = b"\x00" * padding_length

            with self._sequence_lock:
                sequence_window_low = self._sequence_window['low']
                sequence_window_high = self._sequence_window['high']
                credit_charge = self._calculate_credit_charge(message)
                credits_available = sequence_window_high - sequence_window_low
                if credit_charge > credits_available:
                    raise SMBException("Request requires %d credits but only %d credits are available"
                                       % (credit_charge, credits_available))

                current_id = message_id or sequence_window_low
                if message.COMMAND != Commands.SMB2_CANCEL:
                    self._sequence_window['low'] += credit_charge if credit_charge > 0 else 1

            if async_id is None:
                header = SMB2HeaderRequest()
                header['tree_id'] = tree_id if tree_id else 0
            else:
                header = SMB2HeaderAsync()
                header['flags'].set_flag(Smb2Flags.SMB2_FLAGS_ASYNC_COMMAND)
                header['async_id'] = async_id

            header['credit_charge'] = credit_charge
            header['command'] = message.COMMAND
            header['credit_request'] = credit_request if credit_request else credit_charge
            header['message_id'] = current_id
            header['session_id'] = session_id if session_id else 0
            header['data'] = message.pack()

            header['next_command'] = next_command
            if i != 0 and related:
                header['session_id'] = b"\xff" * 8
                header['tree_id'] = b"\xff" * 4
                header['flags'].set_flag(Smb2Flags.SMB2_FLAGS_RELATED_OPERATIONS)

            if session.get('sign', False) and session.get('signing_key', None):
                # Sign the header
                header['flags'].set_flag(Smb2Flags.SMB2_FLAGS_SIGNED)
                b_header = header.pack() + padding
                signature = self._generate_signature(b_header, session['signing_key'])

                # To save on unpacking and re-packing, manually adjust the signature and update the request object for
                # back-referencing.
                b_header = b_header[:48] + signature + b_header[64:]
                header['signature'] = signature
            else:
                b_header = header.pack() + padding

            send_data += b_header

            request = Request(header, type(message), self, session_id=session_id)
            if message.COMMAND != Commands.SMB2_CANCEL:
                requests.append(request)

                with self.outstanding_lock:
                    self.outstanding_requests[header['message_id'].get_value()] = request

        if related:
            requests[0].related_ids = [r.message['message_id'].get_value() for r in requests][1:]

        if session.get('encrypt', False) or tree.get('encrypt', False):
            # encrypt the data
            send_data = self._encrypt(send_data, session_id, session['encryption_key'])

        # TODO: Check the size and fail if it exceeds the transport limit.

        # Send it to the worker process which then sends it over the socket
        self._input_queue.put(send_data)

        # TODO: Find a way to validate the request was sent before returning.

        return requests

    def update_session_keys(self, session_id, signing_key, encryption_key, decryption_key, force_encryption):
        """
        Synchronise the main process and worker process keys associated with a session to enable signing and encryption
        of messages. Should only be called from the main process thread.

        :param session_id: The session id the keys relate to.
        :param signing_key: The key used for signing a message.
        :param encryption_key: The key used for encrypting a message.
        :param decryption_key: The key use for decrypting a message.
        :param force_encryption: Whether to force encryption for the session even if it allows plaintext messages.
        """
        session_keys = SessionKeys(session_id, signing_key, encryption_key, decryption_key, force_encryption)
        self._post_process_session_keys(session_keys)
        self._input_queue.put(session_keys)

    def _process_raw_recv_thread(self, socket_queue):
        """
        Runs as a separate thread in the MessageWorker process. Reads the input bytes sent by the socket, decrypts and
        parses the bytes into an SMB2HeaderResponse before adding the response back to an IPC queue for the main
        process to read. This is done in a separate process due to GIL locking that creates a deadlock if run in a
        different thread on the main process.

        These headers are then placed in an IPC queue (self._output_queue) which the main process will pick up in it's
        own thread (_process_recv_header_thread) and update the request objects accordingly.

        :param socket_queue: The Queue that is used to contain the raw bytes received by the socket.
        """
        try:
            while True:
                b_data = socket_queue.get()

                # The process will put None in the queue if it is time to end.
                if b_data is None:
                    return

                is_encrypted = b_data[:4] == b"\xfdSMB"
                if is_encrypted:
                    b_data = self._decrypt(b_data)

                next_command = -1
                session_id = None
                while next_command != 0:
                    next_command = struct.unpack("<L", b_data[20:24])[0]
                    header_length = next_command if next_command != 0 else len(b_data)
                    b_header = b_data[:header_length]
                    b_data = b_data[header_length:]

                    header = SMB2HeaderResponse()
                    header.unpack(b_header)
                    if not header['flags'].has_flag(Smb2Flags.SMB2_FLAGS_RELATED_OPERATIONS):
                        session_id = header['session_id'].get_value()

                    # TODO: Verify why this is failing now
                    if not is_encrypted:
                        self._verify_signature(header, session_id)

                    # Keeps the class attributes synchronized between the main and worker process.
                    self._post_process_response(header)
                    self._output_queue.put(b_header)
        except Exception as e:
            self._output_queue.put(("Worker output process", e, traceback.format_exc()))

            # Make sure the main worker process thread is finished.
            self._input_queue.put(None)

    def _process_recv_header_thread(self):
        """
        Run as a thread in the main process to process the raw SMB2 Header responses parsed by the worker process. Care
        has been made to make this do as little work as possible to avoid GIL deadlocks on the main process. Ultimately
        it is only doing work against shared structures like outstanding requests, sequence window, request event
        firing which we cannot synchronise easily in the worker thread.
        """
        while True:
            header = self._output_queue.get()

            if header is None:
                return

            if isinstance(header, tuple):
                self.t_exc = to_native("%s failed with %s\n\nOriginal %s" % header)
                self._input_queue.put(None)  # Stop the worker process
                return

            message_id = struct.unpack("<Q", header[24:32])[0]
            with self.outstanding_lock:
                request = self.outstanding_requests[message_id]

            credit_response = struct.unpack("<H", header[14:16])[0]
            with self._sequence_lock:
                self._sequence_window['high'] += credit_response if credit_response > 0 else 1

            flags = struct.unpack("<I", header[16:20])[0]
            with request.response_lock:
                if flags & Smb2Flags.SMB2_FLAGS_ASYNC_COMMAND == Smb2Flags.SMB2_FLAGS_ASYNC_COMMAND:
                    # Async response header has the Async Id in the same fields as reserved and tree_id.
                    request.async_id = header[32:40]

                request.response = header
                request.response_event.set()

    def _post_process_response(self, header):
        if header['status'].get_value() == NtStatus.STATUS_SUCCESS:
            post_process_map = {
                Commands.SMB2_NEGOTIATE: self._post_process_negotiate,
                Commands.SMB2_SESSION_SETUP: self._post_process_session_setup,
                Commands.SMB2_LOGOFF: self._post_process_logoff,
                Commands.SMB2_TREE_CONNECT: self._post_process_tree_connect,
                Commands.SMB2_TREE_DISCONNECT: self._post_process_tree_disconnect,
            }
            post_process = post_process_map.get(header['command'].get_value(), None)
            if post_process:
                post_process(header)

    def _post_process_negotiate(self, header):
        response = SMB2NegotiateResponse()
        response.unpack(header['data'].get_value())

        # Force the connection to sign all requests if the server demands it, otherwise fallback to the user input
        # setting. A session may still not sign requests if encryption is enabled as that covers the signing.
        if not self.sign and response['security_mode'].has_flag(SecurityMode.SMB2_NEGOTIATE_SIGNING_REQUIRED):
            self.sign = True

        self.dialect = response['dialect_revision'].get_value()
        if self.dialect >= Dialects.SMB_2_1_0:
            self.supports_multi_credit = response['capabilities'].has_flag(Capabilities.SMB2_GLOBAL_CAP_LARGE_MTU)

        if self.dialect >= Dialects.SMB_3_1_1:
            for context in response['negotiate_context_list']:
                if context['context_type'].get_value() == NegotiateContextType.SMB2_ENCRYPTION_CAPABILITIES:
                    self.cipher = Ciphers.get_cipher(context['data']['ciphers'][0])
        else:
            self.cipher = Ciphers.get_cipher(Ciphers.AES_128_CCM)

    def _post_process_session_setup(self, header):
        response = SMB2SessionSetupResponse()
        response.unpack(header['data'].get_value())

        encrypt = response['session_flags'].has_flag(SessionFlags.SMB2_SESSION_FLAG_ENCRYPT_DATA)
        sign = False if encrypt else self.sign  # If encryption is used don't sign data for this session.
        session_info = {
            # These keys are explicitly sent by the Session class after it has computed them from the auth key.
            'decryption_key': None,
            'encryption_key': None,
            'signing_key': None,
            'encrypt': encrypt,
            'sign': sign,
            'trees': {},
        }
        self.sessions[header['session_id'].get_value()] = session_info

    def _post_process_session_keys(self, keys):
        self.sessions[keys.session_id]['signing_key'] = keys.signing_key
        self.sessions[keys.session_id]['encryption_key'] = keys.encryption_key
        self.sessions[keys.session_id]['decryption_key'] = keys.decryption_key
        if keys.force_encryption:
            self.sessions[keys.session_id]['encrypt'] = True
            self.sessions[keys.session_id]['sign'] = False

    def _post_process_logoff(self, header):
        del self.sessions[header['session_id'].get_value()]

    def _post_process_tree_connect(self, header):
        response = SMB2TreeConnectResponse()
        response.unpack(header['data'].get_value())
        self.sessions[header['session_id'].get_value()]['trees'][header['tree_id'].get_value()] = {
            'encrypt': response['share_flags'].has_flag(ShareFlags.SMB2_SHAREFLAG_ENCRYPT_DATA),
        }

    def _post_process_tree_disconnect(self, header):
        del self.sessions[header['session_id'].get_value()]['trees'][header['tree_id'].get_value()]

    def _calculate_credit_charge(self, message):
        """
        Calculates the credit charge for a request based on the command. If connection.supports_multi_credit is not
        True then the credit charge isn't valid so it returns 0.

        The credit charge is the number of credits that are required for sending/receiving data over 64 kilobytes, in
        the existing messages only the Read, Write, Query Directory or IOCTL commands will end in this scenario and
        each require their own calculation to get the proper value. The generic formula for calculating the credit
        charge is

        https://msdn.microsoft.com/en-us/library/dn529312.aspx
        (max(SendPayloadSize, Expected ResponsePayloadSize) - 1) / 65536 + 1

        :param message: The message being sent
        :return: The credit charge to set on the header
        """
        credit_size = MAX_PAYLOAD_SIZE

        if (not self.supports_multi_credit) or (message.COMMAND == Commands.SMB2_CANCEL):
            credit_charge = 0
        elif message.COMMAND == Commands.SMB2_READ:
            max_size = message['length'].get_value() + message['read_channel_info_length'].get_value() - 1
            credit_charge = math.ceil(max_size / credit_size)
        elif message.COMMAND == Commands.SMB2_WRITE:
            max_size = message['length'].get_value() + message['write_channel_info_length'].get_value() - 1
            credit_charge = math.ceil(max_size / credit_size)
        elif message.COMMAND == Commands.SMB2_IOCTL:
            max_in_size = len(message['buffer'])
            max_out_size = message['max_output_response'].get_value()
            max_size = max(max_in_size, max_out_size) - 1
            credit_charge = math.ceil(max_size / credit_size)
        elif message.COMMAND == Commands.SMB2_QUERY_DIRECTORY:
            max_in_size = len(message['buffer'])
            max_out_size = message['output_buffer_length'].get_value()
            max_size = max(max_in_size, max_out_size) - 1
            credit_charge = math.ceil(max_size / credit_size)
        else:
            credit_charge = 1

        # python 2 returns a float where we need an integer
        return int(credit_charge)

    def _encrypt(self, b_data, session_id, encryption_key):
        header = SMB2TransformHeader()
        header['original_message_size'] = len(b_data)
        header['session_id'] = session_id

        if self.cipher == aead.AESGCM:
            nonce = os.urandom(12)
            header['nonce'] = nonce + (b"\x00" * 4)
        else:
            nonce = os.urandom(11)
            header['nonce'] = nonce + (b"\x00" * 5)

        cipher_text = self.cipher(encryption_key).encrypt(nonce, b_data, header.pack()[20:])
        signature = cipher_text[-16:]
        enc_message = cipher_text[:-16]

        header['signature'] = signature
        header['data'] = enc_message

        return header.pack()

    def _decrypt(self, b_data):
        header = SMB2TransformHeader()
        header.unpack(b_data)

        if header['flags'].get_value() != 0x0001:
            raise SMBException("Expecting flag of 0x0001 but got %s in the SMB Transform Header Response"
                               % format(header['flags'].get_value(), 'x'))

        session_id = header['session_id'].get_value()
        session = self.sessions.get(session_id, None)
        if session is None:
            raise SMBException("Failed to find valid session %s for message decryption" % session_id)

        nonce_length = 12 if self.cipher == aead.AESGCM else 11
        nonce = header['nonce'].get_value()[:nonce_length]

        signature = header['signature'].get_value()
        enc_message = header['data'].get_value() + signature

        c = self.cipher(session['decryption_key'])
        return c.decrypt(nonce, enc_message, b_data[20:52])

    def _generate_signature(self, b_header, signing_key):
        b_header = b_header[:48] + (b"\x00" * 16) + b_header[64:]

        if self.dialect >= Dialects.SMB_3_0_0:
            c = cmac.CMAC(algorithms.AES(signing_key), backend=default_backend())
            c.update(b_header)
            signature = c.finalize()
        else:
            hmac_algo = hmac.new(signing_key, msg=b_header, digestmod=hashlib.sha256)
            signature = hmac_algo.digest()[:16]

        return signature

    def _verify_signature(self, header, session_id, verify_session=False):
        message_id = header['message_id'].get_value()
        flags = header['flags']
        status = header['status'].get_value()
        command = header['command'].get_value()

        if message_id == 0xFFFFFFFFFFFFFFFF or not flags.has_flag(Smb2Flags.SMB2_FLAGS_SIGNED) or \
                status == NtStatus.STATUS_PENDING or (command == Commands.SMB2_SESSION_SETUP and not verify_session):
            return

        session = self.sessions.get(session_id, None)
        if session is None:
            raise SMBException("Failed to find session %s for message verification" % session_id)

        expected = self._generate_signature(header.pack(), session['signing_key'])
        actual = header['signature'].get_value()
        if actual != expected:
            raise SMBException("Server message signature could not be verified: %s != %s"
                               % (to_native(binascii.hexlify(actual)), to_native(binascii.hexlify(expected))))


class Request(object):

    def __init__(self, message, message_type, worker, session_id=None):
        """
        [MS-SMB2] v53.0 2017-09-15

        3.2.1.7 Per Pending Request
        For each request that was sent to the server and is await a response
        :param message: The message to be sent in the request
        :param message_type: The type of message that is set in the header's data field.
        :param worker: The WorkerProcess the request was sent under.
        :param session_id: The Session Id the request was for.
        """
        self.cancel_id = os.urandom(8)
        self.async_id = None
        self.message = message
        self.timestamp = datetime.now()

        # The following are not in the SMB spec but used by various functions in smbprotocol
        # Used to contain the corresponding response from the server as the
        # receiving in done in a separate thread
        self._response = None
        self._response_build_lock = threading.Lock()

        self.response_lock = threading.Lock()
        self.response_event = threading.Event()
        self.cancelled = False

        # Stores the message_ids of related messages that are sent in a compound request. This is only set on the 1st
        # message in the request.
        self.related_ids = []

        self._worker = worker
        self._message_type = message_type  # Used to rehydrate the message data in case it's needed again.

        # Cannot rely on the message values as it could be a related compound msg which does not set these values.
        self._session_id = session_id

    @property
    def response(self):
        if self._response is None:
            return None

        # Due to GIL funness we can't unpack the header in the thread that receives the messages so instead we rely on
        # the first caller to unpack it.
        with self._response_build_lock:
            if not isinstance(self._response, SMB2HeaderResponse):
                header = SMB2HeaderResponse()
                header.unpack(self._response)
                self._response = header

        return self._response

    @response.setter
    def response(self, value):
        self._response = value

    def cancel(self):
        if self.cancelled is True:
            return

        message_id = self.message['message_id'].get_value()
        log.info("Cancelling message %s" % message_id)
        self._worker.send([SMB2CancelRequest()], session_id=self._session_id, message_id=message_id, credit_request=0,
                          async_id=self.async_id)
        self.cancelled = True

    def get_message_data(self):
        message_obj = self._message_type()
        message_obj.unpack(self.message['data'].get_value())
        return message_obj

    def update_request(self, new_request):
        self.cancel_id = new_request.cancel_id
        self.async_id = new_request.async_id
        self.message = new_request.message
        self.timestamp = new_request.timestamp
        self.response = None
        self.response_lock = new_request.response_lock
        self.response_event = new_request.response_event
        self.cancelled = new_request.cancelled
        self.related_ids = new_request.related_ids


# Ensure we close each worker on exit.
def _close_workers():
    global _WORKERS
    for worker in _WORKERS:
        worker.close()

atexit.register(_close_workers)
