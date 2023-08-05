#!/usr/bin/env python
"""# Environment Modules

The Environment Modules package provides for the dynamic modification of a
user's environment via modulefiles.

* Upstream: https://modules.readthedocs.io/en/latest/
* Packaging: https://github.com/bukzor/environment-modules-setuptools
"""
# this really only works on linux systems, at the moment
from __future__ import print_function


from setuptools import setup
from setuptools.command.sdist import sdist as orig_sdist
from setuptools.command.install import install as orig_install
from distutils.core import Command
from distutils.command.build import build as orig_build


# ############# NOTES #####################
# setuptools.command.sdist.sdist

# setuptools/command/egg_info.py:egg_info.find_sources()
#   seems to be in charge of generating a file list
#   writes SOURCES.txt for its list
#   also reads MANIFEST.in; maybe this is the interface

# setuptools/command/sdist.py:add_defaults
#   adds various files to the file list based on the distribution object

# distutils/command/sdist.py:sdist.make_release_tree(base_dir, files)
#   copy files to base_dir. this will become the sdist

def system(cmd):
    from os import system
    from sys import stderr
    print(': %s' % cmd, file=stderr)
    if system(cmd) != 0:
        exit('command failed: %s' % cmd)


class build(orig_build):
    sub_commands = orig_build.sub_commands + [
        ('build_cexe', None),
    ]


class install(orig_install):
    sub_commands = orig_install.sub_commands + [
        ('install_cexe', None),
    ]


class sdist(orig_sdist):
    def run(self):
        self.run_command('fetch_sources')
        return orig_sdist.run(self)


class fetch_sources(Command):
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def run():
        system('./get_sources.sh')


class build_cexe(Command):
    build_temp = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        self.set_undefined_options('build', ('build_temp', 'build_temp'))

    def run(self):
        self.run_command('fetch_sources')
        system('./build.sh %s' % self.build_temp)


class install_cexe(Command):
    description = 'install C executables'
    outfiles = ()
    build_dir = install_dir = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        # this initializes attributes based on other commands' attributes
        self.set_undefined_options('build', ('build_temp', 'build_dir'))
        self.set_undefined_options(
            'install', ('install_data', 'install_dir'))

    def run(self):
        self.outfiles = self.copy_tree(self.build_dir, self.install_dir)

    def get_outputs(self):
        return self.outfiles


command_overrides = {
    'sdist': sdist,
    'fetch_sources': fetch_sources,
    'build': build,
    'build_cexe': build_cexe,
    'install': install,
    'install_cexe': install_cexe,
}


def wheel_support():
    class bdist_wheel(orig_bdist_wheel):
        def finalize_options(self):
            orig_bdist_wheel.finalize_options(self)
            # Mark us as not a pure python package
            self.root_is_pure = False

        def get_tag(self):
            python, abi, plat = orig_bdist_wheel.get_tag(self)
            # We don't contain any python source, nor any python extensions
            python, abi = 'py2.py3', 'none'
            return python, abi, plat

    command_overrides['bdist_wheel'] = bdist_wheel

try:
    from wheel.bdist_wheel import bdist_wheel as orig_bdist_wheel
except ImportError:
    pass
else:
    wheel_support()


import versions
if versions.version == 'master':
    version = '0'
else:
    version = versions.version
version += versions.suffix

setup(
    name='environment-modules',
    long_description=__doc__,
    long_description_content_type='text/markdown',
    version=version,
    cmdclass=command_overrides,
    platforms=['linux'],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: C',
        'Topic :: System',
        'Development Status :: 5 - Production/Stable',
    ],
)
