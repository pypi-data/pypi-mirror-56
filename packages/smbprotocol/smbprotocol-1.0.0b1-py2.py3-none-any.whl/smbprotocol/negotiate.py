# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Jordan Borean (@jborean93) <jborean93@gmail.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

import hashlib
import struct

from collections import (
    OrderedDict,
)

from cryptography.exceptions import (
    UnsupportedAlgorithm,
)

from cryptography.hazmat.primitives.ciphers import (
    aead,
)

from smbprotocol import (
    Commands,
)

from smbprotocol.structure import (
    BytesField,
    DateTimeField,
    EnumField,
    FlagField,
    IntField,
    ListField,
    Structure,
    StructureField,
    UuidField,
)


class Capabilities(object):
    """
    [MS-SMB2] v53.0 2017-09-15

    2.2.3 SMB2 NEGOTIATE Request Capabilities
    Used in SMB3.x and above, used to specify the capabilities supported.
    """
    SMB2_GLOBAL_CAP_DFS = 0x00000001
    SMB2_GLOBAL_CAP_LEASING = 0x00000002
    SMB2_GLOBAL_CAP_LARGE_MTU = 0x00000004
    SMB2_GLOBAL_CAP_MULTI_CHANNEL = 0x00000008
    SMB2_GLOBAL_CAP_PERSISTENT_HANDLES = 0x00000010
    SMB2_GLOBAL_CAP_DIRECTORY_LEASING = 0x00000020
    SMB2_GLOBAL_CAP_ENCRYPTION = 0x00000040


class Dialects(object):
    """
    [MS-SMB2] v53.0 2017-09-15

    2.2.3 SMB2 NEGOTIATE Request Dialects
    16-bit integeres specifying an SMB2 dialect that is supported. 0x02FF is
    used in the SMBv1 negotiate request to say that dialects greater than
    2.0.2 is supported.
    """
    SMB_2_0_2 = 0x0202
    SMB_2_1_0 = 0x0210
    SMB_3_0_0 = 0x0300
    SMB_3_0_2 = 0x0302
    SMB_3_1_1 = 0x0311
    SMB_2_WILDCARD = 0x02FF


class SecurityMode(object):
    """
    [MS-SMB2] v53.0 2017-09-15

    2.2.3 SMB2 NEGOTIATE Request SecurityMode
    Indicates whether SMB signing is enabled or required by the client.
    """
    SMB2_NEGOTIATE_SIGNING_ENABLED = 0x0001
    SMB2_NEGOTIATE_SIGNING_REQUIRED = 0x0002


class NegotiateContextType(object):
    """
    [MS-SMB2] v53.0 2017-09-15

    2.2.3.1 SMB2 NEGOTIATE_CONTENT Request ContextType
    Specifies the type of context in an SMB2 NEGOTIATE_CONTEXT message.
    """
    SMB2_PREAUTH_INTEGRITY_CAPABILITIES = 0x0001
    SMB2_ENCRYPTION_CAPABILITIES = 0x0002


class HashAlgorithms(object):
    """
    [MS-SMB2] v53.0 2017-09-15

    2.2.3.1.1 SMB2_PREAUTH_INTEGRITY_CAPABILITIES
    16-bit integer IDs that specify the integrity hash algorithm supported
    """
    SHA_512 = 0x0001

    @staticmethod
    def get_algorithm(hash):
        return {
            HashAlgorithms.SHA_512: hashlib.sha512
        }[hash]


class Ciphers(object):
    """
    [MS-SMB2] v53.0 2017-09-15

    2.2.3.1.2 SMB2_ENCRYPTION_CAPABILITIES
    16-bit integer IDs that specify the supported encryption algorithms.
    """
    AES_128_CCM = 0x0001
    AES_128_GCM = 0x0002

    @staticmethod
    def get_cipher(cipher):
        return {
            Ciphers.AES_128_CCM: aead.AESCCM,
            Ciphers.AES_128_GCM: aead.AESGCM
        }[cipher]

    @staticmethod
    def get_supported_ciphers():
        supported_ciphers = []
        try:
            aead.AESGCM(b"\x00" * 16)
            supported_ciphers.append(Ciphers.AES_128_GCM)
        except UnsupportedAlgorithm:  # pragma: no cover
            pass
        try:
            aead.AESCCM(b"\x00" * 16)
            supported_ciphers.append(Ciphers.AES_128_CCM)
        except UnsupportedAlgorithm:  # pragma: no cover
            pass
        return supported_ciphers


