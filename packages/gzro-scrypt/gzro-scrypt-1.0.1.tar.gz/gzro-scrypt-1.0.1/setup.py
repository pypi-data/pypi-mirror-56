from setuptools import setup, Extension

gravity_scrypt_module = Extension('scrypt',
                               sources = ['scrypt/scryptmodule.c',
                                          'scrypt/scrypt.c'],
                               include_dirs=['scrypt/'])

setup (
    name = 'gzro-scrypt',
    version = '1.0.1',
    description = 'Bindings for scrypt proof of work used by Gravity',
    classifiers=[
        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    ext_modules = [gravity_scrypt_module]
)
