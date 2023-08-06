#!/usr/bin/env python3
from distutils.core import setup, Extension
from distutils.util import get_platform

ext_modules = [ Extension('leakless._autofd', ['src/autofd.c']) ]
if get_platform().startswith('linux'):
  ext_modules.append(Extension(
    'leakless._subreaper',
    sources=['src/subreaper_module.c'],
    extra_objects=['src/subreaper_asm.S']
  ))

setup(
  name = 'leakless',
  version = '0.05',
  description = 'Leakless helps you avoid leaking UNIX file descriptors and child processes.',
  url = 'https://github.com/percontation/leakless',
  package_dir = {'leakless': 'src'},
  packages = ['leakless'],
  python_requires = ">=3.5",
  ext_modules = ext_modules,
  classifiers = [
     'Development Status :: 3 - Alpha',
     'License :: OSI Approved :: ISC License (ISCL)',
     'Programming Language :: Python :: 3',
     'Operating System :: POSIX',
     'Operating System :: POSIX :: Linux',
  ],
)
