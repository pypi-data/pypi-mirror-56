#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import setuptools

def main():
    setuptools.setup(
        name                 = 'gpudeets',
        version              = '2018.02.24.1606',
        description          = 'acquire and display GPU details',
        long_description     = long_description(),
        url                  = 'https://github.com/wdbm/spin',
        author               = 'Will Breaden Madden',
        author_email         = 'wbm@protonmail.ch',
        license              = 'GPLv3',
        packages             = setuptools.find_packages(),
        install_requires     = [
                               'docopt',
                               'pyprel',
                               'pandas==0.22.0',
                               'datavision',
                               'technicolor'
                               ],
        entry_points         = {
                               'console_scripts': ('displaygpudeets=gpudeets.__init__:main')
                               },
        include_package_data = True,
        zip_safe             = False
    )

def long_description(filename='README.md'):
    if os.path.isfile(os.path.expandvars(filename)):
      try:
          import pypandoc
          long_description = pypandoc.convert_file(filename, 'rst')
      except ImportError:
          long_description = open(filename).read()
    else:
        long_description = ''
    return long_description

if __name__ == '__main__':
    main()
