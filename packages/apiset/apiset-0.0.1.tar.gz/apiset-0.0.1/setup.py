import re
from pathlib import Path

from setuptools import find_packages, setup


PACKAGE = 'apiset'
PACKAGE_DIR = Path(__file__).parent / PACKAGE


def read(f):
    path = Path(__file__).parent / f
    if not path.exists():
        return ''
    return path.read_text(encoding='latin1').strip()


def get_version():
    text = read(PACKAGE_DIR / 'version.py')
    if not text:
        text = read(PACKAGE_DIR / '__init__.py')
    try:
        return re.findall(r"^__version__ = '([^']+)'$", text, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


setup(
    name=PACKAGE,
    version=get_version(),
    description='Utils for OpenAPI and Swagger',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP'],
    author='Alexander Malev',
    author_email='malev@somedev.ru',
    url='https://github.com/aioworkers/apiset/',
    license='Apache 2',
    packages=find_packages(include=[PACKAGE, PACKAGE + '.*']),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'pyyaml',
    ],
    extras_require={
        'apistar': ['apistar'],
    },
)
