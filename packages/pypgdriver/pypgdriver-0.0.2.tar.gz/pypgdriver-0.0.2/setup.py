from setuptools import setup
import pathlib

_ROOT = pathlib.Path(__file__).parent

with open(str(_ROOT / 'pypgdriver' / '__init__.py')) as f:
    for line in f:
        if line.startswith('__version__ ='):
            _, _, version = line.partition('=')
            VERSION = version.strip(" \n'\"")
            break
        else:
            raise RuntimeError(
                'unable to read the version from pypgdriver/__init__.py')


requires = ["psycopg2>=2.8.3", "asyncio>=3.4.3", "tornado>=6.0.3"]
setup(
    name='pypgdriver',
    version=VERSION,
    description='postgresql接続ドライバー',
    url='https://gitlab.com/Nozomi0720/pypg-driver.git',
    author='nozomi.nishinohara',
    author_email='nozomi.nishinohara@belldata.co.jp',
    # license='Apache License, Version 2.0',
    keywords='',
    packages=[
        "pypgdriver"
    ],
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
