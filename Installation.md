# Building & Installing python-zibopt #

_The following instructions assume you are building against Python 3.2.  To build against Python 2.7, simply leave off the 3s from all the packages and commands._

## Prerequisites ##

This documentation was written with Ubuntu in mind, so you may need to translate the commands to your platform, but the procedure should be the same.  Before we can build python-zibopt, we need shared object libraries for SoPlex and SCIP as well as setuptools for Python 3.2:

```
sudo apt-get install build-essential python3 python3-dev python3-setuptools
easy_install3 python-algebraic
```

We'll assume you have a directory named src in your home for building things, and one named lib for putting the ZIBopt .so file in:

```
mkdir ~/src
mkdir ~/lib
```

Download the latest version of [ZIBopt](http://zibopt.zib.de/download.shtml) and the latest version of [python-zibopt](http://code.google.com/p/python-zibopt/downloads/list) to the src directory referenced above.  Uncompress and build SoPlex and SCIP, then copy their .so files to your lib:

```
cd ~/src
tar xvfz ziboptsuite-2.1.1.tgz
cd ziboptsuite-2.1.1/
```

Build the ZIBopt .so file:

```
make ziboptlib SHARED=true ZIMPL=false ZLIB=false READLINE=false
```

Copy the ZIBopt .so file to your ~/lib directory and create a symbolic link to their latest version (your file names may be slightly different):

```
cp lib/libzibopt-2.1.1.linux.x86_64.gnu.opt.so ~/lib/
ln -s ~/lib/libzibopt-2.1.1.linux.x86_64.gnu.opt.so ~/lib/libzibopt.so
```

## Building python-zibopt ##

In order to build and use python-zibopt, we need to reference the C header files and .so files for ZIBopt in our environment.  Once it is built, you'll need to keep the LD\_LIBRARY\_PATH set, possibly in your .bashrc, in order to use it:

```
export LD_LIBRARY_PATH=$HOME/lib
export LIBRARY_PATH=$HOME/lib
export C_INCLUDE_PATH=~/src/ziboptsuite-2.1.1/scip-2.1.1/src/
```

Now we build python-zibopt:

```
cd ~/src
tar xvfz python-zibopt-0.7.1.dev-r202.tar.gz 
cd python-zibopt-0.7.1.dev-r202/
python3 setup.py build
```

Test the library to make sure it is in working order:

```
python3 setup.py test
```

You should see output to the effect of:

```
running test
running egg_info
[... snip ...]
Tests nonlinear objective maximization ... ok
testSimpleLP (tests.lp.LPInterfaceTest) ... ok

----------------------------------------------------------------------
Ran 47 tests in 0.547s

OK
```

And finally install it:

```
sudo python3 setup.py install 
```

## Verifying Your Installation ##

You should now be able to do this without getting any errors:

```
python3
Python 3.2 (r32:88445, Mar 25 2011, 19:56:22) 
[GCC 4.5.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.

>>> import zibopt
>>> zibopt.__version__
'0.7.1'
>>> zibopt.scip.solver()
<zibopt.scip.solver object at 0xb7d28cd4>
>>> exit()
 
python3 examples/sudoku.py 
[3, 1, 8, 6, 9, 2, 7, 4, 5]
[7, 6, 4, 3, 5, 1, 8, 9, 2]
[2, 9, 5, 8, 7, 4, 3, 1, 6]
[6, 2, 9, 5, 1, 7, 4, 8, 3]
[1, 4, 7, 2, 8, 3, 5, 6, 9]
[8, 5, 3, 4, 6, 9, 1, 2, 7]
[5, 7, 2, 1, 4, 6, 9, 3, 8]
[4, 8, 6, 9, 3, 5, 2, 7, 1]
[9, 3, 1, 7, 2, 8, 6, 5, 4]
```