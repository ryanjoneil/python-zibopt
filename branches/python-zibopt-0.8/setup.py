from Cython.Distutils import build_ext
from setuptools import setup, find_packages, Extension

def zibopt_ext(name):
    # ZIBopt headers and shared objects will must be in the user's
    # C_INCLUDE_PATH and LIBRARY_PATH, respectively.
    return Extension('zibopt.%s' % name, 
        sources = ['src/zibopt/%s.pyx' % name], 
        libraries = ['zibopt']
    )

setup (
    name         = 'python-zibopt',
    version      = '0.8.0',
    description  = 'ZIB Optimization Suite interface for python',
    author       = "Ryan J. O'Neil",
    author_email = 'ryanjoneil@gmail.com',
    url          = 'http://code.google.com/p/python-zibopt/',
    download_url = 'http://code.google.com/p/python-zibopt/downloads/list',

    package_dir = {'': 'src'},
    packages    = find_packages('src', exclude=['tests', 'tests.*']),
    test_suite  = 'tests',

    cmdclass = {'build_ext': build_ext},
    ext_modules = [
        zibopt_ext('error'),
        zibopt_ext('expression'),
        zibopt_ext('scip'),
        zibopt_ext('variable')
    ],  

    keywords    = 'mixed binary integer programming optimization zib zibopt',
    classifiers = [
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering :: Mathematics'
    ]    
)

