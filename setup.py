# Dodo setup.py script
#
# It doesn't depend on setuptools, but if setuptools is available it'll use
# some of its features, like package dependencies.

from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES
import os
import sys


class OsxInstallData(install_data):
    # On MacOS, the platform-specific lib dir is /System/Library/Framework/Python/.../
    # which is wrong. Python 2.5 supplied with MacOS 10.5 has an Apple-specific fix
    # for this in distutils.command.install_data#306. It fixes install_lib but not
    # install_data, which is why we roll our own install_data class.

    def finalize_options(self):
        # By the time finalize_options is called, install.install_lib is set to the
        # fixed directory, so we set the installdir to install_lib. The
        # install_data class uses ('install_data', 'install_dir') instead.
        self.set_undefined_options('install', ('install_lib', 'install_dir'))
        install_data.finalize_options(self)


if sys.platform == "darwin":
    cmdclasses = {'install_data': OsxInstallData}
else:
    cmdclasses = {'install_data': install_data}


def full_split(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return full_split(head, [tail] + result)

# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in list(INSTALL_SCHEMES.values()):
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)


def is_not_module(filename):
    return os.path.splitext(filename)[1] not in ['.py', '.pyc', '.pyo']

scripts = ['dodo', 'dodo.py']


setup_args = {
    'name': 'dodopie',
    'version': '0.99',
    'url': 'http://atmb4u.github.io/dodo',
    'description': 'Task Management for Hackers',
    'author': 'Anoop Thomas Mathew',
    'author_email': 'atmb4u@gmail.com',
    'license': 'BSD',
    'packages': packages,
    'cmdclass': cmdclasses,
    'data_files': data_files,
    'scripts': scripts,
    'include_package_data': True,
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
setup(**setup_args)
