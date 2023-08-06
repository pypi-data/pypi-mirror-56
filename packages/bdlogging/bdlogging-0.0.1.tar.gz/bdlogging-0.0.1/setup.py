from setuptools import setup
import pathlib

_ROOT = pathlib.Path(__file__).parent

with open(str(_ROOT / 'bdlogging' / '__init__.py')) as f:
    for line in f:
        if line.startswith('__version__ ='):
            _, _, version = line.partition('=')
            VERSION = version.strip(" \n'\"")
            break
        else:
            raise RuntimeError(
                'unable to read the version from bdlogging/__init__.py')


requires = ["pika"]
setup(
    name='bdlogging',
    version=VERSION,
    description='RabbitMQログ出力モジュール',
    url='https://gitlab.com/belldata/logging.git',
    author='nozomi.nishinohara',
    author_email='nozomi.nishinohara@belldata.co.jp',
    # license='Apache License, Version 2.0',
    keywords='',
    packages=[
        "bdlogging"
    ],
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
