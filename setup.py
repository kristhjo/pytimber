#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ast
import six

import setuptools
from setuptools.command.install import install as _install

if six.PY2:
    from urllib import urlopen
else:
    from urllib.request import urlopen


# Repository URL for cmmnbuild_dep_manager
cmmnbuild_url = 'https://gitlab.cern.ch/scripting-tools/cmmnbuild-dep-manager/'


# Version number helper functions
def parse_init(file):
    '''Get __version__ code from file'''
    for line in file:
        if line.startswith('__version__'):
            return ast.literal_eval(line.split('=', 1)[1].strip())


def pytimber_version():
    '''Get pytimber version from local __init__.py'''
    init = os.path.join(os.path.dirname(__file__), 'pytimber', '__init__.py')
    with open(init, 'r') as file:
        return parse_init(file)


def cmmnbuild_version():
    '''Get cmmnbuild_dep_manager version from remote __init__.py'''
    init = cmmnbuild_url + 'raw/master/cmmnbuild_dep_manager/__init__.py'
    file = urlopen(init)
    return parse_init(file.read().decode('UTF-8').split('\n'))


# Custom install function
class install(_install):
    '''Install and perform the jar resolution'''
    user_options = _install.user_options + [
        ('no-jars', None, 'do not register with cmmnbuild_dep_manager')
    ]

    def initialize_options(self):
        self.no_jars = False
        _install.initialize_options(self)

    def run(self):
        if not self.no_jars:
            import cmmnbuild_dep_manager
            mgr = cmmnbuild_dep_manager.Manager()
            mgr.install('pytimber')
            print('registered pytimber with cmmnbuild_dep_manager')
        _install.run(self)


# Setup
setuptools.setup(
    name='pytimber',
    version=pytimber_version(),
    description='A Python wrapping of CALS API',
    author='Riccardo De Maria',
    author_email='riccardo.de.maria@cern.ch',
    url='https://github.com/rdemaria/pytimber',
    packages=['pytimber'],
    package_dir={
        'pytimber': 'pytimber'
    },
    setup_requires=[
        'cmmnbuild_dep_manager>=1.3.2'
    ],
    install_requires=[
        'JPype1>=0.6.1',
        'cmmnbuild_dep_manager>=1.3.2'
    ],
    dependency_links=[
        cmmnbuild_url + 'repository/archive.zip?ref=master#egg=cmmnbuild_dep_manager-' + cmmnbuild_version()
    ],
    cmdclass={
        'install': install
    }
)
