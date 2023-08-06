import os
import abc
import struct
import logging
import time

from collections import OrderedDict, namedtuple
from datetime import datetime
from typing import List, Dict, Optional, Any, Type, TypeVar

from .audit_event import AUDIT_EVENT, get_audit_events
from .bsm_h import *
from .bsm_errors import BSM_ERRORS
from .audit_record import *
from .argtypes import *

logger = logging.getLogger(__name__)

#https://github.com/openbsm/openbsm/blob/master/libbsm/bsm_io.c

AUDIT_HEADER_SIZE = 18
AUDIT_TRAILER_SIZE = 7

Token = TypeVar("Token", bound="BaseToken")
Rec = TypeVar("Record", bound="Record")


class NotImplementedToken(Exception):
    pass


class UnknownHeader(Exception):
    pass


def unpack_one(fmt, data):
    one = struct.unpack(fmt, data)[0]
    logger.debug(f"data: {data}, unpacked: {one}")
    return one


class TokenFetcher(abc.ABCMeta):
    __tokens__ = {}

    def __new__(metaclass, name, base, namespace):
        cls = abc.ABCMeta.__new__(metaclass, name, base, namespace)
        if getattr(cls, "token_id", None):
            cls.token_name = f"AUT_{name.upper()}"
            logger.debug(cls.token_id, cls.token_name)
            metaclass.__tokens__[cls.token_id] = cls
        return cls

    @classmethod
    def get_token(cls, token_id: int, record: Rec) -> Token:
        obj = cls.__tokens__.get(token_id, None)
        if obj is None:
            raise NotImplementedError(f"{token_id}(0x{token_id:x})")
        token = obj()
        token.fetch(record)
        return token


