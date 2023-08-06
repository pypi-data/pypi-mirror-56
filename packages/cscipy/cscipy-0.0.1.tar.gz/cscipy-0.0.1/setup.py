from setuptools import setup, Extension
from codecs import open
import sys
import os
import numpy


def is_platform_mac():
    return sys.platform == 'darwin'


def is_platform_windows():
    return sys.platform == 'win32' or sys.platform == 'cygwin'


try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True

if use_cython:
    sourcefiles = ['cscipy/distance.pyx']
else:
    sourcefiles = ['cscipy/distance.cpp']

# Fix compatibility when compiling on Mac Mojave.
# Explanation: https://github.com/pandas-dev/pandas/issues/23424#issuecomment-446393981
# Code credit: https://github.com/pandas-dev/pandas/pull/24274/commits/256faf2011a12424e684a42c147e1ba7ac32c6fb
if is_platform_mac():
    import _osx_support
    import distutils.sysconfig

    if not 'MACOSX_DEPLOYMENT_TARGET' in os.environ:
        current_system = list(map(int, _osx_support._get_system_version().split('.')))
        python_osx_target_str = distutils.sysconfig.get_config_var('MACOSX_DEPLOYMENT_TARGET')
        python_osx_target = list(map(int, python_osx_target_str.split('.')))
        if python_osx_target < [10, 9] <= current_system:
            os.environ['MACOSX_DEPLOYMENT_TARGET'] = '10.9'

if is_platform_windows():
    extra_compiler_args = []
else:
    extra_compiler_args = [
        '-std=c++11',
        '-Wno-sign-compare',
        '-Wno-incompatible-pointer-types',
        '-Wno-unused-variable',
        '-Wno-absolute-value',
        '-Wno-visibility',
        '-Wno-#warnings',
    ]

ext_modules = [
    Extension('cscipy.distance',
              sourcefiles,
              language='c++',
              include_dirs=[numpy.get_include()],
              extra_compile_args=extra_compiler_args,
              ),
]

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup_args = dict(
    name='cscipy',
    ext_modules=ext_modules,
    license='MIT',
    packages=['cscipy'],
    version='0.0.1',
    author=['Yukio Fukuzawa'],
    description='Some scipy functions rewritten in Cython',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fzyukio/cscipy',
    keywords=['scipy', 'cython', 'distance'],
    install_requires=['Cython', 'numpy'],
)

if use_cython:
    setup_args['cmdclass'] = {'build_ext': build_ext}

setup(
    **setup_args
)