class SMB2NegotiateRequest(Structure):
    """
    [MS-SMB2] v53.0 2017-09-15

    2.2.3 SMB2 Negotiate Request
    The SMB2 NEGOTIATE Request packet is used by the client to notify the
    server what dialects of the SMB2 Protocol the client understands. This is
    only used if the client explicitly sets the Dialect to use to a version
    less than 3.1.1. Dialect 3.1.1 added support for negotiate_context and
    SMB3NegotiateRequest should be used to support that.
    """
    COMMAND = Commands.SMB2_NEGOTIATE

    def __init__(self):
        self.fields = OrderedDict([
            ('structure_size', IntField(
                size=2,
                default=36,
            )),
            ('dialect_count', IntField(
                size=2,
                default=lambda s: len(s['dialects'].get_value()),
            )),
            ('security_mode', FlagField(
                size=2,
                flag_type=SecurityMode
            )),
            ('reserved', IntField(size=2)),
            ('capabilities', FlagField(
                size=4,
                flag_type=Capabilities,
            )),
            ('client_guid', UuidField()),
            ('client_start_time', IntField(size=8)),
            ('dialects', ListField(
                size=lambda s: s['dialect_count'].get_value() * 2,
                list_count=lambda s: s['dialect_count'].get_value(),
                list_type=EnumField(size=2, enum_type=Dialects),
            )),
        ])

        super(SMB2NegotiateRequest, self).__init__()


class SMB3NegotiateRequest(Structure):
    """
    [MS-SMB2] v53.0 2017-09-15

    2.2.3 SMB2 Negotiate Request
    Like SMB2NegotiateRequest but with support for setting a list of
    Negotiate Context values. This is used by default and is for Dialects 3.1.1
    or greater.
    """
    COMMAND = Commands.SMB2_NEGOTIATE

    def __init__(self):
        self.fields = OrderedDict([
            ('structure_size', IntField(
                size=2,
                default=36,
            )),
            ('dialect_count', IntField(
                size=2,
                default=lambda s: len(s['dialects'].get_value()),
            )),
            ('security_mode', FlagField(
                size=2,
                flag_type=SecurityMode,
            )),
            ('reserved', IntField(size=2)),
            ('capabilities', FlagField(
                size=4,
                flag_type=Capabilities,
            )),
            ('client_guid', UuidField()),
            ('negotiate_context_offset', IntField(
                size=4,
                default=lambda s: self._negotiate_context_offset_value(s),
            )),
            ('negotiate_context_count', IntField(
                size=2,
                default=lambda s: len(s['negotiate_context_list'].get_value()),
            )),
            ('reserved2', IntField(size=2)),
            ('dialects', ListField(
                size=lambda s: s['dialect_count'].get_value() * 2,
                list_count=lambda s: s['dialect_count'].get_value(),
                list_type=EnumField(size=2, enum_type=Dialects),
            )),
            ('padding', BytesField(
                size=lambda s: self._padding_size(s),
                default=lambda s: b"\x00" * self._padding_size(s),
            )),
            ('negotiate_context_list', ListField(
                list_count=lambda s: s['negotiate_context_count'].get_value(),
                unpack_func=lambda s, d: self._negotiate_context_list(s, d),
            )),
        ])
        super(SMB3NegotiateRequest, self).__init__()

    def _negotiate_context_offset_value(self, structure):
        # The offset from the beginning of the SMB2 header to the first, 8-byte
        # aligned, negotiate context
        header_size = 64
        negotiate_size = structure['structure_size'].get_value()
        dialect_size = len(structure['dialects'])
        padding_size = self._padding_size(structure)
        return header_size + negotiate_size + dialect_size + padding_size

    def _padding_size(self, structure):
        # Padding between the end of the buffer value and the first Negotiate
        # context value so that the first value is 8-byte aligned. Padding is
        # 4 is there are no dialects specified
        mod = (structure['dialect_count'].get_value() * 2) % 8
        return 0 if mod == 0 else mod

    def _negotiate_context_list(self, structure, data):
        context_count = structure['negotiate_context_count'].get_value()
        context_list = []
        for idx in range(0, context_count):
            field, data = self._parse_negotiate_context_entry(data, idx)
            context_list.append(field)

        return context_list

    def _parse_negotiate_context_entry(self, data, idx):
        data_length = struct.unpack("<H", data[2:4])[0]
        negotiate_context = SMB2NegotiateContextRequest()
        negotiate_context.unpack(data[:data_length + 8])
        return negotiate_context, data[8 + data_length:]


