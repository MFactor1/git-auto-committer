import py_compile

py_compile.compile('src/gaccli.py', cfile='src/gaccli.pyc')
py_compile.compile('src/gaccmd.py', cfile='src/gaccmd.pyc')
py_compile.compile('src/gacmain.py', cfile='src/gacmain.pyc')
py_compile.compile('src/gacworker.py', cfile='src/gacworker.pyc')
