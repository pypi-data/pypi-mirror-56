#!/usr/bin/python

# Copyright (C) 2013 J. K. Stafford (jspenguin@gmail.com)
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""\
EasyCluster is a remote execution / clustering module for Python.

To get started, first generate a keyfile:
$ easycluster -g secret.key
$ ls -l secret.key
-rw------- 1 1000 1000 65 2012-12-05 16:00 test.key

Then start the server:
$ easycluster --serve -k secret.key
Listening on port 11999

>>> from easycluster import *
>>> define_common('''
... def addvals(a, b):
...     return a + b
... def subvals(a, b):
...     return a - b
... ''')
>>> key = read_key_file('secret.key')
>>> rmt = Client(key, 'localhost')
>>> rmt.execblock('print "Hello"')
>>>

"Hello" will be printed on the server side.

>>> rmt.addvals(3, 4)
7
>>> rmt.subvals(15, 4)
11
>>> rmt.subprocess.call(['/bin/echo', 'hello'])

"""
from __future__ import print_function

import sys
import os
import signal
import socket
import select
import traceback
import struct
import weakref
import time
import hmac
import threading
import errno

from hashlib import md5
from io import BytesIO, IOBase
from types import GeneratorType, ModuleType
from collections import deque
from binascii import a2b_hex, b2a_hex

VERSION = '0.06'

PYTHON3 = sys.version_info >= (3, 0)
if PYTHON3:
    import pickle
    import queue
    import builtins
    def _hexenc(data):
        return b2a_hex(data).decode('ascii')
    def _hexdec(data):
        return a2b_hex(data.encode('ascii'))
    _next_method = '__next__'
else:
    import cPickle as pickle
    import Queue as queue
    import __builtin__ as builtins
    _hexenc = b2a_hex
    _hexdec = a2b_hex

    ## Make all classes new-style by default
    __metaclass__ = type
    _next_method = 'next'

try:
    from select import epoll
except ImportError:
    epoll = None

_is_main = __name__ == '__main__'
if _is_main:
    __name__ = 'easycluster'
    sys.modules[__name__] = sys.modules['__main__']


__all__ = ['AutoThreadingClient', 'Client', 'ClientGroup', 'Connection',
           'DefaultRemoteProxy', 'QuietServer', 'RemoteException',
           'RemoteProxy', 'SelfIterProxy', 'Server', 'ServerObject',
           'add_key_options', 'call_method_multi', 'call_multi', 'decode_key',
           'define_common', 'definitions_module', 'eval_multi', 'exec_return',
           'execblock_multi', 'generate_key', 'key_from_options',
           'make_server_class', 'make_singleton', 'read_key_file', 'run_server',
           'server_check_runner', 'spawn_local', 'write_key_file',]

## Special value for TID which causes thread to exit after one request
SINGLE = -1


_nonblocking_errors = set()
for k in ('EWOULDBLOCK', 'EINTR', 'EINPROGRESS', 'EAGAIN'):
    val = getattr(errno, k, None)
    if val is not None:
        _nonblocking_errors.add(val)
del k, val

try:
    from socket import socketpair
except ImportError:
    def socketpair():
        '''Emulate socketpair() using a locally-bound TCP socket'''
        socka = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socka.setblocking(0)

        svr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        svr.bind(('127.0.0.1', 0))

        svr.listen(1)
        try:
            socka.connect(svr.getsockname())
        except socket.error as e:
            if e.errno not in _nonblocking_errors:
                raise

        socka.setblocking(1)
        while True:
            sockb, addr = svr.accept()

            ## There is a short window in which another local application may
            ## connect to the listening socket we just opened. If the address
            ## returned by accept() does not match our socket, close it and try
            ## again. 
            if addr == socka.getsockname():
                svr.close()
                return socka, sockb
            sockb.close()

HMAC_MOD = md5
HMAC_SIZE = len(HMAC_MOD().digest())
ERROR, CHALLENGE, CHALLENGE_RESPONSE, KEEPALIVE, REQUEST, RESPONSE, INIT = range(7)
_pickle_messages = set([REQUEST, RESPONSE, INIT])

DEFAULT_PORT = 11999

_singletons = {}

_extra_base_classes = {}

def eval_multi(connections, code):
    '''Evaluates a Python expression on multiple connections in parallel. Does
    not return until all hosts finish executing the code.

    `connections` is a list (or other sequence) of Client instances to run the
    code on.

    `code` is the code to run, which will be executed in the context of the
    easycluster_code module.

    Returns a list of return values in the same order as _connections. To
    associate the connections with return values, use 
    zip(connections, eval_multi(connections, ...)).
    '''

    resp = [h.eval(code, nonblocking=True) for h in connections]
    return [r.wait() for r in resp]

def execblock_multi(connections, code):
    '''Similar to eval_multi, except `code` is a block of python code instead of
    a single expression.
    '''

    resp = [h.evalblock(code, nonblocking=True) for h in connections]
    return [r.wait() for r in resp]

def call_multi(_connections, _func, *a, **kw):
    '''Calls a function on multiple connections in parallel.
    
    _connections is a list (or other sequence) of connections to call
    the function on.

    _func is the absolute name of the function to call. See
    Client.call for details.

    Any extra arguments are passed to the remote function.

    Returns a list of return values in the same order as _connections. To
    associate the connections with return values, use 
    zip(connections, call_multi(connections, ...)).
    '''
    resp = [h.raw_call(_func, a, kw, nonblocking=True) for h in _connections]
    return [r.wait() for r in resp]
    
def call_method_multi(_objects, _method, *a, **kw):
    '''Calls a method on multiple RemoteProxy objects in parallel. Each
    object should be associated with a different Client instance,
    although this is not enforced.
    
    _objects is a list (or other sequence) of RemoteProxy to call the
    method on.

    _method is the name of the method to be called.

    Any extra arguments are passed to the remote function.

    Returns a list of return values in the same order as _objects. To
    associate the connections with return values, use 
    zip(objects, call_multi(objects, ...)).
    '''
    resp = [o.raw_call_method(_method, a, kw, nonblocking=True) for o in _objects]
    return [r.wait() for r in resp]

def make_server_class(typ, export_methods=(), export_attrs=(), proxy_class=None):
    '''Mark a pre-existing class as a server-object class. This function will
    attempt to assign attributes to 'typ'; if that fails, the type will be added
    to a global dictionary.
    
    typ is an old-style or new-style class.
    export_methods is a sequence of method names that the class exports.
    export_attrs is a sequence of attribute names that the class exports.
    proxy_class is a class to instantiate as a proxy for `typ`.

    export_methods and export_attrs are ignored when proxy_class is given.
    '''

    try:
        typ.export_methods = export_methods
        typ.export_attrs = export_attrs
        typ.proxy_class = proxy_class
        typ._is_server_object = True
    except Exception:
        # If setting attributes on the type fails, it probably means it's an
        # extension type that doesn't have a __dict__. In that case, store it in
        # _extra_base_classes; Server.persistent_id searches through the MRO of
        # new-style classes to find the first one in this dict.
        _extra_base_classes[typ] = export_methods, export_attrs, proxy_class

def make_singleton(obj, export_methods=(), export_attrs=(), proxy_class=None):
    '''Mark a singleton object instance as a server object. When this object is
    referenced in a return value, it will be instantiated on the client as a
    simple remote proxy.
    '''

    addr = id(obj)
    def wrcb(wr, addr=addr):
        _singletons.pop(addr, None)
        
    try:
        wr = weakref.ref(obj, wrcb)
        obj = None
    except TypeError:
        ## type(obj) is not weakref-capable.
        wr = None
        
    _singletons[addr] = export_methods, export_attrs, proxy_class, wr, obj

class DummyConnection(object):
    '''Replacement object for _connection in invalidated proxies.'''
    peername = '<closed connection>'
    def send_request(self, *a, **kw):
        raise IOError("Connection has been closed")

_dummy_connection = DummyConnection()

class RemoteProxyRef(weakref.ref):
    __slots__ = ('oid',)
    def __new__(cls, prox, cb, oid):
        self = weakref.ref.__new__(cls, prox, cb)
        self.oid = oid
        return self
    
    def __init__(self, prox, cb, oid):
        super(RemoteProxyRef, self).__init__(prox, cb)

def _create_wrapper_method(name):
    def rtnf(self, *a, **kw):
        return self._connection.send_request(self._oid, name, a, kw, *_get_special_keywords(kw))
    rtnf.__name__ = name
    return rtnf

def _create_attr_wrapper(name):
    def get(self):
        return self._connection.send_request(0, 'getattr', (self, name))

    def set(self, value):
        return self._connection.send_request(0, 'setattr', (self, name, value))

    def delete(self):
        return self._connection.send_request(0, 'delattr', (self, name))

    return property(get, set, delete)

class RemoteProxyMeta(type):
    def __new__(mcs, clsname, bases, typedict):
        proxy_methods = typedict.setdefault('proxy_methods', ())
        proxy_attrs = typedict.setdefault('proxy_attrs', ())
        for name in proxy_methods:
            typedict[name] = _create_wrapper_method(name)

        for name in proxy_attrs:
            typedict[name] = _create_attr_wrapper(name)
        
        return super(RemoteProxyMeta, mcs).__new__(mcs, clsname, bases, typedict)

RemoteProxyBase = RemoteProxyMeta('RemoteProxyBase', (object,), {'__module__': __name__})

class RemoteProxy(RemoteProxyBase):
    '''A client-side proxy for an object on the server.'''

    typeid = None

    def __init__(self, client, oid):
        '''Create a RemoteProxy object. This should not be called
        directly. RemoteProxy objects are created automatically when a
        ServerObject is returned by the server.'''

        self._connection = client
        self._oid = oid

    @property
    def proxy_connection(self):
        '''Returns the connection that this object is associated with, or None
        if the connection was closed.'''
        ret = self._connection
        if ret is _dummy_connection:
            ret = None
        return ret

    @property
    def proxy_object_id(self):
        '''The object ID assigned by the remote connection for this object'''
        return self._oid

    def raw_call_method(self, method, args, kwargs={}, nonblocking=False,
                        oncomplete=None, onerror=None, threadid=None):
        '''Call a method on the remote object. 

        method is the method to call.
        args is a tuple of positional arguments to the method
        kwargs is a dict of keyword arguments to the method

        See Client.send_request for the meaning of the 'nonblocking',
        'oncomplete', 'onerror', and 'threadid' arguments. 
        '''
        return self._connection.send_request(self._oid, method, args, kwargs,
                                         nonblocking, oncomplete, onerror, threadid)

    def __repr__(self):
        return '<RemoteProxy for oid %d on %s>' % (self._oid, self._connection.peername)

class DefaultRemoteProxy(RemoteProxy):
    """A remote proxy for server-side classes that don't explicitly export
    any methods.
    """
    def __getattr__(self, attr):
        return _create_wrapper_method(attr).__get__(self)

class SelfIterProxy(RemoteProxy):
    """A proxy class for an iterator which returns itself when __iter__ is
    called."""
    proxy_methods = (_next_method,)

    def __iter__(self):
        return self

class ServerObject:
    '''A base class for objects which can be referenced by a client.'''
    _is_server_object = True
    export_methods = True
    export_attrs = ()
    proxy_class = None

class RemoteException(Exception):
    '''Raised on the client when an exception occurs during execution, and the
    origexc argument to NonblockingResponse.wait is False.

    Attributes:

    orig: The original exception raised by the call
    text: A list of strings as returned by traceback.format_exception.
    '''
    def __init__(self, orig=None, text=None):
        Exception.__init__(self, str(orig))
        self.orig = orig
        self.text = text

class NonblockingResponse:
    '''Returned by remote calls when the `nonblocking` flag is set to True.'''
    def __init__(self, client, request_id):
        self.client = client
        self.request_id = request_id
        self._have_response = False
        self._response_val = None

    @property
    def have_response(self):
        '''Returns True if a response is available.'''
        return self._have_response

    def fileno(self):
        '''Returns the file descriptor of the associated Client instance so that
        responses can be used with select().

        '''
        return self.client.fileno()
    
    def read_response(self, block=True):
        '''Calls read_response on the associated Client.'''
        return self.client.read_response(block)
    
    def set_response(self, val):
        self._response_val = val
        self._have_response = True

    def wait(self, origexc=True):
        '''Waits for the request to complete.
        
        If the call causes an exception and `origexc` is True (default), the
        remote exception traceback is printed to sys.stderr and the original
        exception is raised. If origexc is False, a RemoteException is raised
        instead and the remote traceback is not printed.
        '''

        self.client._wait_for_response(self)

        rval = self._response_val
        if type(rval) is RemoteException:
            if origexc:
                self.client.report_exception(rval)
                raise rval.orig
            raise rval
        return rval

class Connection:
    '''Base class for Client and Server objects'''
    def __init__(self, key):
        self._key = key
        self._recv_buf = BytesIO()
        self._recv_expect = 5
        self._recv_msgtype = None
        self._recv_data = None
        self._recv_expect_hmac = None
        self._recv_hmac = None
        self._send_hmac = None
        self._peer_version = None
        self._init_data = {'version': VERSION}
        
        self._my_nonce = struct.pack('>d', time.time()) + os.urandom(HMAC_SIZE - 8)
        self._verified = False

        self._sock = None
        self._peername = ''
        self._remote_host = None
        self._remote_port = None
        
        self._lock = threading.Lock()
        self._sendlock = threading.Lock()

    @property
    def peername(self):
        '''The name of the host we are connected to'''
        return self._peername

    @property
    def connected(self):
        '''True if we are connected to a remote host.'''
        return self._sock is not None

    @property
    def remote_host(self):
        '''The hostname or IP address passed to connect(), or None for a local
        connection'''
        return self._remote_host

    @property
    def remote_port(self):
        '''The TCP port passed to connect(), or None for a local connection'''
        return self._remote_port

    def connect(self, host, port=DEFAULT_PORT):
        '''Connect to a remote host.'''
        self._remote_host = host
        self._remote_port = port
        self._peername = '%s:%d' % (host, port)
        self.set_socket(socket.create_connection((host, port)))
        
    def reconnect(self):
        '''Reconnect to the remote host. This will reset the remote environment,
        and any currently held proxied objects will become invalid.'''
        if self._remote_host is None:
            raise ValueError('Cannot reconnect before first connection.')
        self.close()
        self.connect(self._remote_host, self._remote_port)

    def set_socket(self, sock, peername=None):
        '''Use an already-open socket for this connection.'''
        if peername is None:
            peername = _get_peer_name(sock.getpeername())

        _mark_non_inheritable(sock.fileno())
        self._sock = sock
        self._peername = peername
        self._recv_hmac = hmac.new(self._key, self._recviv, HMAC_MOD)
        self._send_hmac = hmac.new(self._key, self._sendiv, HMAC_MOD)
        self._after_connect()
        
    def _after_connect(self):
        pass

    def send_challenge(self):
        self.send_message(CHALLENGE, self._my_nonce)

    def _on_ready(self):
        pass
        
    def send_message(self, typ, data):
        hdr = struct.pack('>BI', typ, len(data))
        hmac = self._send_hmac
        with self._sendlock:
            hmac.update(hdr)
            hmac.update(data)
            if typ == ERROR:
                digest = b''
            else:
                digest = hmac.digest()
                hmac.update(digest)
            _sock_sendall(self._sock, b''.join((hdr, data, digest)))

    def make_pickle(self, object):
        sio = BytesIO()
        p = pickle.Pickler(sio, protocol=pickle.HIGHEST_PROTOCOL)
        p.persistent_id = self._persistent_id
        p.dump(object)
        return sio.getvalue()
        
    def fileno(self):
        '''Returns the file descriptor of the connected socket.'''
        return self._sock.fileno()
    
    def _got_request(self, p):
        return True

    def _got_response(self, p):
        return True

    def _got_init(self, p):
        self._peer_version = p.get('version')
        return True

    def _got_keepalive(self):
        pass

    def _read_data(self, block=True):
        ## attribute access protected by GIL
        sock = self._sock
        if sock is None:
            raise EOFError
        
        recv_buf = self._recv_buf
        recv_hmac = self._recv_hmac
        while True:
            try:
                data = sock.recv(self._recv_expect)
            except socket.error as e:
                if e.errno not in _nonblocking_errors:
                    raise
                if not block:
                    return False
                select.select([sock], [], [], None)
                continue

            if not data:
                raise EOFError

            recv_hmac.update(data)
            recv_buf.write(data)
            newlen = self._recv_expect - len(data)
            if newlen > 0:
                self._recv_expect = newlen
                continue

            data = recv_buf.getvalue()
            recv_buf.seek(0)
            recv_buf.truncate(0)
            if self._recv_msgtype is None:
                self._recv_msgtype, self._recv_expect = struct.unpack('>BI', data)
                if self._recv_expect == 0:
                    data = ''
                else:
                    continue

            if self._recv_msgtype == ERROR:
                self._recv_msgtype = None
                self._recv_expect = 5
                raise ValueError('Peer error: %s' % data)
            
            if self._recv_data is None:
                self._recv_data = data
                self._recv_expect_hmac = recv_hmac.digest()
                self._recv_expect = HMAC_SIZE
            else:
                rmsg = self._recv_msgtype
                rdata = self._recv_data
                expect_hmac = self._recv_expect_hmac

                self._recv_expect = 5
                self._recv_msgtype = None
                self._recv_data = None
                self._recv_expect_hmac = None

                if data != expect_hmac:
                    self.send_message(ERROR, b'HMAC error')
                    continue

                if rmsg in _pickle_messages:
                    if not self._verified:
                        self.send_message(ERROR, b'Not verified')
                        continue

                    p = pickle.Unpickler(BytesIO(rdata))
                    p.persistent_load = self._persistent_load
                    pick = p.load()
                    if rmsg == REQUEST:
                        return self._got_request(pick)
                    elif rmsg == RESPONSE:
                        return self._got_response(pick)
                    elif rmsg == INIT:
                        return self._got_init(pick)

                elif rmsg == KEEPALIVE:
                    self._got_keepalive()
                elif rmsg == CHALLENGE:
                    self.send_message(CHALLENGE_RESPONSE, rdata)
                elif rmsg == CHALLENGE_RESPONSE:
                    if rdata == self._my_nonce:
                        self._verified = True
                        self.send_message(INIT, self.make_pickle(self._init_data))
                        self._on_ready()
                    else:
                        self.send_message(ERROR, b'Invalid nonce')
                else:
                    self.send_message(ERROR, b'Invalid message type')

    def close(self):
        '''Close the connection.'''
        if self._sock is not None:
            self._sock.shutdown(socket.SHUT_RDWR)
            self._sock = None

class _GlobalProxy:
    '''A proxy for a global object on a remote server'''
    __slots__ = ('_client', '_name')
    def __init__(self, client, name):
        self._client = client
        self._name = name

    @property
    def value(self):
        return self._client.send_request(0, 'get_global', (self._name,))
 
    @value.setter
    def value(self, newval):
        self._client.send_request(0, 'set_global', (self._name, newval))
        return newval

    def __getattr__(self, name):
        return _GlobalProxy(self._client, '%s.%s' % (self._name, name))
    
    def __call__(self, *args, **kw):
        return self._client.raw_call(self._name, args, kw, *_get_special_keywords(kw))

class Client(Connection):
    '''Represents the client side of the connection. '''

    _sendiv = b'CLNT'
    _recviv = b'SRVR'
    
    def __init__(self, key, sock_or_host=None, port=DEFAULT_PORT,
                 definitions='easycluster_code'):
        '''Create a new Client object.

        `key` is the HMAC key to use.

        `sock_or_host` is either an open socket or a host name, or None. If None
        is given, you must call connect() or set_socket() before using the
        Client instance.

        `port` is the TCP port to use, if a host name is given.

        `definitions` is the name of the dynamic module where common definitions
        are stored. This must be the same name passed to define_common() or
        definitions_module().
        '''
        Connection.__init__(self, key)

        self._next_request_id = 0
        self._pending_requests = None
        self._nonblocking_responses = {}
        self._completion = {}

        self._default_thread = 0

        def proxy_deleted(refdat, wrself=weakref.ref(self)):
            self = wrself()
            if self is not None:
                self._proxy_by_id.pop(refdat.oid, None)
                self._garbage_proxies.append(refdat.oid)

        self._proxy_deleted = proxy_deleted

        ## Proxies that we have for remote objects
        self._proxy_by_id = {}
        self._proxy_type_by_id = {}
        self._garbage_proxies = []

        self._is_ready = False
        self._defmod = definitions_module(definitions)
        self._init_data['definitions_module'] = definitions

        ## Compatibility with 0.05 server
        self._init_data['definitions_source'] = []
        self._peer_version = None

        if hasattr(sock_or_host, 'send'):
            self.set_socket(sock_or_host)
        elif sock_or_host is not None:
            self.connect(sock_or_host, port)

    def _init_thread(self):
        pass

    def _after_connect(self):
        self._is_ready = False
        self._pending_requests = []
        self._init_response = None

        self._definition_count = 0

        self._sock.setblocking(0)
        self._init_thread()
        self.send_challenge()
        if self._defmod._source_code:
            self.update_definitions(oncomplete=lambda val: None, 
                                    onerror=self._init_error)

    def _init_error(self, exc):
        self.report_exception(exc)
        ## Raise the error in all outstanding requests
        self.close(exc)

    def read_response(self, block=True):
        '''Try to read a response and call its completion function (if any).
        Returns True when a response is received, or False if 'block' is false
        and a response was not processed.

        If using select or another I/O polling method, this method should be
        called after the poll indicates the socket is ready for reading.
        '''
        return self._read_data(block)

    def set_default_thread(self, threadid):
        '''Set the default thread id.'''
        self._default_thread = threadid

    def _on_ready(self):
        with self._lock:
            self._is_ready = True
            rq = self._pending_requests
            self._pending_requests = None
        for p in rq:
            self.send_message(REQUEST, p)
        
    def ready(self):
        '''Returns True if our peer is ready to accept requests.'''
        return self._is_ready
    
    def wait_ready(self):
        '''Wait until the peer is ready to accept requests.'''
        while not self._is_ready:
            self.read_response()

    def get_root(self):
        '''Returns the a proxy for the 'root' object, which is used to
        implement 'call' and 'eval' functions.'''
        return DefaultRemoteProxy(self, 0)

    def _thread_id(self):
        return self._default_thread

    def _set_nbr_response(self, nbr, response):
        '''Set the response value for a non-blocking response and wake it up if
        necessary.'''
        nbr.set_response(response)

    def _got_response(self, p):
        rid, response = p
        complete = self._completion.pop(rid, None)
        if not complete:
            nbr = self._nonblocking_responses.pop(rid, None)
            if nbr is None:
                return
            nbr = nbr()
            if nbr is None:
                return
            self._set_nbr_response(nbr, response)
            return True

        # index 0 = oncomplete, index 1 = onerror
        compf = complete[int(type(response) is RemoteException)]
        if isinstance(compf, tuple):
            compf[0](response, *compf[1:])
        else:
            compf(response)
        return True

    def send_request(self, oid, meth, args, kwargs={}, nonblocking=False,
                     oncomplete=None, onerror=None, threadid=None):
        '''Send a request to the remote server. This method is normally not
        called directly.

        oid is the object ID of the object on which to call the method. 
        args is a tuple of positional arguments to the method
        kwargs is a dict of keyword arguments to the method

        If nonblocking is False and oncomplete is None, this method waits for
        the remote call to finish, then returns the value returned by the remote
        method call.
        If oncomplete is specified, it must be a function which is called with
        the return value when the request is complete. If the request raises an
        exception, onerror is called with a RemoteException instance. If onerror
        is not specified, it defaults to oncomplete.

        oncomplete or onerror may also be a tuple of (func, arg1, arg2, ...) in
        which case the function will be called as func(resp, arg1, arg2, ...).

        If nonblocking is True, a NonblockingResponse object is returned instead.

        threadid is the remote thread to queue the response in. If not
        specified, the current default will be used. The default can be changed
        by calling set_default_thread(). If the specified thread does not
        exist on the server, it is created. If the threadid is the special
        constant SINGLE, a new thread is created on the server for this request,
        then exits.

        If your client application is multithreaded, and you want to have a
        separate thread on the server for each client, see AutoThreadingClient.

        See NonblockingResponse.wait for details on exception handling.
        '''
        with self._lock:
            if self._sock is None:
                raise IOError("Not connected")
            if threadid is None:
                threadid = self._thread_id()

            request_id = self._next_request_id 
            self._next_request_id = request_id + 1

            garbage = []
            gobj = self._garbage_proxies
            while gobj:
                garbage.append(gobj.pop())
        
            try:
                rq = self.make_pickle((request_id, garbage, threadid,
                                       oid, meth, args, kwargs))
            except Exception:
                gobj.extend(garbage)
                raise

            if not self._is_ready:
                self._pending_requests.append(rq)
                rq = None
        
        if oncomplete is not None:
            if onerror is None:
                onerror = oncomplete
            self._completion[request_id] = oncomplete, onerror
            rval = request_id
        else:
            rval = NonblockingResponse(self, request_id)
            self._nonblocking_responses[request_id] = weakref.ref(rval)
        if rq is not None:
            self.send_message(REQUEST, rq)

        if oncomplete is None and not nonblocking:
            return rval.wait()
        return rval

    def report_exception(self, exc):
        '''Report a remote exception to sys.stderr. This can be
        overridden in a subclass to change exception reporting.'''
        ## Don't print anything for StopIteration; remote iterators may generate this.
        if isinstance(exc.orig, StopIteration):
            return

        if exc.text:
            print('*** Remote exception from %s:' % (self._peername), file=sys.stderr)
            print(''.join(exc.text), file=sys.stderr)

    def stop_remote_thread(self, threadid):
        '''Stop the remote thread identified by 'threadid' once it has finished
        processing all of its requests.'''

        self.send_message(REQUEST, self.make_pickle((None, None, threadid,
                                                     None, None, None, None)))

    def _wait_for_response(self, nbr):
        '''Wait for a response to complete. Normally not called directly.'''
        while not nbr._have_response:
            self.read_response()

    def update_definitions(self, nonblocking=False,
                           oncomplete=None, onerror=None, threadid=None):
        '''Call this after calling define_common to send any new common
        definitions to the server.'''

        source = self._defmod._source_code
        current_count = self._definition_count
        rv = self.send_request(0, 'update_definitions', (source[current_count:],), {}, 
                          nonblocking, oncomplete, onerror, threadid)
        self._definition_count = len(source)
        return rv

    def raw_call(self, func, args, kwargs={}, nonblocking=False,
                        oncomplete=None, onerror=None, threadid=None):
        '''Call a function on the remote server.

        func is the absolute name of the function to call. If 'func'
        is a simple name, it is assumed to be in the 'easycluster_code'
        module. This simplifies access to classes and functions
        defined with 'eval'.
        args is a tuple of positional arguments to the function.
        kwargs is a dict of keyword arguments to the function.

        See Client.send_request for the meaning of the 'nonblocking',
        'oncomplete', 'onerror', and 'threadid' arguments. 
        '''
        return self.send_request(0, 'call', (func, args, kwargs), {},
                                 nonblocking, oncomplete, onerror, threadid)
        
    def call(self, _func, *args, **kwargs):
        '''Wrapper for raw_call which allows specifying
        arguments directly.'''
        return self.raw_call(_func, args, kwargs, *_get_special_keywords(kwargs))

    def eval(self, expr, nonblocking=False, oncomplete=None, onerror=None, threadid=None):
        '''Evaluate an expression on the remote server. The code is executed in
        the context of the 'easycluster_code' module.

        See Client.send_request for the meaning of the 'nonblocking',
        'oncomplete', 'onerror', and 'threadid' arguments. 
        '''
        return self.send_request(0, 'eval', (expr, 'eval'), {},
                                 nonblocking, oncomplete, onerror, threadid)

    def execblock(self, code, nonblocking=False, oncomplete=None, onerror=None, threadid=None):
        '''Run a block of code on the remote server. The code is executed in the
        context of the 'easycluster_code' module. Returns None unless the block
        executes exec_return().

        See Client.send_request for the meaning of the 'nonblocking',
        'oncomplete', 'onerror', and 'threadid' arguments. 
        '''
        return self.send_request(0, 'eval', (code, 'exec'), {},
                                 nonblocking, oncomplete, onerror, threadid)

    def import_modules(self, names, nonblocking=False, oncomplete=None, onerror=None, threadid=None):
        '''Imports one or more modules on the remote server.

        client.import_modules(["sys", "os"])

        is equivalent to

        client.eval("import sys, os")

        `names` is a list of modules to import.

        See Client.send_request for the meaning of the 'nonblocking',
        'oncomplete', 'onerror', and 'threadid' arguments. 

        '''

        return self.send_request(0, 'import_modules', (names,), {},
                                 nonblocking, oncomplete, onerror, threadid)

    def import_module(self, name, nonblocking=False, oncomplete=None, onerror=None, threadid=None):
        '''Imports a module on the remote server. Equivalent to import_modules([name]).'''

        return self.send_request(0, 'import_modules', ([name],), {},
                                 nonblocking, oncomplete, onerror, threadid)

    @property
    def server_version(self):
        '''Return the version of EasyCluster on the server'''
        return self._peer_version

    def __getattr__(self, attr):
        '''Returns a proxy object to call a global function or class on the
        server. This lets you do things like:

        client.os.system("echo hello")

        '''

        return _GlobalProxy(self, attr)

    def _persistent_id(self, obj):
        if isinstance(obj, RemoteProxy):
            if obj._connection is self:
                return str(obj._oid)
            raise TypeError('cannot send %r to remote connection %s' % (obj, self._peername))

    def _persistent_load(self, id):
        l = id.split('\n')
        oid = int(l[0])

        wrprox = self._proxy_by_id.get(oid)
        if wrprox is not None:
            prox = wrprox()
            if prox is not None:
                return prox

        proxclas = tid = typedat = None
        if len(l) > 1:
            tid = int(l[1])
            proxclas = self._proxy_type_by_id.get(tid)
 
            # Check if we have a type created for this object
            if proxclas is None and len(l) > 2:
                typedat = l[2]
                if typedat == ':!:':
                    proxclas = DefaultRemoteProxy
                elif typedat[0] == ':':
                    _, export_methods, export_attrs = typedat.split(':')
                    base_class = RemoteProxy
                    if export_methods == '!':
                        base_class = DefaultRemoteProxy
                        export_methods = []
                    else:
                        export_methods = export_methods.split(',')
                    export_attrs = export_attrs.split(',')
                    typedict = {'__module__':__name__, 
                                'proxy_methods': export_methods,
                                'proxy_attrs': export_attrs
                                }
                    proxclas = RemoteProxyMeta('dynamic_proxy_' + '_'.join(export_methods + export_attrs), 
                                               (base_class,), typedict)

                else:
                    mod, cls = typedat.rsplit('.', 1)
                    try:
                        proxclas = getattr(_get_module(mod), cls)
                    except (ImportError, AttributeError):
                        proxclas = DefaultRemoteProxy
                self._proxy_type_by_id[tid] = proxclas

        prox = (proxclas or DefaultRemoteProxy)(self, oid)
        ref = RemoteProxyRef(prox, self._proxy_deleted, oid)
        self._proxy_by_id[oid] = ref
        return prox

    def close(self, message='Connection closed'):
        '''Close the connection and invalidate all remote proxies. `message` is
        either a string or a RemoteException instance to raise in all
        outstanding requests.'''
        Connection.close(self)
        proxies = self._proxy_by_id
        while proxies:
            oid, wrprox = proxies.popitem()
            prox = wrprox()
            if prox is not None:
                prox._connection = _dummy_connection
                
        ## Send an error to any outstanding requests
        if isinstance(message, RemoteException):
            error = message
        else:
            error = RemoteException(IOError(message), '')

        comp = self._completion
        while comp:
            rid, (oncomplete, onerr) = comp.popitem()
            try:
                if isinstance(onerr, tuple):
                    onerr[0](error, *onerr[1:])
                else:
                    onerr(error)
            except Exception:
                pass

        nbrs = self._nonblocking_responses
        while nbrs:
            rid, nbr = nbrs.popitem()
            nbr = nbr()
            if nbr:
                nbr.set_response(error)
        

class AutoThreadingClient(Client, threading.Thread):
    '''A client that automatically creates unique threads on the server for each
    thread on the client that makes remote calls.

    Whenever a request is made from a thread on a client, a new thread is
    created on the server. All requests made from this client thread are
    processed by the same thread on the server. If the client thread exits, the
    server thread will be stopped once check_threads() is called. By default,
    threads are checked whenever a response is received.

    This class creates a new thread on the client to process responses. Completion
    functions will be called in the context of this thread. read_response() must not be
    called. This class is also incompatible with ClientGroup.
    '''
    
    def __init__(self, key, sock_or_host=None, port=DEFAULT_PORT,
                 definitions='easycluster_code', keep_alive_interval=10, 
                 keep_alive_timeout=60):
        '''Creates a new AutoThreadingClient. Arguments are the same as Client.'''
        threading.Thread.__init__(self)
        self.daemon = True


        ## use pseudo-thread IDs instead of sending real ones
        self._next_thread_id = 1
        self._id_by_thread = {}
        self._response_lock = threading.Lock()
        self._have_response = threading.Condition(self._response_lock)
        self._keep_alive_interval = keep_alive_interval
        self._keep_alive_timeout = keep_alive_timeout
        self._last_keep_alive = None

        Client.__init__(self, key, sock_or_host, port, definitions)

        self._init_data['keep_alive_interval'] = keep_alive_interval

    def _init_thread(self):
        self.start()

    def _got_keepalive(self):
        self._last_keep_alive = time.time()

    def check_threads(self):
        '''Check for threads that have exited, and kill the 
        corresponding threads on the server.'''
        done = []
        with self._lock:
            if not self._is_ready:
                return
            for t, id in list(self._id_by_thread.items()):
                if not t.is_alive():
                    done.append(id)
                    del self._id_by_thread[t]
        for id in done:
            self.stop_remote_thread(id)

    def run(self):
        '''Read responses from the server.'''
        next_wake_time = 0
        fd = self.fileno()
        self._got_keepalive()
        closeargs = ()
        try:
            while True:
                ctime = time.time()
                timeout = self._keep_alive_timeout
                if timeout is not None:
                    if ctime >= self._last_keep_alive + timeout:
                        closeargs = ('Remote server not responding',)
                        return

                if ctime >= next_wake_time:
                    next_wake_time = ctime + 1
                    # Wake up any threads that are waiting so they can check if they've
                    # been interrupted.
                    with self._response_lock:
                        self._have_response.notify_all()
                    continue
                rd, _, _ = select.select([fd], (), (), next_wake_time - ctime)
                if rd:
                    if self._read_data(False):
                        ## Check thread status after every valid message received
                        self.check_threads()
        except socket.error as e:
            if e.errno != errno.ECONNRESET:
                raise
        except EOFError:
            ## Swallow this error so it isn't printed. Since we call close(),
            ## any outstanding or future requests will fail.
            pass
        finally:
            self.close(*closeargs)

    def read_response(self, *args):
        '''Do not call this method on AutoThreadingClient.'''
        raise TypeError('read_response should not be called on AutoThreadingClient objects')

    ## called with lock held
    def _thread_id(self):
        ct = threading.current_thread()
        tid = self._id_by_thread.get(ct)
        if tid is None:
            tid = self._next_thread_id
            self._next_thread_id = tid + 1
            self._id_by_thread[ct] = tid
        return tid
    
    def _set_nbr_response(self, nbr, response):
        with self._response_lock:
            nbr.set_response(response)
            self._have_response.notify_all()

    def _add_pending_response(self, rid, response):
        with self._response_lock:
            self._pending_responses[rid] = response
            self._have_response.notify_all()

    def _wait_for_response(self, nbr):
        '''Wait for a response to complete. This method is normally not called
        directly.
        '''
        with self._response_lock:
            while not nbr._have_response:
                self._have_response.wait()

    def close(self, *a):
        '''Close the connection and stop the processing thread.'''
        ## This will shut down the socket and cause the reading thread to exit
        ## cleanly.
        with self._response_lock:
            Client.close(self, *a)
            self._have_response.notify_all()

class RootObject:
    '''Utility class instantiated automatically on the server as OID 0.'''
    def __init__(self):
        self._defmod = None

    def eval(self, code, mode):
        cb = compile(code, '<remote code>', mode, dont_inherit=True)
        try:
            return eval(cb, self._defmod.__dict__)
        except _ExecReturn as e:
            return e.val
        
    def get_global(self, name):
        return _get_global(name, self._defmod, True)

    def set_global(self, name, value):
        return _set_global(name, self._defmod, value)

    def update_definitions(self, code):
        for c in code:
            self._defmod.define(c)

    def call(self, func, args, kwargs={}):
        f = _get_global(func, self._defmod, True)
        return f(*args, **kwargs)
        
    def getattr(self, obj, attr):
        return getattr(obj, attr)

    def setattr(self, obj, attr, val):
        return setattr(obj, attr, val)

    def delattr(self, obj, attr):
        return delattr(obj, attr)

    def import_modules(self, names):
        for n in names:
            setattr(self._defmod, n, __import__(n))
        
class ServerThread(threading.Thread):
    '''A thread that runs code on behalf of the client.'''
    def __init__(self, svr, tid):
        threading.Thread.__init__(self)
        self.tid = tid
        self.lock = threading.Lock()
        self.queue = queue.Queue()
        self.svr = svr
        self.daemon = True

    def run(self):
        '''Runs the server request thread.'''
        queue = self.queue
        svr = self.svr
        self.svr = None

        while True:
            rid, obj, meth, args, kw = queue.get()
            if obj is None:
                return
            svr.run_request(rid, obj, meth, args, kw)

class Server(Connection):
    '''Represents the server side of a remote connection.'''

    _sendiv = b'SRVR'
    _recviv = b'CLNT'

    def __init__(self, key, sock, peername):
        Connection.__init__(self, key)
        self._next_object_id = 1
        self._next_type_id = 1

        # Local object that our peer has proxies for
        root = RootObject()
        self._root = root
        self._local_object_by_id = {0: root}
        self._local_id_by_object = {id(root): 0}
        self._local_type_by_id = {}
        self._local_id_by_type = {}
        
        self._pending_responses = deque()
        self._keep_alive_interval = None

        self._threads = {}
        self.set_socket(sock, peername)

        
    def _after_connect(self):
        self._sock.setblocking(1)
        self.send_challenge()

    def report_connection(self):
        '''Report that a connection was received.'''
        print('New connection from %s' % (self._peername))

    def report_disconnection(self):
        '''Report that a client disconnected.'''
        print('Connection to %s terminated' % (self._peername))

    def report_request(self, rid, garbage, tid, oid, meth, args, kw):
        '''Report a request from the client.'''
        if rid is not None:
            print('Request %d: <%s> %d.%s g=%s' % (rid, tid, oid, meth, garbage))

    def run_request(self, rid, oid, meth, args, kw):
        '''Processes a single request.'''
        try:
            obj = self._local_object_by_id[oid]
            rval = getattr(obj, meth)(*args, **kw)
            with self._lock:
                rpickle = self.make_pickle((rid, rval))
        except Exception:
            typ, val, tb = sys.exc_info()
            text = traceback.format_exception(typ, val, tb)
            rval = RemoteException(val, text)
            with self._lock:
                rpickle = self.make_pickle((rid, rval))
        self.send_message(RESPONSE, rpickle)

    def _got_request(self, p):
        rid, garbage, tid, oid, meth, args, kw = p
        if garbage:
            with self._lock:
                for deloid in garbage:
                    obj = self._local_object_by_id.get(deloid)
                    if obj is not None:
                        del self._local_object_by_id[deloid]
                        del self._local_id_by_object[id(obj)]

        self.report_request(rid, garbage, tid, oid, meth, args, kw)
        if tid == SINGLE:
            t = threading.Thread(target=self.run_request, args=(rid, oid, meth, args, kw))
            t.start()
            return True

        t = self._threads.get(tid)
        if oid is None:
            ## request to end thread
            if t is not None:
                del self._threads[tid]
        elif t is None:
            self._threads[tid] = t = ServerThread(self, tid)
            t.start()

        if t is not None:
            t.queue.put((rid, oid, meth, args, kw))
        return True


    def _got_init(self, args):
        super(Server, self)._got_init(args)
        self._root._defmod = definitions_module(args['definitions_module'], False)
        self._keep_alive_interval = args.get('keep_alive_interval')
        if self._keep_alive_interval:
            self._sock.setblocking(0)
            
        self._root._defmod.running_server = self
        return True

    def run(self):
        '''Runs the main server thread.'''
        self.report_connection()
        next_keep_alive = 0
        try:
            while True:
                if self._keep_alive_interval:
                    ctime = time.time()
                    rtime = next_keep_alive - ctime
                    if rtime <= 0:
                        next_keep_alive = ctime + self._keep_alive_interval
                        self.send_message(KEEPALIVE, b'')
                        continue
                    r, w, e = select.select([self._sock], (), (), rtime)
                    if self._sock in r:
                        self._read_data(False)
                else:
                    self._read_data(True)
        except socket.error as e:
            if e.errno != errno.ECONNRESET:
                raise
        except EOFError:
            pass
        self.report_disconnection()

        threads = self._threads.values()
        for t in threads:
            t.queue.put((None, None, None, None, None))
        for t in threads:
            t.join()

    def _persistent_load(self, id):
        '''Implements Unpickler.persistent_load.'''
        return self._local_object_by_id.get(int(id))

    def _persistent_id(self, obj):
        '''Implements Unpickler.persistent_id.'''
        oid = self._local_id_by_object.get(id(obj))
        if oid is not None:
            return str(oid)

        ## Find out if the object is a server object or not
        typ = obj.__class__
        tid = self._local_id_by_type.get(typ)
        if tid is None:
            export_methods, export_attrs, proxy_class = _get_proxy_data(obj, typ)
            if export_methods is None:
                return None
        oid = self._next_object_id
        self._next_object_id = oid + 1
        self._local_id_by_object[id(obj)] = oid
        self._local_object_by_id[oid] = obj

        if tid is not None:
            return '%d\n%d' % (oid, tid)
        elif not (proxy_class or export_methods or export_attrs):
            return str(oid)
        else:
            tid = self._next_type_id
            self._next_type_id = tid + 1
            self._local_id_by_type[typ] = tid
            self._local_type_by_id[tid] = typ
            if proxy_class:
                typedat = proxy_class.__module__ + '.' + proxy_class.__name__
            else:
                if export_methods is True:
                    export_methods = ('!',)
                typedat = ':' + ','.join(export_methods) + ':' + ','.join(export_attrs)
            return '%d\n%d\n%s' % (oid, tid, typedat)

class ClientGroup:
    '''Represents a set of Client objects that can be queried as a group.'''

    def __init__(self, clients=()):
        '''Create a new ClientGroup object. 'clients' is an optional sequence of
        Client instances to add to the group.'''
        self.clients = {}
        self.epoll = (epoll() if epoll is not None else None)
        for c in clients:
            self.add_client(c)
        
    def add_client(self, cl):
        '''Add a Client instance to the group. Does nothing if the client is already registered.'''
        fd = cl.fileno()
        mycl = self.clients.get(fd)
        if cl is mycl:
            return

        if mycl and self.epoll:
            self.epoll.unregister(fd)

        self.clients[fd] = cl
        if self.epoll:
            self.epoll.register(fd, select.POLLIN|select.POLLERR|select.POLLHUP)

    def remove_client(self, cl):
        '''Remove a Client instance from the group. Does nothing if the client is not registered.'''
        fd = cl.fileno()
        mycl = self.clients.get(fd)
        if cl is mycl:
            del self.clients[fd]
            if self.epoll:
                self.epoll.unregister(fd)

    def read_responses(self, timeout=None, max=-1):
        '''Read responses from the Client objects in the group.'''
        etime = (None if timeout is None else time.time() + timeout)
        while max:
            rtime = (1000.0 if etime is None else etime - time.time())
            if rtime < 0:
                rtime = 0
            if self.epoll:
                evts = self.epoll.poll(rtime, len(self.clients))
                if not evts and not rtime:
                    return
                for fd, evt in evts:
                    if self.clients[fd].read_response(False):
                        if max > 0:
                            max -= 1
                            if max == 0:
                                return
                        
            else:
                r, _, _ = select.select(self.clients.values(), (), (), rtime)
                if not r and not rtime:
                    return
                for client in r:
                    if client.read_response(False):
                        if max > 0:
                            max -= 1
                            if max == 0:
                                return

class QuietServer(Server):
    '''A subclass of Server which does not print anything to output.'''
    def report_connection(self):
        pass

    def report_disconnection(self):
        pass

    def report_request(self, *args):
        pass

def exec_return(rval):
    '''When called from within code sent to Client.eval, causes eval to return 'rval'.'''
    raise _ExecReturn(rval)

def definitions_module(name, keep_source=True):
    '''Get or create a module to store common definitions in.''' 
    mod = sys.modules.get(name)
    if mod is not None:
        try:
            mod._source_code
        except AttributeError:
            raise ImportError('%s already exists, but is not a dynamic module' % name)
        return mod
    mod = ModuleType(name, 'EasyCluster common definitions')
    sys.modules[name] = mod
    mod._source_code = source = []
    def define(code):
        if not code.endswith('\n'):
            code += '\n'
        cb = compile(code, '<easycluster definitions %r>' % name, 'exec', dont_inherit=True)
        eval(cb, mod.__dict__)
        if keep_source:
            source.append(code)
            
    mod.define = define
    define.__module__ = name
    define('import easycluster\nfrom easycluster import *\n')
    del source[:]
    return mod

def define_common(code, name='easycluster_code'):
    '''Define common classes in the specified module. Equivalent to:
    definitions_module(name).define(code)
    '''
    definitions_module(name).define(code)

def decode_key(key):
    '''If 'key' is a hex-encoded string of the proper size, returns the actual key,
    otherwise just returns the original string.'''
    try:
        if len(key) == 2*HMAC_SIZE:
            return _hexdec(key)
    except Exception:
        traceback.print_exc()
    return key.encode('utf-8')

def read_key_file(path):
    '''Read an HMAC key from a file.'''
    with open(path, 'r') as fp:
        return decode_key(fp.readline().rstrip('\r\n'))

def write_key_file(path, key, overwrite=False):
    '''Write an HMAC key to a file. If overwrite is True, it will try to
    overwrite the key file if it already exists.'''
    if not _write_key_file(path, key):
        if not overwrite:
            return False
        os.unlink(path)
        return _write_key_file(path, key)
    return True

def generate_key():
    '''Generates a random HMAC key of the proper size.'''
    return os.urandom(HMAC_SIZE)


def add_key_options(options, key_option='-K', keyfile_option='-k'):
    '''Add options for specifying a HMAC key or keyfile to an optparse.OptionParser.'''
    options.add_option(key_option, '--key', help='HMAC key to use; either a %d-character hex string '
                       'or a ASCII string which will be padded. This method of specifying a key '
                       'is insecure because other users on the system can read it.' % (2*HMAC_SIZE))
    options.add_option(keyfile_option, '--keyfile', metavar='FILE', help='Read HMAC key from file. This '
                       'is the preferred method of specifying a key.')
    
def key_from_options(opts, warn=True):
    '''Get an HMAC key from an options instance.

    >>> options = optparse.OptionParser()
    >>> easycluster.add_key_options(options)
    >>> opts, args = options.parse_args()
    >>> key = easycluster.key_from_options(opts)
    >>>
    '''
    key = b''
    if opts.keyfile:
        key = read_key_file(opts.keyfile)
    elif opts.key:
        if warn:
            print('SECURITY WARNING: using key from command line.', file=sys.stderr)
        key = decode_key(opts.key)
    if key == b'' and warn:
        print('SECURITY WARNING: running with blank key.', file=sys.stderr)
    return key

def server_main(args=None):
    '''Run by the easycluster script.'''
    server_check_runner()

    from optparse import OptionParser
    if args is None:
        args = sys.argv[1:]

    key = ''
    options = OptionParser(description="Runs the EasyCluster service and generates keyfiles", version=VERSION)
    add_key_options(options)
    options.add_option('-S', '--serve', metavar='FILE', action='store_true', help='Run the server on the specified port')
    options.add_option('-g', '--generate', metavar='FILE', help='Generate random HMAC key and '
                       'write it to FILE. The file will be created with read access only for the owner.')
    options.add_option('-O', '--overwrite', metavar='FILE', action='store_true', help='Allow --generate to overwrite existing keyfile')
    options.add_option('-p', '--port', type='int', default=DEFAULT_PORT, help='TCP port to listen on. Default: %d' % DEFAULT_PORT)
    options.add_option('-c', '--class', dest='svrclass', default='easycluster.Server', help='Fully-qualified name of server class')
    opts, args = options.parse_args(args)

    if opts.generate:
        if not write_key_file(opts.generate, generate_key(), opts.overwrite):
            print('Key file already exists (use --overwrite to overwrite it)', file=sys.stderr)
        return

    elif opts.serve:
        key = key_from_options(opts)
        if '.' in opts.svrclass:
            svrmod, svrclassname = opts.svrclass.rsplit('.')
            clas = getattr(_get_module(svrmod), svrclassname)
        else:
            clas = globals()[opts.svrclass]

        run_server(opts.port, key, clas)
    else:
        options.print_help()

def run_server(port, key, svrclass=Server):
    '''Runs a server on the specified port.

    port is the TCP port to listen on.
    key is the HMAC key to use.
    svrclass is the server class to instantiate for each client
    (default: easycluster.Server).
    '''
    server_init()

    if socket.has_ipv6:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        # Windows needs this socket option set to listen on both IPV4 and
        # IPV6. However, IPPROTO_IPV6 is missing from the socket module on Windows.
        # Since the value is likely to never change, just include it here.
        IPPROTO_IPV6 = 41
        sock.setsockopt(IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    _mark_non_inheritable(sock.fileno())

    sock.bind(('', port))
    sock.listen(1)

    print('Listening on port %d' % port)
    while True:
        try:
            csock, addr = sock.accept()
        except socket.error as e:
            if e.errno in _nonblocking_errors:
                continue
            else:
                raise
        spawn_runner_process(csock, _get_peer_name(addr), svrclass, key)
        csock.close()

_local_id = 0

def spawn_local(clientclass=Client, svrclass=QuietServer):
    '''Create a private server instance and connect to it.'''
    global _local_id
    csock, ssock = socketpair()
    _mark_non_inheritable(csock.fileno())

    spawn_runner_process(ssock, 'local:%d' % _local_id, svrclass, b'')
    ssock.close()

    rc = clientclass(b'')
    rc.set_socket(csock, 'local:%d' % _local_id)
    _local_id += 1
    return rc

###############################
# Internal classes
###############################

class GeneratorProxy(SelfIterProxy):
    """A proxy class for generator objects."""
    proxy_methods = 'send', 'throw', 'close'

    def __iter__(self):
        return self

class FileProxy(RemoteProxy):
    """A proxy class for files and file-like objects."""
    proxy_methods = ('close',  'errors', 'fileno', 'flush', 'isatty', 'next', 'read', 
                     'readinto', 'readline', 'readlines', 'seek', 'tell', 'truncate', 
                     'write', 'writelines', 'xreadlines')
    proxy_attrs = ('closed', 'encoding', 'errors', 'mode', 'name', 'newlines')

class _ExecReturn(BaseException):
    def __init__(self, val):
        self.val = val

###############################
# Internal functions
###############################

def _get_proxy_data(obj, typ):
    '''Returns the proxy class or exported attributes and methods for object
    `obj` of type `typ`.

    '''
    sdat = _singletons.get(id(obj))
    if sdat is not None:
        export_methods, export_attrs, proxy_class, wr, sobj = sdat
        if sobj is not None or (wr is not None and wr() is obj):
            return export_methods, export_attrs, proxy_class
    
    if hasattr(typ, '_is_server_object'):
        return typ.export_methods, typ.export_attrs, typ.proxy_class
    else:
        ebc = _extra_base_classes
        for b in getattr(typ, '__mro__', ()):
            r = ebc.get(b)
            if r:
                return r
    return None, None, None

def _get_module(name):
    '''Imports and returns a module object.'''
    components = name.split('.')
    mod = __import__(name)
    for c in components[1:]:
        mod = getattr(mod, c)
    return mod

def _get_global_root(mod, attr):
    try:
        return getattr(mod, attr)
    except AttributeError:
        return getattr(builtins, attr)

def _try_import(mod, name, is_root):
    newname = (name if is_root else mod.__name__ + '.' + name)

    try:
        newmod = __import__(newname)
    except ImportError:
        return False

    if is_root:
        setattr(mod, name, newmod)

    return True

def _get_global(name, defmod, auto_import=False):
    """
    Get a global variable in the context of `defmod`. If `name` contains
    periods, it will call getattr() to resolve the actual value of the object.

    If `auto_import` is true, and accessing a value from a module fails, it will
    attempt to import the module and retry the access.

    """

    components = name.split('.')
    _getattr = _get_global_root
    val = defmod

    for i, name in enumerate(components):
        try:
            val = _getattr(val, name)
        except AttributeError:
            if auto_import and isinstance(val, ModuleType) and _try_import(val, name, i == 0):
                val = _getattr(val, name)
            else:
                raise
        _getattr = getattr

    return val

def _set_global(name, defmod, value):
    """
    Set a global variable in the context of `defmod`. If `name` contains
    periods, it will call getattr() to resolve the actual object on which to set
    the attribute.

    """

    components = name.split('.')
    if len(components) == 1:
        setattr(defmod, name, value)
    else:
        gv = _get_global('.'.join(components[:-1]))
        setattr(gv, components[-1], value)

def _get_peer_name(addr):
    if isinstance(addr, tuple):
        host, port = addr[:2]
        ## When listening on a dual-stack socket, IPv4 addresses
        ## are embedded within IPv6 addresses.
        if host.startswith('::ffff:'):
            host = host[7:]
        ## Standard convention for IPv6 addresses is to surround
        ## them with brackets when used with a port number.
        if ':' in host:
            host = '[%s]' % host
        return '%s:%d' % (host, port)
    return addr

def _sock_sendall(sock, data):
    '''Send all of `data` over `sock`, blocking until the send is complete'''
    while data:
        try:
            numsent = sock.send(data)
            data = data[numsent:]
        except socket.error as e:
            if e.errno not in _nonblocking_errors:
                raise
            select.select([], [sock], [], None)

def _get_special_keywords(kwargs):
    '''Returns the values of the keywords nonblocking, oncomplete, onerror, and threadid.'''
    
    nonblocking = kwargs.pop('nonblocking', False)
    oncomplete = kwargs.pop('oncomplete', None)
    onerror = kwargs.pop('onerror', None)
    threadid = kwargs.pop('threadid', None)
    return nonblocking, oncomplete, onerror, threadid

def _add_extra_classes():
    _file_export = ((), (), FileProxy)

    _extra_base_classes[GeneratorType] = ((), (), GeneratorProxy)
    _extra_base_classes[IOBase] = _file_export
    try:
        _extra_base_classes[file] = _file_export
    except NameError:
        pass

    try:
        import _io
        _extra_base_classes[_io._IOBase] = _file_export
        del _io
    except (NameError, ImportError):
        pass
    
    # Proxy module objects.
    _extra_base_classes[ModuleType] = ((), (), None)
    
_add_extra_classes()
del _add_extra_classes

if os.name == 'nt':
    from ctypes import (windll, Structure, Union, c_size_t, c_int,
                        py_object, POINTER, pythonapi, create_string_buffer, WinError)
    import subprocess

    kernel32 = windll.kernel32
    SetHandleInformation = kernel32.SetHandleInformation

    # Windows does not support "inheriting" sockets; the only way to
    # pass an open socket to another process is to use the
    # WSADuplicateSocket function, send the WSAPROTOCOL_INFO over a
    # pipe, then call WSASocket in the receiving process.
    #
    # Python 3.3 implements this as share() and fromshare().
    if hasattr(socket, 'fromshare'):
        def dupsock(sock, pid):
            return sock.share(pid)
            
        def make_socket(af, stype, proto, protoinfo):
            return socket.fromshare(protoinfo)
    else:

        winsock = windll.ws2_32
        WSASocket = winsock.WSASocketA
        WSADuplicateSocket = winsock.WSADuplicateSocketA
        WSAGetLastError = winsock.WSAGetLastError
        WSASetLastError = winsock.WSASetLastError
        WSAclose = winsock.closesocket
        PyErr_SetExcFromWindowsErr = pythonapi.PyErr_SetExcFromWindowsErr
        PyErr_SetExcFromWindowsErr.argtypes = [py_object, c_int]

        def _raise_socket_error():
            ec = WSAGetLastError()
            WSASetLastError(0)
            PyErr_SetExcFromWindowsErr(socket.error, ec)

        def dupsock(sock, pid):
            pinfo = create_string_buffer(512)
            rv = WSADuplicateSocket(sock.fileno(), pid, pinfo)
            if rv != 0:
                _raise_socket_error()
            return pinfo.raw

        ## Replicate the relevant fields from socketmodule.h. This has been
        ## consistent through CPython 2.5 (the first to support ctypes)
        ## through 2.7.3, and for CPython 3.0 to 3.3, where it is
        ## unnecessary. It is unlikely to change, since 2.7 is the last 
        ## major version of Python 2.x.
        class _socketobject(Structure):
            _fields_ = [("refcount", c_size_t),
                        ("classptr", py_object),
                        ("fd", c_int)]

        class _socketunion(Union):
            _fields_ = [('pyo', py_object),
                       ('sock', POINTER(_socketobject))]

        ## This function hacks a socket object to change its descriptor to the
        ## one returned by WSASocket.
        def make_socket(af, stype, proto, protoinfo):
            ## Get a socket handle for the socket we want to create
            newfd = WSASocket(af, stype, proto, protoinfo, 0, 0)
            if newfd < 0:
                _raise_socket_error()

            ## Create a new socket object
            sock = socket.socket(af, stype, proto)

            ## Get the original file descriptor so we can close it
            rfd = sock.fileno()

            try:
                sobj = sock._sock
            except AttributeError:
                sobj = sock
            sobj = _socketunion(sobj).sock.contents
            assert sobj.fd == rfd, 'socket structure mismatch'

            ## Replace the descriptor with the new value
            sobj.fd = newfd

            ## Close the original descriptor
            WSAclose(rfd)
            return sock

    MAGIC_ARG = '--easycluster-run-server'
    
    def _mark_non_inheritable(fd):
        """Mark the given handle as non-inheritable."""
        if not SetHandleInformation(fd, 1, 0):
            raise WinError()

    def spawn_runner_process(csock, peername, svrclass, key):
        args = [sys.executable, sys.argv[0], MAGIC_ARG]
        p = subprocess.Popen(args, stdin=subprocess.PIPE)
        pinfo = dupsock(csock, p.pid)
        p.stdin.write(b2a_hex(pickle.dumps((pinfo, csock.family, csock.type, csock.proto, peername, svrclass, key), protocol=pickle.HIGHEST_PROTOCOL)) + b'\r\n')
        p.stdin.close()
                
    def server_check_runner():
        if len(sys.argv) == 2 and sys.argv[1] == MAGIC_ARG:
            pinfo, family, type, proto, peername, svrclass, key = pickle.loads(_hexdec(sys.stdin.readline().strip()))
            sys.stdin.close()
            sock = make_socket(family, type, proto, pinfo)
            try:
                svrclass(key, sock, peername).run()
            except Exception:
                traceback.print_exc()
            sys.exit(0)
                
    def server_init():
        pass

    def _write_key_file(path, key):
        '''Write an HMAC key to a file. Returns True if the file was created, or
        False if it already exists.'''
        import win32api, win32file, win32security
        import ntsecuritycon, win32con, pywintypes
        user, domain, type = win32security.LookupAccountName ("", win32api.GetUserName())

        dacl = win32security.ACL()
        dacl.AddAccessAllowedAce(win32security.ACL_REVISION, 
                                 ntsecuritycon.FILE_ALL_ACCESS, user)

        sd = win32security.SECURITY_DESCRIPTOR()
        sd.SetSecurityDescriptorDacl(1, dacl, 0)

        sa = win32security.SECURITY_ATTRIBUTES()
        sa.SECURITY_DESCRIPTOR = sd
        sa.bInheritHandle = 0

        try:
            fil = win32file.CreateFile(path, win32con.GENERIC_WRITE, 0, sa, 
                                       win32con.CREATE_NEW, 0, 0)
        except pywintypes.error as e:
            ## File exists.
            if e[0] == 80:
                return False
        try:
            win32file.WriteFile(fil, _hexenc(key) + '\r\n', None)
        finally:
            win32file.CloseHandle(fil)
        return True

else:
    import fcntl
    
    try:
        _max_fd = os.sysconf('SC_OPEN_MAX')
    except Exception:
        _max_fd = 1024

    def sigcld(signal, frame):
        try:
            while True:
                pid, status = os.waitpid(-1, os.WNOHANG)
                if not pid:
                    return
        except OSError:
            pass

    def _mark_non_inheritable(fd):
        fcntl.fcntl(fd, fcntl.F_SETFD, fcntl.fcntl(fd, fcntl.F_GETFD, 0) | fcntl.FD_CLOEXEC)

    def server_check_runner():
        pass

    def spawn_runner_process(csock, peername, svrclass, key):
        cpid = os.fork()
        if cpid == 0:
            fd = csock.fileno()
            os.closerange(3, fd)
            os.closerange(fd + 1, _max_fd)
            try:
                svrclass(key, csock, peername).run()
            except Exception:
                traceback.print_exc()
            sys.exit(0)

    def server_init():
        signal.signal(signal.SIGCLD, sigcld)

    def _write_key_file(path, key):
        '''Write an HMAC key to a file. Returns True if the file was created, or
        False if it already exists.'''
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except OSError as e:
            if e[0] == errno.EEXIST:
                return False
        try:
            os.write(fd, _hexenc(key) + '\n')
        finally:
            os.close(fd)
        return True

if _is_main:
    server_main()
