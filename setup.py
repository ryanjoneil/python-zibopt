from distutils.core import setup, Extension

scip = Extension('scip', 
    sources = ['src/scipmodule.c'], 
    library_dirs = ['../../lib'], # TODO: fix this
    include_dirs = ['../ziboptsuite-1.1.0/scip-1.1.0/src/'], # TODO: fix this
    libraries = [
        'lpispx', 'objscip', 'scip', 'soplex', 'zimpl'
    	'readline', 'ncurses', 'gmp', 'z'
    ],
)

setup (
    name = 'zibopt',
    version = '0.1-alpha',
    description = 'ZIB Optimization Suite interface for python',
    ext_modules = [scip]
)