class BaseToken(metaclass=TokenFetcher):
    __delm__ = ","

    def __init__(self):
        self.args = []

        self._setup()

    def __repr__(self):
        return f"{self.token_name}"

    # @abc.abstractproperty
    @abc.abstractmethod
    __fields__ = (
        raise NotImplemented

    def add_argument(self, name, argtype, **kwargs):
        """
        """
        self.args.append((name, argtype, kwargs))

    def get_length(self):
        return sum([struct.calcsize(self.args[key][0]) for key in self.args])

    def __str__(self):
        return f"{self.token_id}{self.__delm__}".join(
            [f"{getattr(self, arg[0])}" for arg in self.args]
        )

    def fetch(self, record: Rec) -> None:
        for name, argtype, kwargs in self.args:
            try:
                value = argtype(record)
                logger.debug(f"key: {name}, argtype: {argtype}")
            except NotImplementedError as e:
                logger.error(f"{e}: {name}, {argtype}")
                raise(e)
            logger.debug(f"r_value: {value._raw}, type: {type(value)}, value: {value}")
            #setattr(self, f"_{name}", r_value)
            setattr(self, name, value)

    def print_tok_type(self, tok_type, tokname, oflags):
        if oflags & AU_OFLAG_RAW:
            print(f"{tok_type}", end=self.__delm__)
        else:
            print(f"{tokname}", end=self.__delm__)
  
    def print(self, oflags: int):
        if oflags & AU_OFLAG_RAW:
            print(f"{self.token_id}", end=self.__delm__)
        else:
            print(f"{self.identifier}", end=self.__delm__)
        self._print(oflags)
    
    def asdict(self):
        return { name: f"{getattr(self, name)}" for name, _, _, kw in self.args if kw.get("show", True) }

    def _print(self, oflags: int):
        if oflags & AU_OFLAG_XML:
            for name, _, _, kw in self.args:
                if kw.get("show", True):
                    print(f"{name}={getattr(self, name)}")
        elif oflags & AU_OFLAG_RAW:
            print(
                f"{self.__delm__}".join(
                    [
                        f"{getattr(self, name)}"
                        for name, _, kw in self.args
                        if kw.get("show", True)
                    ]
                )
            )
        else:
            print(
                f"{self.__delm__}".join(
                    [
                        f"{getattr(self, name)}"
                        for name, _, kw in self.args
                        if kw.get("show", True)
                    ]
                )
            )


class Header(Struct):
    identifier = "header"
    __fields__ = (
        UInt32("size"),
        UInt8("version"),
        EventType("event_type"),
        UInt16("modifier"),
    )

class Header32(Struct):
    """
        record byte count       4 bytes
        version #               1 byte    [2]
        event type              2 bytes
        event modifier          2 bytes
        seconds of time         4 bytes/8 bytes (32-bit/64-bit value)
        milliseconds of time    4 bytes/8 bytes (32-bit/64-bit value)
    Example:
        record = Record()
        record.generate(AUT_HEADER32)
    """

    token_id = AUT_HEADER32
    __fields__ = (
        Header(),
        DateTime("time"),
        MSec("msec")
    )

class Header32_Ex(Struct):
    """
    * The Solaris specifications for AUE_HEADER32_EX seem to differ a bit
    * depending on the bit of the specifications found.  The OpenSolaris source
    * code uses a 4-byte address length, followed by some number of bytes of
    * address data.  This contrasts with the Solaris audit.log.5 man page, which
    * specifies a 1-byte length field.  We use the Solaris 10 definition so that
    * we can parse audit trails from that system.
    *
    * record byte count       4 bytes
    * version #               1 byte     [2]
    * event type              2 bytes
    * event modifier          2 bytes
    * address type/length     4 bytes
    *   [ Solaris man page: address type/length     1 byte]
    * machine address         4 bytes/16 bytes (IPv4/IPv6 address)
    * seconds of time         4 bytes/8 bytes  (32/64-bits)
    * nanoseconds of time     4 bytes/8 bytes  (32/64-bits)
    """

    token_id = AUT_HEADER32_EX
    __fields__ = (
        Header(),
        IPAddress("address"),
        DateTime("time"),
        MSec("msec")
    )

class Trailer(Struct):
    """
    trailer magic 2 bytes show=False
    record size   4 bytes
    """

    token_id = AUT_TRAILER
    identifier = "trailer"

    __fields__  = (
        UInt16("magic"),
        UInt32("count"),
    )

class Argument(Struct):
    """
    * argument #              1 byte
    * argument value          4 bytes/8 bytes (32-bit/64-bit value)
    * text length             2 bytes
    * text                    N bytes + 1 terminating NULL byte
    """

    token_id = AUT_ARG
    identifier = "argument"

    __fields__  = (
        UInt8("no"),
        UInt32("val"),# Hex
        String("text"),
    )

class Arg32(Argument):
    token_id = AUT_ARG32


class Arg64(Argument):
    """
       "no": ">b",
        "val": ">Q",
        "text_size": ">H",
        "text": ">{text_size}s",
    """

    token_id = AUT_ARG64
    identifier = "argument"
    
    __fields__  = (
        UInt8("no"),
        UInt64("val"),# Hex
        String("text"),
    )
    

class Text(Struct):
    token_id = AUT_TEXT
    identifier = "text"

    __fields__ = (
        String('data'),
    )
    

class Path(Text):
    token_id = AUT_PATH
    identifier = "path"


class Return(Struct):

    token_id = AUT_RETURN
    identifier = "return"

    __fields__ = (
        ReturnString("errno"),
    )
   

class Return32(Struct):
    """
        "errno": ">B",
        "value": ">I",
    """
    token_id = AUT_RETURN32
    identifier = "return"
    
    __fields__ = (
        Return(),
        UInt32("value"),
    )

class Return64(Return):
    token_id = AUT_RETURN64
    
    __fields__ = (
        Return(),
        UInt64("value"),
    )

class ReturnUuid(Struct):
    token_id = AUT_RETURN_UUID
    identifier = "ret_uuid"

    __fields__ = (
        Return(),
        UInt16("size_of_uuid"),
        String("uuid"),
    )


class Uuid(Struct):
    toekn_id = AUT_ARG_UUID
    identifier = "uuid"

class Identity(Struct):
    """
    "signer_type": ">I",
    "signing_size": ">H",
    "signing_id": ">{signing_size}s",
    "signing_id_truncated": ">B",
    "team_id_length": ">H",
    "team_id": ">{team_id_length}s",
    "team_id_truncated": ">B",
    "cdhash_size": ">H",
    "cdhash": ">{cdhash_size}s"
    """

    token_id = AUT_IDENTITY
    identifier = "identity"

    __fields__ = (
        "signer_type",            UInt32(),
        "signing_id",             String(),
        "signing_id_truncated",   CompleteString(),
        "team_id",                String(),
        "team_id_truncated",      CompleteString(),
        "cbhash",                 ByteString(),


class Subject(Struct):
    token_id = AUT_SUBJECT
    identifier = "subject"

    __fields__ = (
        "auid", User(),
        "euid", User(),
        "egid", Group(),
        "ruid", User(),
        "rgid", Group(),
        "pid", Process(),
        "sid", UInt32(),


class Subject32(Subject):
    """
    audit ID                4 bytes
    effective user ID       4 bytes
    effective group ID      4 bytes
    real user ID            4 bytes
    real group ID           4 bytes
    process ID              4 bytes
    session ID              4 bytes
    terminal ID
        port ID               4 bytes/8 bytes (32-bit/64-bit value)
        machine address       4 bytes
    """

    token_id = AUT_SUBJECT32

    __fields__ = (
        super()._setup()
        "tid_port",       UInt32(),
        "tid_address",    IPv4Address(),


class Subject32_Ex(Subject):
    """
    * audit ID                     4 bytes
    * euid                         4 bytes
    * egid                         4 bytes
    * ruid                         4 bytes
    * rgid                         4 bytes
    * pid                          4 bytes
    * sessid                       4 bytes
    * terminal ID
    *   portid             4 bytes
    *	 type				4 bytes
    *   machine id         16 bytes
    """

    token_id = AUT_SUBJECT32_EX
    identifier = "subject_ex"

    __fields__ = (
        super()._setup()
        "tid_port",       UInt32(),
        "tid_type",       UInt32(), show=False)
        "tid_address",    IPAddress(),

#TODO: Complete Subject64
class Subject64(Subject):
    token_id = AUT_SUBJECT64

#TODO: Complete Subject64Ex
class Subject64Ex(Subject):
    token_id = AUT_SUBJECT64_EX

class Attr(Struct):
    """
    * file access mode        4 bytes
    * owner user ID           4 bytes
    * owner group ID          4 bytes
    * file system ID          4 bytes
    * node ID                 8 bytes
    * device                  4 bytes/8 bytes (32-bit/64-bit)
    """
    token_id = AUT_ATTR
    identifier = "attribute"

    __fields__ = (
        'mode', UInt32(),
        'uid', User(),
        'gid', Group(),
        'fsid', UInt32(),
        'nodeid', UInt64(),
        'device', UInt32(),
    )
class Attr32(Attr):
    token_id = AUT_ATTR32

class Attr64(Attr):
    token_id = AUT_ATTR64


class Opaque(Struct):
    token_id = AUT_OPAQUE
    identifier = "opaque"

    __fields__ = (
        "data", ByteString(),


class Exit(Struct):
    """
    * status                  4 bytes
    * return value            4 bytes
    """
    token_id = AUT_EXIT
    identifier = "exit"

    __fields__ = (
        'errval', UInt32(),
        'retval', UInt32(),

class ExecArgs(Struct):
    """ TODO:
    * count                   4 bytes
    * text                    count null-terminated string(s)

    fetch_execarg_tok(tokenstr_t *tok, u_char *buf, int len)
    {
        int err = 0;
        u_int32_t i;
        u_char *bptr;

        READ_TOKEN_U_INT32(buf, len, tok->tt.execarg.count, tok->len, err);
        if (err)
            return (-1);

        for (i = 0; i < tok->tt.execarg.count; i++) {
            bptr = buf + tok->len;
            if (i < AUDIT_MAX_ARGS)
                tok->tt.execarg.text[i] = (char*)bptr;

            /* Look for a null terminated string. */
            while (bptr && (*bptr != '\0'), {
                if (++tok->len >= (u_int32_t)len)
                    return (-1);
                bptr = buf + tok->len;
            }
            if (!bptr)
                return (-1);
            tok->len++; /* \0 character */
        }
        if (tok->tt.execarg.count > AUDIT_MAX_ARGS)
            tok->tt.execarg.count = AUDIT_MAX_ARGS;

        return (0);
    }
    """
    token_id = AUT_EXEC_ARGS
    identifier = "exec arg"

    __fields__ = (
        "args", Texts(),

class ExecEnv(Struct):
    """ TODO:
    """
    token_id = AUT_EXEC_ENV
    identifier = "exec env"

    __fields__ = (
        "args", Texts(),

class OtherFile(Struct):
    """
    * seconds of time          4 bytes
    * milliseconds of time     4 bytes
    * file name len            2 bytes
    * file pathname            N bytes + 1 terminating NULL byte
    """
    token_id = AUT_OTHER_FILE32
    identifier = "file"

    __fields__ = (
        "time", UInt32(),
        "msec", MSec(),
        "pathname", String(),



class NewGroups(Struct):
    """
     * number groups           2 bytes
    * group list              count * 4 bytes
    """
    token_id = AUT_NEWGROUPS
    identifier = "group"
    
    __fields__ = (
        "groups", "{count}I", Groups)

class InAddr(Struct):
    """
     * Internet addr 4 bytes
    """
    token_id = AUT_IN_ADDR
    identifier = "ip addr"

    __fields__ = (
        "addr", IPv4Address(),

class InAddrEx(Struct):
    """
    type 4 bytes
    address 16 bytes
    """
    token_id = AUT_IN_ADDR_EX
    identifier = "ip addr ex"
    
    __fields__ = (
        "ad_type", UInt32(),
        "address", IPv6Address) # print_ip_ex_address

class Ip(Struct):
    """ TODO:
    ip header 20 bytes
    """
    token_id = AUT_IP
    identifier = "ip"

    __fields__ = (
        "version", "B", UInt32(),
        "tos", "B", UInt32(),
        "len", "H", UInt32(),
        "id", "H", UInt32(),
        "offset", "H", UInt32(),
        "ttl", "B", UInt32(),
        "prot", "B", UInt32(),
        "chksm", "H", UInt32(),
        "src", "I", UInt32(),
        "dest", "I", UInt32(),

class Ipc(Struct):
    """ TODO:
     * object ID type       1 byte
    * Object ID            4 bytes
    """
    token_id = AUT_IPC
    identifier = "ipc"

    __fields__ = (
        "ipc_type", "B", UInt32(),
        "ipc_id", "I", UInt32(),

class IpcPerm(Struct):
    """ TODO:
     * owner user id        4 bytes
    * owner group id       4 bytes
    * creator user id      4 bytes
    * creator group id     4 bytes
    * access mode          4 bytes
    * slot seq                     4 bytes
    * key                          4 bytes
    """
    token_id = AUT_IPC_PERM
    identifier = "IPC perm"

    __fields__ = (
        "uid", "I", UInt32(),
        "gid", "I", UInt32(),
        "puid", "I", UInt32(),
        "pgid", "I", UInt32(),
        "mode", "I", UInt32(),
        "seq", "I", UInt32(),
        "key", "I", UInt32(),


class Iport(Struct):
    """ TODO:
     * port Ip address  2 bytes
    """
    token_id = AUT_IPORT
    identifier = "ip port"

    __fields__ = (
        "port", "H", UInt32(),


class Process32(Subject32):
    """ TODO:
     * token ID                     1 byte
    * audit ID                     4 bytes
    * euid                         4 bytes
    * egid                         4 bytes
    * ruid                         4 bytes
    * rgid                         4 bytes
    * pid                          4 bytes
    * sessid                       4 bytes
    * terminal ID
    *   portid             4 bytes
    *   machine id         4 bytes
    """
    token_id = AUT_PROCESS32
    identifier = "process"

class Process32Ex(Subject32_Ex):
    """ TODO:
    * token ID                1 byte
    * audit ID                4 bytes
    * effective user ID       4 bytes
    * effective group ID      4 bytes
    * real user ID            4 bytes
    * real group ID           4 bytes
    * process ID              4 bytes
    * session ID              4 bytes
    * terminal ID
    *   port ID               4 bytes
    *   address type-len      4 bytes
    *   machine address      16 bytes
    """
    token_id = AUT_PROCESS32_EX
    identifier = "process"

class Process64(Subject):
    """ TODO:
    * token ID                     1 byte
    * audit ID                     4 bytes
    * euid                         4 bytes
    * egid                         4 bytes
    * ruid                         4 bytes
    * rgid                         4 bytes
    * pid                          4 bytes
    * sessid                       4 bytes
    * terminal ID
    *   portid             8 bytes
    *   machine id         4 bytes
    */
    """
    token_id = AUT_PROCESS64
    identifier = "process"

    __fields__ = (
        super()._setup()
        "tid_port", "Q", UInt32(),
        "tid_address", "I", IPv4Address(),

class Process64Ex(Subject):
    """ TODO:
    * token ID                1 byte
    * audit ID                4 bytes
    * effective user ID       4 bytes
    * effective group ID      4 bytes
    * real user ID            4 bytes
    * real group ID           4 bytes
    * process ID              4 bytes
    * session ID              4 bytes
    * terminal ID
    *   port ID               8 bytes
    *   address type-len      4 bytes
    *   machine address      16 bytes
    """
    token_id = AUT_PROCESS64_EX
    identifier = "process"

    __fields__ = (
        super()._setup()
        "tid_port", "Q", UInt32(),
        "tid_addr_type", "I", UInt32(),
        "tid_address", "2Q", UInt32(),


class Seq(Struct):
    token_id = AUT_SEQ
    identifier = "sequence"

    __fields__ = (
        "seqno", UInt32(),


class Socket(Struct):
    """
    * socket type             2 bytes
    * local port              2 bytes
    * local address           4 bytes
    * remote port             2 bytes
    * remote address          4 bytes
    """    
    token_id = AUT_SOCKET
    identifier = "socket"

    __fields__ = (
        "sock_type", UInt16(),
        "l_port", UInt16(),
        "l_addr", IPv4Address(),
        "r_port", UInt16(),
        "r_addr", IPv4Address(),
    

class SockInet32(Struct):
    """
    * socket family           2 bytes
    * local port              2 bytes
    * socket address          4 bytes
    """
    token_id = AUT_SOCKINET32
    identifier = "socket-inet"

    __fields__ = (
        "family", UInt16(),
        "port", UInt16(),
        "address", IPv4Address(),

#TODO: Complete Token classes

class SockUnix(Struct):
    """
    * socket family           2 bytes
    * path                    (up to) 104 bytes + NULL (NULL terminated string).
    """
    token_id = AUT_SOCKUNIX
    identifier = "socket-unix"

    __fields__ = (
        "addr_type", UInt16(),
        "path", String(),

class SockInet128(Struct):
    """
    * socket family	 2 bytes
    * local port		 2 bytes
    * socket address	16 bytes
    """
    token_id = AUT_SOCKINET128
    identifier = "socket-inet6"

    __fields__ = (
        "sock_type", UInt16(),
        "port", UInt16(),
        "addr", IPAddress(), # TODO: This field is dynamic field.

class SocketEx(Struct):
    """
    * socket domain           2 bytes
    * socket type             2 bytes
    * address type            2 bytes
    * local port              2 bytes
    * local Internet address  4/16 bytes
    * remote port             2 bytes
    * remote Internet address 4/16 bytes
    """
    token_id = AUT_SOCKET_EX
    identifier = "socket"

    __fields__ = (
        "domain", UInt16(),
        "sock_type", UInt16(),
        "addr_type", UInt16(),
        "l_port", UInt16(),
        "l_addr", IPAddress(),  # TODO: This field is dynamic field.
        "r_port", UInt16(),
        "r_addr", IPAddress(),  # TODO: This field is dynamic field.
    )

class Arb(Struct):
    """
    * how to print            1 byte
    * basic unit              1 byte
    * unit count              1 byte
    * data items              (depends on basic unit)
    """
    token_id = AUT_DATA
    identifier = "arbitrary"

    __fields__ = (
        ("", UInt8("howtopr"),
        ("bu", UInt8("bu"),,
        ("uc", UInt8(),,
        ("data", "set_data")
    )

    def set_data(self, rec: Rec):
        datasize_dict = {
            AUR_BYTE: AUR_BYTE_FORMAT,
            AUR_SHORT: AUR_SHORT_FORMAT,
            AUR_INT32: AUR_INT32_FORMAT,
            AUR_INT64: AUR_INT64_FORMAT,
        }
        datasize = datasize_dict[self.bu]
        fmt = f">{self.uc}{datasize}"
        fmt_length = struct.calcsize(fmt)
        return struct.unpack(fmt, rec.read(fmt_length),

class Zonename(Struct):
    """
    * size                         2 bytes;
    * zonename                     size bytes;
    """
    token_id = AUT_ZONENAME
    identifier = "zone"

    __fields__ = (
        "zoename", "{len}s", len_fmt="H", String(),
    
class Upriv(Struct):
    """
    * status                       1 byte
    * privstrlen                   2 bytes
    * priv                         N bytes + 1 (\0 byte)
    """
    token_id = AUT_UPRIV
    identifier = "use of privilege"

    __fields__ = (
        "status", type=UInt8(),
        "priv", String(), # TODO: string with terminator
    

class Priv(Struct):
    """
    /*
    * privtstrlen		1 byte
    * privtstr		    N bytes + 1
    * privstrlen		1 byte
    * privstr		    N bytes + 1
    */
    """
    token_id = AUT_PRIV
    identifier = "priv"

    __fields__ = (
        "privset", type=String(), # TODO length is not 16 bytes, it might requires __new__ function
        "privstr", type=String(), # TODO length is not 16 bytes
