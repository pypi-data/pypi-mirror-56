from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
import sys
import setuptools
import os

__version__ = '0.0.2'

# Read contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Grabs all cppFiles in a folder
def getCppFiles(folders):
    files = []

    for folder in folders:
        for file in os.listdir(folder):
            if file.endswith('.cpp'):
                files.append(folder + '/' + file) 
    return files

# Find pybind11 header files
class get_pybind_include(object):
    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)

ext_modules = [
    Extension(
        '_matrix_hal_nfc',
        sources=getCppFiles([
            'hal_nfc_wrapper',
            'hal_nfc_wrapper/ndef_types',
            'hal_nfc_wrapper/writer',
            'hal_nfc_wrapper/reader',
            'hal_nfc_wrapper/reader/read_values'
        ]),
        include_dirs=[
            get_pybind_include(),
            get_pybind_include(user=True),
            '/usr/local/include/matrix_nfc/nxp_nfc/NxpNfcRdLib/intfs',
            '/usr/local/include/matrix_nfc/nxp_nfc/NxpNfcRdLib/types',
        ],
        libraries=['matrix_hal_nfc'],
        extra_compile_args=[
            '-DNXPBUILD__PH_RASPBERRY_PI',
            '-O3',
        ],
        language='c++'
    ),
]

class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {'unix': [],}
    l_opts = {'unix': [],}

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        link_opts = self.l_opts.get(ct, [])

        # fix extra_compile_args being ignored
        for arg in ext_modules[0].extra_compile_args: 
            opts.append(arg)     

        opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
        opts.append('-std=c++11')

        for ext in self.extensions:
            ext.extra_compile_args = opts
            ext.extra_link_args = link_opts

        build_ext.build_extensions(self)

setup(
    name='matrix_lite_nfc',
    version=__version__,
    author='MATRIX',
    author_email='devel@matrixlabs.ai',
    packages=find_packages(),
    url='https://github.com/matrix-io/matrix-lite-nfc-py',
    description='A Python wrapper for MATRIX HAL NFC',
    long_description=long_description,
    long_description_content_type='text/markdown',
    ext_modules=ext_modules,
    install_requires=['pybind11>=2.4'],
    setup_requires=['pybind11>=2.4'],
    cmdclass={'build_ext': BuildExt},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
    ],
)