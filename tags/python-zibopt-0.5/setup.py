from setuptools import setup, find_packages, Extension

def zibopt_ext(name, c_file):
    # ZIBOpt headers and shared objects will must be in the user's
    # C_INCLUDE_PATH and LIBRARY_PATH, respectively.
    return Extension('zibopt.%s' % name, 
        sources = ['src/ext/%s' % c_file], 
        libraries = [
            'lpispx', 'objscip', 'scip', 'soplex', 'readline'
        ],
    )

setup (
    name         = 'python-zibopt',
    version      = '0.5',
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
        # Modules to setup and solve optimization problems
        zibopt_ext('_scip', 'scipmodule.c'),
        zibopt_ext('_vars', 'varsmodule.c'),
        zibopt_ext('_cons', 'consmodule.c'),
        zibopt_ext('_soln', 'solnmodule.c'),
        
        # Modules to adjust priority and settings
        zibopt_ext('_branch',   'branchmodule.c'),
        zibopt_ext('_conflict', 'conflictmodule.c'),
        zibopt_ext('_heur',     'heuristicmodule.c'),
        zibopt_ext('_nodesel',  'nodeselectormodule.c'),
        zibopt_ext('_presol',   'presolvermodule.c'),
        zibopt_ext('_prop',     'propagatormodule.c'),
        zibopt_ext('_sepa',     'separatormodule.c'),
    ],

    keywords    = 'mixed binary integer programming optimization zib zibopt',
    classifiers = [
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Topic :: Scientific/Engineering :: Mathematics',
    ]    
)

