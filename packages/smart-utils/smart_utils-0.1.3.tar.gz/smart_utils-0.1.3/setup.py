from setuptools import setup, find_packages
from os import path
from smart_utils import __version__

setup(
        name='smart_utils',
        version=__version__,
        description='Utils module',
        long_description='This repository has a library of tools to facilitate development in all smart-development',
        url="https://github.com/smart-protection/smart_python_utils",
        author='jc_diaz',
        author_email='juancarlos.diaz@smartprotection.com',

        license='MIT',

        # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
        classifiers=[
            'Development Status :: 4 - Beta',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: MIT License',

            'Operating System :: OS Independent',

            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
        ],

        keywords='sample setup',
        packages=find_packages(),
        install_requires=["boto3>=1.9", "PyYAML==5.1.2", "sentry-sdk>=0.12"]
)
