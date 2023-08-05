EasyCluster
===========

EasyCluster is a remote execution / clustering module for Python.

Possible uses include:

* computation (e.g. NumPy, PyOpenCL)
* coordinated automation for testing networks / SANs
* access to specific hardware in multiple systems (e.g. GPUs, video capture/encoding boards)

Links
-----
* [Releases](https://pypi.python.org/pypi/EasyCluster)
* [Development](https://github.com/ktpanda/easycluster)
* [Documentation](http://pythonhosted.org/EasyCluster/)

Requirements
------------
* CPython 2.6+ or 3.2+
* SSH support requires an 'ssh' binary on the client, and 'sshd' on the server

Features
--------
* Transparent calling of functions and methods
* Transparent handling of exceptions
* Convenience functions for calling one function in parallel on
  multiple remote systems
* Automatic support for threading
* Requests and responses protected with shared HMAC key
* Connecting via SSH without installing anything on the server (Linux/Unix only)
* Cross-platform compatible; Master scripts running on Linux/OSX can connect
  to servers running on Windows and vice/versa.


Installing
----------

EasyCluster uses setuptools for installation. To install, run:

    python setup.py build
    sudo python setup.py install

If you do not have setuptools installed, it will be downloaded for you.


How it works
------------

EasyCluster works by having a single master script connect to one or more
servers running SSH or the cluster service. The master can then call Python
functions on the remote service or send code to execute.

See `easycluster_demo.py` for an example of how to use most of the features.

Since version 0.22.1, SSH is the preferred method of connecting to servers on
all platforms except Windows. When using SSH, the server does not need to have
easycluster installed - it only needs to have SSH and either Python 2.6, 2.7, or
3.2+. When using SSH, you should use SSH private keys and an SSH agent,
otherwise SSH will prompt for a password whenever it connects.

If you don't want to use SSH, e.g. you need to run the server on Windows and
don't want to run Cygwin, you will need to generate a secret key that is shared
between the client and server. This key is used to authenticate requests, but
does not encrypt data, therefore it should only be used on a trusted, firewalled
network, not openly on the Internet. If you want to use EasyCluster to
coordinate systems in remote geographic areas, consider using a VPN or SSH
tunnel. The EasyCluster service operates over a single TCP port, so most
tunneling solutions will work.


Connecting to a server
----------------------

The easiest way to use EasyCluster is to use Client.from_spec:

    >>> rmt = Client.from_spec('user@example.com')
    >>> rmt = ThreadedClient.from_spec('user@example.com:rpython=python2.7')

The connection spec looks like this::

    [user@]host[:port][:opt=val]...


The 'host' can be a hostname, IPv4 address, or bracketed IPv6 address.

For compatibility reasons, SSH is only used if the 'user' field is present. If
you want to use SSH without specifying a user name, pass ':ssh=yes' as an option.

For standalone servers, the key is determined by specifying either the 'kf' or 'key' options.

If ':compress=1' is specified, then compression is enabled for the connection.

Example connection specifications::

    'user@example.com'                   # Using SSH
    'example.com:ssh=yes'                # Using SSH without a user name (let SSH choose)
    'example.com:ssh=/usr/local/bin/ssh' # Using a custom SSH path
    'user@192.0.2.1:9999'                # IPv4 address on non-standard port
    'user@[2001:db8::2]'                 # IPv6 addresses must be in brackets
    'example.com:kf=secret.key'          # Connecting to a standalone server using a key from a file
    'example.com:9999:key=s3cret'        # Using a key directly, with non-standard port

The recommended way of allowing the user of your script to specify remote
options is to use `optparse`:

    # File: connect_example.py

    import sys
    import optparse
    import easycluster

    options = optparse.OptionParser(description='Do some stuff')
    easycluster.add_key_options(options)
    opts, args = options.parse_args()
    default_key = easycluster.key_from_options(opts)
    remotes = []
    for spec in args:
        params = easycluster.parse_connection_spec(spec, default_key=default_key)
        rmt = easycluster.Client(**params)
        remotes.append(rmt)

This example allows a user to specify a default key using `-k` (if multiple
servers use the same key), but allows the user to specify individual keys if
necessary:

    python do_stuff.py -k common.key host1 host2 oddhost:kf=key_for_oddhost.key

You can also specify a different TCP port to connect to. This is useful if you
want to use SSH tunnels:

    ssh host1 -N -f -L 11001:localhost:11999
    ssh host2 -N -f -L 11002:localhost:11999
    python do_stuff.py -k common.key localhost:11001 localhost:11002

The master script can connect to the same server multiple times. Each connection
creates a separate process with a clean environment. The master can also create
a "local" instance using `easycluster.server.spawn_local()`, which starts a new
server process without having to run a separate server.


Executing code remotely
-----------------------

The most straightforward way to execute code remotely is to define functions in
a string, and call `define_common()`:

    >>> from easycluster import *
    >>> define_common('''
    ... def addvals(a, b):
    ...     return a + b
    ... def subvals(a, b):
    ...     return a - b
    ... ''')
    >>> key = read_key_file('secret.key')
    >>> rmt = Client(key, 'localhost')
    >>> rmt.addvals(3, 4)
    7
    >>> rmt.subvals(15, 4)
    11

Any functions or classes you define in in the block of code passed to
`define_common` can be called on the remote side. You can also call functions in
classes defined in standard library modules:

    >>> rmt.subprocess.call(['/bin/echo', 'hello'])
    >>>

This example won't actually echo anything to your terminal - `echo` is executed
on the server, so if you have the server open in a terminal, you will see it
echoed there.

The block of code you pass to define_common is also evaluated on the client, so
functions, classes, and class instances can be pickled by reference and passed
back and forth between client and server. By default, a virtual module called
`easycluster.remote_code` is created to store the definitions. You can import
this module on the client if you want to run a function on both client and
server, or create a instance of a class that will be passed to the server by
value:

    >>> from easycluster.remote_code import addvals, subvals
    >>> addvals(1, 2)
    3
    >>>

You can change the name of the module by specifying a different second parameter
to `define_common`. Remember that since this code is executed in the context of
a different module, you won't have access to global variables and imported
modules from your master script:

    >>> import os
    >>> define_common('''
    ... def hello():
    ...     os.system('echo hello')
    ... ''')
    ...
    >>> rmt.hello()
    Traceback (most recent call last):
      ...
    NameError: global name 'os' is not defined
    >>>

You must remember to import whatever modules you need to use inside of your
define_common block. Of course, the libraries you import must be available on
the remote system too - EasyCluster will not copy them over.

Exceptions
----------

If the remote code raises an exception, the exception will be pickled up and
re-raised on the client, along with a stack trace. By default, the stack trace
will be printed to STDERR, because otherwise it would be lost - the stack trace
generated by raising the exception on the client only goes as far as the proxy
wrapper. If you don't want exceptions to be printed, you can subclass `Client`
and override `report_exception`. For a single request, you can also set
`origexc` to `False` or `'quiet'` (see the section on Parallel Execution below).

Manipulating objects on the server
----------------------------------

By default, if you call a function on the server, and it returns a value, that
value will be pickled, and a new copy of the object will be created on the
client. This is fine for simple values such as strings, integers, tuples,
dictionaries, etc., but a lot of objects can't or shouldn't be pickled; instead,
EasyCluster allows you to mark classes as "server objects" that are not pickled,
but remain on the server and are referenced by the client.

When the returned data structure is reconstructed on the client, any "server
objects" are converted into "proxy" objects. Calling a method on this proxy
calls the corresponding method on the server. These proxy objects can also be
passed as arguments to other functions on the same connection, and will be
unserialized as the original object on the server.

    >>> define_common('''
    ... class TestObject1(ServerObject):
    ...    def __init__(self, val):
    ...        self.val = val
    ...    def getval(self):
    ...        return self.val
    ...    def newobj(self):
    ...        return TestObject1(self.val + 1)
    ...
    ... def get_object_vals(lst):
    ...     return [obj.val for obj in lst]
    ... ''')
    >>>
    >>> # Call this on every connection after calling define_common.
    >>> rmt.update_definitions()
    >>>
    >>> obj1 = rmt.TestObject1(100)
    >>> obj1
    <RemoteProxy for oid 1 on localhost:11999>
    >>> obj1.getval()
    100
    >>> obj2 = obj1.newobj()
    >>> obj2
    <RemoteProxy for oid 2 on localhost:11999>
    >>> obj2.getval()
    101
    >>> rmt.get_object_vals[obj1, obj2]
    [100, 101]
    >>>

Classes can indicate that they should be proxied rather than copied by
inheriting from `ServerObject`. Existing classes which are unaware of EasyCluster
can be registered on the server by calling `make_server_class`.

There are two ways classes can specify which methods and attributes to export:

* Specifying `export_methods`, `export_attrs`, or `export_attrs_cache`.  Classes
  which inherit from `ServerObject` but do not specify a proxy class will have
  one dynamically created when they are first referenced. The server will
  examime the class to determine which methods and attributes should be
  exported.

    * If the class has a class attribute called `export_methods`, then the proxy
      class will only have wrappers for those methods.

    * If `export_methods` is not defined (default), or the special value `'@auto'`
      is in the list of exported method names, then the class will be examined,
      and all defined methods will be automatically added to the list.

    * The `export_attrs` class attribute works the same way: if it is defined,
      wrapper properties will be created on the proxy object for each
      attribute. If `export_attrs` is not defined, or `'@auto'` is included in
      export_attrs, then a special `__getattr__` is defined on the proxy which
      will forward attribute accesses to the server.

   * If you know that an attribute contains data which will not change over the
     lifetime of the object, you can put it in `export_attrs_cache`. The client
     will cache the value of the attribute the first time it is accessed, and
     won't access it again.

* Defining a proxy class directly. This is the most flexible way of exporting
  methods and attributes. This allows you to not only define proxy methods and
  attributes, but allows you to:

    * Implement simple methods on the client. For example, most iterators simply
      return `self` from `__iter__`. In fact, easycluster provides a proxy class
      you can inherit from called SelfIterProxy which does this.

    * Make your proxy object inherit from some other class so that
      `isinstance(prox, clas)` returns `True`.

Example of both methods:

    >>> define_common('''
    ... class TestObject2(TestObject1):
    ...     export_methods = ('getval',)
    ...     export_attrs = ('val',)
    ...
    ... class TestObject3Proxy(RemoteProxy):
    ...     proxy_methods = ('getval',)
    ...     proxy_attrs = ('val',)
    ...
    ... class TestObject3(TestObject1):
    ...     proxy_class = TestObject3Proxy
    ... ''')
    >>>
    >>> rmt.update_definitions()
    >>> obj2 = rmt.TestObject2(200)
    >>> obj2.val
    200
    >>> obj2.getval()
    200
    >>> obj2.non_existant_method()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'dynamic_proxy_getval_val' object has no attribute 'non_existant_method'
    >>>

    >>> define_common('''
    ... ''')
    >>> rmt.update_definitions()
    >>> obj3 = rmt.TestObject3(300)
    >>> type(obj3)
    <class 'easycluster_code.TestObject3Proxy'>
    >>> obj3.val
    300

If you have a built-in class or a class from a library module that you want to
treat as a "server object", you can call `easycluster.make_server_class()` in your
define_common block:

    >>> define_common('''
    ... import array
    ... make_server_class(array.array)
    ... ''')
    >>> rmt.update_definitions()
    >>> rmt_array = rmt.array.array('B', 1234)

You can pass `export_methods`, `export_attrs`, `export_attrs_cache`, and
`proxy_class` to `make_server_class`; they have the same meaning as defined for
ServerObject.

There is also a function called `make_singleton`, which behaves like
`make_server_class`, except it operates on a single instance of a class; if that
instance is returned, it will be proxied, but other instances of the same class
will be pickled.

Parallel Execution
------------------

Usually, clustering implies you want to execute code in parallel on multiple
systems. By default, calling remote code suspends execution of the master script
while the remote code is executing. However, there are several ways to execute
remote code in parallel.

The simplest way to do this is to use a non-blocking response:

    >>> rmt2 = Client(key, 'otherhost')
    >>> r1 = rmt.addvals(5, 8, nonblocking=True)
    >>> r2 = rmt2.addvals(14, 18, nonblocking=True)
    >>> r1.wait()
    13
    >>> r2.wait()
    32
    >>>

Passing `nonblocking=True` to any proxy method causes it to immediately return a
special "non-blocking response" object which has a `wait()` method. The `wait()`
method waits until the code has finished executing on the remote server and
returns the response value. If the remote side raised an exception, `wait()`
will raise the same exception (unless you pass `origexc` -- see below).

You can also use the convenience functions `eval_multi`, `call_multi`, and
`call_method_multi` to call the same function in parallel on multiple systems:

    >>> call_multi([rmt, rmt2], 'addvals', 2, 3)
    [5, 5]
    >>>

This function calls a specific function on multiple systems, waits for all of
the responses, then returns a list of their responses.

Besides `nonblocking`, there are other common keyword arguments that can be
passed to remote calls:

* `oncomplete` - If this is specified, then the remote call will return
  immediately, and will call this function when the remote call completes. This
  can be either a function which will be called as `func(response)`, or a tuple
  of `(func, arg1, arg2, ...)` which will be called as `func(response, arg1,
  arg2, ...)`. If you're using the standard `Client` class, completion functions
  will not be called until something calls `read_response()` on the client
  object, or calls `wait()` on a non-blocking response associated with the
  client. If you're using `ThreadedClient`, completion functions are called from
  the thread which reads responses from the server.

* `onerror` - Identical to oncomplete, but called with a `RemoteException`
  instance instead of a return value when the remote call raises an
  exception. If `oncomplete` is specified, but `onerror` is not, the
  `oncomplete` function is called in both cases.

* `threadid` - An arbitrary integer specifying the thread on the server to run
  the request in. If not specified, the current default will be used. The
  default can be changed by calling `set_default_thread()` on the client
  object. If the specified thread does not exist on the server, it is
  created. If the threadid is the special constant `easycluster.SINGLE`, a new
  thread is created on the server for this request, then exits.

* `origexc` - If `True` (default), and the request raises an exception, it will
  print the remote stack trace to the screen and raise the original
  exception. If it is `False`, a `RemoteException` is raised instead. If it is
  the value `'quiet'`, then the original exception is raised without a stack
  trace being printed. `RemoteException` instances have the two attributes:
  `orig`, the original exception; and `text`, the stack trace on the server.

You can start multiple threads on the same server by using non-blocking
responses with `threadid`:

    >>> r1 = rmt.addvals(101, 102, nonblocking=True, threadid=1)
    >>> r2 = rmt.addvals(222, 333, nonblocking=True, threadid=2)
    >>> r3 = rmt.addvals(555, 888, nonblocking=True, threadid=3)
    >>> [r1.wait(), r2.wait(), r3.wait()]
    [203, 555, 1443]


Using ThreadedClient
--------------------

If your master script is already multi-threaded, you can use `ThreadedClient`
to automatically manage server threads for you.

The `ThreadedClient` class starts a separate thread to read responses from the
server. Because of this, completion functions are called as soon as the remote
call returns, and the thread actively monitors the server to ensure that it
hasn't gone down or locked up.

`ThreadedClient` will detect if you call remote functions from a separate thread
in your master script, and will start a corresponding thread on the server to
handle your request:

    >>> import threading
    >>> tc1 = ThreadedClient(key, 'host1')
    >>> tc2 = ThreadedClient(key, 'host2')
    >>>
    >>> def client_thread(id, a, b):
    ...     print 'Thread %d: starting' % id
    ...     val1 = tc1.addvals(a, b)
    ...     print 'Thread %d: tc1 returned %r' % (id, val1)
    ...     val2 = tc2.addvals(a, b)
    ...     print 'Thread %d: tc2 returned %r' % (id, val2)
    ...     print 'Thread %d: finished' % id
    ...
    >>> def run_threads():
    ...     t1 = threading.Thread(target=client_thread, args=(1, 200, 500))
    ...     t2 = threading.Thread(target=client_thread, args=(2, 300, 600))
    ...     t1.start(); t2.start()
    ...     t1.join(); t2.join()
    ...
    >>> run_threads()
    Thread 1: starting
    Thread 2: starting
    Thread 1: tc1 returned 700
    Thread 2: tc1 returned 900
    Thread 1: tc2 returned 700
    Thread 2: tc2 returned 900
    Thread 1: finished
    Thread 2: finished
    >>>

Once threads in your master script exit, `ThreadedClient` will detect it and
stop the corresponding thread on the server.


Starting the standalone server
------------------------------

On POSIX systems (Linux, BSD, Solaris), a command called `easycluster` should be
installed in `/usr/local/bin`. On Windows, the main entry point is installed
under `%PYTHON%\scripts\easycluster.exe`. With Python 2.7 and 3.2, you can also
run `python -m easycluster`.

Before you run the server, you should create a secret HMAC keyfile. Both the
server and the client need this keyfile to be able to communicate:

    easycluster -g secret.key

This will create a new file, called 'secret.key' which is readable only by the
user that created it. You can then run the server with:

    easycluster -S -k secret.key

If you don't want to see every remote call logged, run:

    easycluster -S -k secret.key -c QuietServer


Running EasyCluster standalone server as a service on boot
----------------------------------------------------------

You can have the easycluster service start automatically on boot on Windows,
Solaris, and Linux (Redhat, Debian, Ubuntu, and SuSE have been tested):

    easycluster --install

This will register a service with the system which will start on the next
boot. You can unregister it with `easycluster --uninstall`. Once the service is
registered, you can start and stop it with `easycluster --start` and
`easycluster --stop`
