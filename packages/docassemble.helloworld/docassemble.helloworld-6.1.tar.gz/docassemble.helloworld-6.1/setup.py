import os
import sys
from setuptools import setup, find_packages
from fnmatch import fnmatchcase
from distutils.util import convert_path

standard_exclude = ('*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')
def find_package_data(where='.', package='', exclude=standard_exclude, exclude_directories=standard_exclude_directories):
    out = {}
    stack = [(convert_path(where), '', package)]
    while stack:
        where, prefix, package = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                        stack.append((fn, '', new_package))
                else:
                    stack.append((fn, prefix + name + '/', package))
            else:
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out

setup(name='docassemble.helloworld',
      version='6.1',
      description=('A æøå docassemble extension.'),
      long_description="# docassemble.helloworld\r\n\r\nA primitive docassemble extension that does mailing.  æøå foo foo\r\n\r\n## Mailing feature\r\n\r\nTo send an e-mail, write send_email().\r\n\r\nIf you don't want to send an e-mail, don't send it.  Really.  I mean it.  \r\nActually I don't.  Or do I?\r\n\r\n## Author\r\n\r\nSystem Administrator, jpyle@docassemble.orgafasdfadsfasfasf\r\n\r\n",
      long_description_content_type='text/markdown',
      author='System Administrator',
      author_email='jpyle@docassemble.org',
      license='The MIT License (MIT)',
      url='https://docassemble.org',
      packages=find_packages(),
      namespace_packages=['docassemble'],
      install_requires=['airtable-python-wrapper'],
      zip_safe=False,
      package_data=find_package_data(where='docassemble/helloworld/', package='docassemble.helloworld'),
     )

