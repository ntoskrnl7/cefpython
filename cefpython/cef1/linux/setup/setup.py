from distutils.core import setup
# Use "Extension" from Cython.Distutils so that "cython_directives" works.
# from distutils.extension import Extension
from Cython.Distutils import build_ext, Extension
import sys
import platform
from Cython.Compiler import Options

BITS = platform.architecture()[0]
assert (BITS == "32bit" or BITS == "64bit")

# Stop on first error, otherwise hundreds of errors appear in the console.
Options.fast_fail = True

# Since Cython 0.18 it is required to set string encoding
if sys.version_info.major < 3:
    C_STRING_TYPE = "str"
    C_STRING_ENCODING = "utf8"
else:
    C_STRING_TYPE = "unicode"
    C_STRING_ENCODING = "utf8"

# Written to cython_includes/compile_time_constants.pxi
CEF_VERSION = 1

# Python version string: "27" or "32".
PYTHON_VERSION = str(sys.version_info.major) + str(sys.version_info.minor)

def CompileTimeConstants():

    print("Generating: cython_includes/compile_time_constants.pxi")
    with open("./../../../cython_includes/compile_time_constants.pxi", "w") as fd:
        fd.write('# This file was generated by setup.py\n')
        # A way around Python 3.2 bug: UNAME_SYSNAME is not set.
        fd.write('DEF UNAME_SYSNAME = "%s"\n' % platform.uname()[0])
        fd.write('DEF CEF_VERSION = %s\n' % CEF_VERSION)

CompileTimeConstants()

ext_modules = [Extension(

    "cefpython_py%s" % PYTHON_VERSION,
    ["cefpython.pyx"],

    cython_directives={
        "c_string_type": C_STRING_TYPE,
        "c_string_encoding": C_STRING_ENCODING,
    },

    language='c++',
    include_dirs=[
        r'./../',
        r'./../../',
        r'./../../../',
        r'./../../../cython_includes/',
        '/usr/include/gtk-2.0',
        '/usr/include/glib-2.0',
        '/usr/lib/i386-linux-gnu/gtk-2.0/include',
        '/usr/lib/i386-linux-gnu/glib-2.0/include',
        '/usr/include/cairo',
        '/usr/include/pango-1.0',
        '/usr/include/gdk-pixbuf-2.0',
        '/usr/include/atk-1.0',
        # 64bit Ubuntu
        '/usr/lib/x86_64-linux-gnu/glib-2.0/include',
        '/usr/lib/x86_64-linux-gnu/gtk-2.0/include',
    ],

    # http_authentication not implemented on Linux.
    library_dirs=[
        r'./lib_%s' % BITS,
        r'./../../v8function_handler/',
        r'./../../client_handler/',
        r'./../../../cpp_utils/'
    ],

    libraries=[
        'cef_dll_wrapper',
        'v8function_handler',
        'client_handler',
        'cpp_utils'
    ],

    # Loading libcef.so will only work when running scripts from the same
    # directory that libcef.so resides in when you put "./" in here.
    # runtime_library_dirs=[
    #    './'
    #],

    # /EHsc - using STL string, multimap and others that use C++ exceptions.
    extra_compile_args=[],

    # '/ignore:4217' - silence warnings: "locally defined symbol _V8FunctionHandler_Execute
    #                  imported in function "public: virtual bool __thiscall V8FunctionHandler::Execute".
    #                  client_handler or other vcprojects include setup/cefpython.h,
    #                  this is a list of functions with "public" statement that is
    #                  accessible from c++.
    extra_link_args=[],

    # Defining macros:
    # define_macros = [("UNICODE","1"), ("_UNICODE","1"), ]
)]

setup(
    name = 'cefpython_py%s' % PYTHON_VERSION,
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)