class SMB2NegotiateContextRequest(Structure):
    """
    [MS-SMB2] v53.0 2017-09-15

    2.2.3.1 SMB2 NEGOTIATE_CONTEXT Request Values
    The SMB2_NEGOTIATE_CONTEXT structure is used by the SMB2 NEGOTIATE Request
    and the SMB2 NEGOTIATE Response to encode additional properties.
    """
    COMMAND = Commands.SMB2_NEGOTIATE

    def __init__(self):
        self.fields = OrderedDict([
            ('context_type', EnumField(
                size=2,
                enum_type=NegotiateContextType,
            )),
            ('data_length', IntField(
                size=2,
                default=lambda s: len(s['data'].get_value()),
            )),
            ('reserved', IntField(size=4)),
            ('data', StructureField(
                size=lambda s: s['data_length'].get_value(),
                structure_type=lambda s: self._data_structure_type(s)
            )),
            # not actually a field but each list entry must start at the 8 byte
            # alignment
            ('padding', BytesField(
                size=lambda s: self._padding_size(s),
                default=lambda s: b"\x00" * self._padding_size(s),
            ))
        ])
        super(SMB2NegotiateContextRequest, self).__init__()

    def _data_structure_type(self, structure):
        con_type = structure['context_type'].get_value()
        if con_type == \
                NegotiateContextType.SMB2_PREAUTH_INTEGRITY_CAPABILITIES:
            return SMB2PreauthIntegrityCapabilities
        elif con_type == NegotiateContextType.SMB2_ENCRYPTION_CAPABILITIES:
            return SMB2EncryptionCapabilities

    def _padding_size(self, structure):
        data_size = len(structure['data'])
        return 8 - data_size if data_size <= 8 else 8 - (data_size % 8)


class SMB2PreauthIntegrityCapabilities(Structure):
    """
    [MS-SMB2] v53.0 2017-09-15

    2.2.3.1.1 SMB2_PREAUTH_INTEGRITY_CAPABILITIES
    The SMB2_PREAUTH_INTEGRITY_CAPABILITIES context is specified in an SMB2
    NEGOTIATE request by the client to indicate which preauthentication
    integrity hash algorithms it supports and to optionally supply a
    preauthentication integrity hash salt value.
    """

    def __init__(self):
        self.fields = OrderedDict([
            ('hash_algorithm_count', IntField(
                size=2,
                default=lambda s: len(s['hash_algorithms'].get_value()),
            )),
            ('salt_length', IntField(
                size=2,
                default=lambda s: len(s['salt']),
            )),
            ('hash_algorithms', ListField(
                size=lambda s: s['hash_algorithm_count'].get_value() * 2,
                list_count=lambda s: s['hash_algorithm_count'].get_value(),
                list_type=EnumField(size=2, enum_type=HashAlgorithms),
            )),
            ('salt', BytesField(
                size=lambda s: s['salt_length'].get_value(),
            )),
        ])
        super(SMB2PreauthIntegrityCapabilities, self).__init__()


class SMB2EncryptionCapabilities(Structure):
    """
    [MS-SMB2] v53.0 2017-09-15

    2.2.3.1.2 SMB2_ENCRYPTION_CAPABILITIES
    The SMB2_ENCRYPTION_CAPABILITIES context is specified in an SMB2 NEGOTIATE
    request by the client to indicate which encryption algorithms the client
    supports.
    """

    def __init__(self):
        self.fields = OrderedDict([
            ('cipher_count', IntField(
                size=2,
                default=lambda s: len(s['ciphers'].get_value()),
            )),
            ('ciphers', ListField(
                size=lambda s: s['cipher_count'].get_value() * 2,
                list_count=lambda s: s['cipher_count'].get_value(),
                list_type=EnumField(size=2, enum_type=Ciphers),
            )),
        ])
        super(SMB2EncryptionCapabilities, self).__init__()


