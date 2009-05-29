from setuptools import setup, find_packages, Extension

def zibopt_ext(name, c_file):
    return Extension('zibopt.%s' % name, 
        sources = ['src/ext/%s' % c_file], 
        library_dirs = ['../../lib'], # TODO: fix this
        include_dirs = ['../ziboptsuite-1.1.0/scip-1.1.0/src/'], # TODO: fix this
        libraries = [
            'lpispx', 'objscip', 'scip', 'soplex', 'zimpl',
        	'readline', 'ncurses', 'gmp', 'z'
        ],
    )

setup (
    name         = 'python-zibopt',
    version      = '0.1',
    description  = 'ZIB Optimization Suite interface for python',
    author       = "Ryan J. O'Neil",
    author_email = 'ryan@chenoneil.com',
    url          = 'http://code.google.com/p/python-zibopt/',
    download_url = 'http://code.google.com/p/python-zibopt/downloads/list',

    package_dir = {'': 'src'},
    packages    = find_packages('src', exclude=['tests', 'tests.*']),
    zip_safe    = True,
    test_suite  = 'tests',

    ext_modules  = [
        zibopt_ext('_scip', 'scipmodule.c'),
        zibopt_ext('_vars', 'varsmodule.c'),
        zibopt_ext('_cons', 'consmodule.c'),
        zibopt_ext('_soln', 'solnmodule.c'),
    ],

    keywords    = 'mixed binary integer programming optimization zib zibopt',
    classifiers = [
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Topic :: Scientific/Engineering :: Mathematics',
    ]    
)

