import os
import re
from setuptools import setup, find_packages


RE_PY_VERSION = re.compile(
    r'__version__\s*=\s*["\']'
    r'(?P<version>\d+(\.\d+(\.\d+)?)?)'
    r'["\']'
)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def read_version():
    content = read('src/apiref/__init__.py')
    m = RE_PY_VERSION.search(content)
    if not m:
        return '0.0'
    else:
        return m.group('version')


setup(
    name="apiref",
    version=read_version(),
    author="Mateusz Klos",
    author_email="novopl@gmail.com",
    license="Apache 2.0",
    keywords="library",
    url="https://github.com/novopl/apiref",
    description="library",
    long_description=read('README.rst'),
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        "apispec>=3.1.0",
        "flask>=1.0.2",
        "marshmallow>=3.2.2",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Typing :: Typed",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
)
