#! env python3
"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
# Always prefer setuptools over distutils
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ttc',  # Required
    version=os.getenv("pkg_version", "0.0.0"),  # Required
    description='TremTec CLI utilities',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://gitlab.com/tremtec/ttc',  # Optional
    author='TremTec Org.',  # Optional
    author_email='marco@tremtec.com',  # Optional
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='tremtec cli',  # Optional
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    install_requires=[
        'click',
        'click-completion',
        'PyInquirer',
    ],  # Optional
    extras_require={  # Optional
        'dev': [
            # linters
            'flake8',
            'black',
            'pylint',
            'pydocstyle',
            'pycodestyle',
            # extra
            'rope',  # refactoring in vscode
        ],
        'test': [
            'coverage'
        ],
    },
    entry_points={  # Optional
        'console_scripts': [
            'ttc=ttc.main:main',
            'tt=ttc.main:main',
        ],
    },
)
