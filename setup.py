#!/usr/bin/env python

# 
# Copyright (c) 2020 Fernando Pelliccioni
# 

import atexit
from setuptools import setup
from setuptools.command.install import install


__title__ = "kthbuild"
__summary__ = "Knuth node build tools"
__uri__ = "https://github.com/k-nuth/kthbuild"
__version__ = "0.0.25"
__author__ = "Fernando Pelliccioni"
__email__ = "fpelliccioni@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2020 Fernando Pelliccioni"


install_requires = [
    "conan >= 1.21.1",
    "cpuid >= 0.0.9",
]


def exec_conan_user(default=None):
    try:
        # res = subprocess.Popen(["conan", "user"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res = subprocess.Popen(["conan", "remote", "add", "kth", "https://api.bintray.com/conan/k-nuth/kth"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output, _ = res.communicate()
        print('fer 0')

        if output:
            print('fer 0.1')
            if res.returncode == 0:
                ret = output.decode("utf-8").replace('\n', '').replace('\r', '')
                return ret
        return default
    except OSError: # as e:
        print('fer 1')
        return default
    except:
        print('fer 2')
        return default

# class PostDevelopCommand(develop):
#     """Post-installation for development mode."""
#     def run(self):
#         print('********** PostDevelopCommand **********')
#         exec_conan_user()
#         print('********** PostDevelopCommand **********')
#         develop.run(self)

# class PostInstallCommand(install):
#     """Post-installation for installation mode."""
#     def run(self):
#         print('********** PostInstallCommand **********')
#         exec_conan_user()
#         print('********** PostInstallCommand **********')
#         install.run(self)


def _post_install():
    exec_conan_user()
    print('POST INSTALL')


class new_install(install):
    def __init__(self, *args, **kwargs):
        super(new_install, self).__init__(*args, **kwargs)
        atexit.register(_post_install)




setup(
    name = __title__,
    version = __version__,
    description = __summary__,
    long_description=open("./README.rst").read(),
    license = __license__,
    url = __uri__,
    author = __author__,
    author_email = __email__,

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],    

    # What does your project relate to?
    keywords='knuth kth crypto bitcoin btc bch cash build tool',

    py_modules=["kthbuild"],

    install_requires=install_requires,
    # setup_requires=setup_requires,
    

    dependency_links=[
        'https://testpypi.python.org/pypi',
        # 'https://testpypi.python.org/pypi/cpuid-native/',
    ],

    # cmdclass={
    #     'develop': PostDevelopCommand,
    #     'install': PostInstallCommand,
    # },

    cmdclass={'install': new_install},

    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },
)

