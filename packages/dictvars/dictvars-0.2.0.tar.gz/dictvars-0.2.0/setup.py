import re
from os import path
from io import open
from pathlib import Path

from setuptools import setup


mainpkg = 'dictvars'
here = path.abspath(path.dirname(__file__))


def read_file(fname):
    with open(path.join(here, str(fname)), encoding='utf-8') as f:
        return f.read()


def read_version():
    content = read_file(Path(mainpkg) / '__init__.py')
    return re.search(r"__version__ = '([^']+)'", content).group(1)


setup(
        name=mainpkg,
        version=read_version(),
        description='Create dicts from variables in scope',
        long_description=read_file('README.md'),
        long_description_content_type='text/markdown',
        author='Fabiano Engler',
        author_email='fabianoengler@gmail.com',
        url='https://github.com/fabianoengler/dictvars',
        packages=[mainpkg],
        zip_safe=True,
        classifiers=[
                'Development Status :: 5 - Production/Stable',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: BSD License',
                'Natural Language :: English',
                'Operating System :: OS Independent',
                'Topic :: Software Development :: Libraries',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.5',
                'Programming Language :: Python :: 3.6',
                'Programming Language :: Python :: 3.7',
                'Programming Language :: Python :: 3.8',
                ],
        python_requires='>=3.5',
        )