class SMB2NegotiateResponse(Structure):
    """
    [MS-SMB2] v53.0 2017-09-15

    2.2.4 SMB2 NEGOTIATE Response
    The SMB2 NEGOTIATE Response packet is sent by the server to notify the
    client of the preferred common dialect.
    """
    COMMAND = Commands.SMB2_NEGOTIATE

    def __init__(self):
        self.fields = OrderedDict([
            ('structure_size', IntField(
                size=2,
                default=65,
            )),
            ('security_mode', FlagField(
                size=2,
                flag_type=SecurityMode,
            )),
            ('dialect_revision', EnumField(
                size=2,
                enum_type=Dialects,
            )),
            ('negotiate_context_count', IntField(
                size=2,
                default=lambda s: self._negotiate_context_count_value(s),
            )),
            ('server_guid', UuidField()),
            ('capabilities', FlagField(
                size=4,
                flag_type=Capabilities
            )),
            ('max_transact_size', IntField(size=4)),
            ('max_read_size', IntField(size=4)),
            ('max_write_size', IntField(size=4)),
            ('system_time', DateTimeField()),
            ('server_start_time', DateTimeField()),
            ('security_buffer_offset', IntField(
                size=2,
                default=128,  # (header size 64) + (structure size 64)
            )),
            ('security_buffer_length', IntField(
                size=2,
                default=lambda s: len(s['buffer'].get_value()),
            )),
            ('negotiate_context_offset', IntField(
                size=4,
                default=lambda s: self._negotiate_context_offset_value(s),
            )),
            ('buffer', BytesField(
                size=lambda s: s['security_buffer_length'].get_value(),
            )),
            ('padding', BytesField(
                size=lambda s: self._padding_size(s),
                default=lambda s: b"\x00" * self._padding_size(s),
            )),
            ('negotiate_context_list', ListField(
                list_count=lambda s: s['negotiate_context_count'].get_value(),
                unpack_func=lambda s, d:
                self._negotiate_context_list(s, d),
            )),
        ])
        super(SMB2NegotiateResponse, self).__init__()

    def _negotiate_context_count_value(self, structure):
        # If the dialect_revision is SMBv3.1.1, this field specifies the
        # number of negotiate contexts in negotiate_context_list; otherwise
        # this field must not be used and must be reserved (0).
        if structure['dialect_revision'].get_value() == Dialects.SMB_3_1_1:
            return len(structure['negotiate_context_list'].get_value())
        else:
            return None

    def _negotiate_context_offset_value(self, structure):
        # If the dialect_revision is SMBv3.1.1, this field specifies the offset
        # from the beginning of the SMB2 header to the first 8-byte
        # aligned negotiate context entry in negotiate_context_list; otherwise
        # this field must not be used and must be reserved (0).
        if structure['dialect_revision'].get_value() == Dialects.SMB_3_1_1:
            buffer_offset = structure['security_buffer_offset'].get_value()
            buffer_size = structure['security_buffer_length'].get_value()
            padding_size = self._padding_size(structure)
            return buffer_offset + buffer_size + padding_size
        else:
            return None

    def _padding_size(self, structure):
        # Padding between the end of the buffer value and the first Negotiate
        # context value so that the first value is 8-byte aligned. Padding is
        # not required if there are not negotiate contexts
        if structure['negotiate_context_count'].get_value() == 0:
            return 0

        mod = structure['security_buffer_length'].get_value() % 8
        return 0 if mod == 0 else 8 - mod

    def _negotiate_context_list(self, structure, data):
        context_count = structure['negotiate_context_count'].get_value()
        context_list = []
        for idx in range(0, context_count):
            field, data = self._parse_negotiate_context_entry(data)
            context_list.append(field)

        return context_list

    def _parse_negotiate_context_entry(self, data):
        data_length = struct.unpack("<H", data[2:4])[0]
        negotiate_context = SMB2NegotiateContextRequest()
        negotiate_context.unpack(data[:data_length + 8])
        padded_size = data_length % 8
        if padded_size != 0:
            padded_size = 8 - padded_size

        return negotiate_context, data[8 + data_length + padded_size:]
