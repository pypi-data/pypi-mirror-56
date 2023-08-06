#!/usr/bin/env python
from __future__ import print_function
#
# Based on: xcsoar

from sys import platform
from setuptools import setup
from setuptools.command.install import install
from distutils.command.build import build
from subprocess import call
from multiprocessing import cpu_count

import glob
import codecs
import os
import pycudd
import shutil


BASEPATH = os.path.dirname(os.path.abspath(__file__))
CUDD_PATH = os.path.join(BASEPATH, 'cudd-3.0.0')
PYCUDD_PATH = os.path.join(BASEPATH, 'pycudd')
CUDD_CONFIGURE_OPTS = ['--enable-shared', '--enable-dddmp', '--enable-obj',
                       '\'CFLAGS=-std=c99\'']


# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


class PyCuddBuild(build):
    def linux_prepare_so_files(self):
        print('BuildCudd: linux_prepare_so_files')
        install_path = os.path.join(CUDD_PATH, 'cudd', '.libs')
        lib_search = os.path.join(install_path, '*.so')
        target_dir = CUDD_PATH
        for filename in glob.glob(lib_search):
            shutil.copy(filename, target_dir)
            print(filename)

    def build_swig_package(self):
        print('BuildCudd: build_swig_package')
        build_status = call(['make'], shell=True, cwd=PYCUDD_PATH)

    def sanity_test_package(self):
        print('TODO')
        pass

    def windows_prepare_so_files(self):
        raise NotImplementedError('Windows not yet supported')

    def osx_prepare_so_files(self):
        raise NotImplementedError('OS X not yet supported')

    def run(self):
        # run original build code
        build.run(self)

        # build PyCudd
        build_path = os.path.abspath(self.build_temp)

        configure_cmd = ['./configure {}'.format(' '.join(CUDD_CONFIGURE_OPTS))]
        make_cmd = [
            'make',
            #'OUT=' + build_path,
            #'V=' + str(self.verbose),
        ]

        try:
            make_cmd.append('-j%d' % cpu_count())
        except NotImplementedError:
            print('Unable to determine number of CPUs. Using single threaded make.')

        targets = [] #'']
        make_cmd.extend(targets)

        target_files = [os.path.join(build_path, 'bin', 'cudd.so')]

        def compile():
            call(configure_cmd, cwd=CUDD_PATH, shell=True)
            call(make_cmd, cwd=CUDD_PATH)

        self.execute(compile, [], 'Compiling cudd')

        # copy resulting tool to library build folder
        self.mkpath(self.build_lib)

        if not self.dry_run:
            #for target in target_files:
                #self.copy_file(target, self.build_lib)
            # now install the libso or DLL files into the pycudd path
            if platform.startswith('win32') or platform.startswith('cygwin'):
                self.windows_prepare_so_files()
            elif platform.startswith('darwin'):
                self.osx_prepare_so_files()
            elif platform.startswith('linux'):
                self.linux_prepare_so_files()
            else:
                raise Exception('Unsupported platform: {}'.format(platform))

        # Once the files have been copied, run swig
        self.build_swig_package()
        self.sanity_test_package()



class PyCuddInstall(install):
    def initialize_options(self):
        install.initialize_options(self)
        self.build_scripts = None

    def finalize_options(self):
        install.finalize_options(self)
        self.set_undefined_options('build', ('build_scripts', 'build_scripts'))

    def run(self):
        # run original install code
        install.run(self)

        # install PyCudd executables
        self.copy_tree(self.build_lib, self.install_lib)


setup(
    name='pycudd',

    # Treat the prior releases of PyCUDD as v1.0.x. The new packaged libraries
    # will be versions 1.1.x+
    version=pycudd.__version__,
    description='PyCudd',
    long_description=long_description,

    maintainer='Alexander Feldman',
    maintainer_email='alex@llama.gs',

    # The project's main homepage.
    url='https://github.com/pycudd/pycudd',

    # Author details
    author='PyCUDD Community',
    author_email='noreply@github.com',

    # Choose your license
    license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
    ],

    cmdclass={
        'build': PyCuddBuild,
        'install': PyCuddInstall,
    }
)
