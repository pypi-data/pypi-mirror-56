#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.edit',
  description = 'Convenience functions for editing things. - Cameron Simpson <cs@cskk.id.au> 02jun2016',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20191201.1',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  include_package_data = True,
  install_requires = ['cs.pfx'],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description = '*Latest release 20191201.1*:\nInitial PyPI release: assorted functions for invoking editors on strings.\n\nConvenience functions for editing things.\n- Cameron Simpson <cs@cskk.id.au> 02jun2016\n\n## Function `choose_editor(editor=None, environ=None)`\n\nChoose an editor.\n\n## Function `edit(lines, editor=None, environ=None)`\n\nWrite lines to a temporary file, edit the file, return the new lines.\n\n## Function `edit_strings(strs, editor=None, environ=None)`\n\nEdit a list of string, return tuples of changed string pairs.\nHonours $EDITOR envvar, defaults to "vi".\n\n\n\n# Release Log\n\n*Release 20191201.1*:\nInitial PyPI release: assorted functions for invoking editors on strings.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.edit'],
)
