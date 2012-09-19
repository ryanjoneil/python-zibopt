from Cython.Distutils import build_ext
from setuptools import setup, find_packages, Extension

def scipopt_ext(name):
    # ZIBopt headers and shared objects will must be in the user's
    # C_INCLUDE_PATH and LIBRARY_PATH, respectively.
    return Extension('scipopt.%s' % name, 
        sources = ['src/scipopt/%s.pyx' % name], 
        libraries = ['scipopt']
    )

setup (
    name         = 'python-scipopt',
    version      = '1.0.0',
    description  = 'SCIP Optimization Suite interface for python',
    author       = "Ryan J. O'Neil",
    author_email = 'ryanjoneil@gmail.com',
    url          = 'http://code.google.com/p/python-scipopt/',
    download_url = 'http://code.google.com/p/python-scipopt/downloads/list',

    package_dir = {'': 'src'},
    packages    = find_packages('src', exclude=['tests', 'tests.*']),
    test_suite  = 'tests',

    cmdclass = {'build_ext': build_ext},
    ext_modules = [
        scipopt_ext('lpi'),
        scipopt_ext('message'),
        scipopt_ext('scip'),
    ],  

    keywords    = 'mixed binary integer programming optimization scib scipopt',
    classifiers = [
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering :: Mathematics'
    ]    
)
