from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='reelib',
    packages=find_packages(),

    version='1.1.0',

    license='MIT',

    install_requires=[],

    author='reeve0930',
    author_email='reeve0930@gmail.com',

    url='https://github.com/reeve0930/reelib',

    description='頻繁に利用する処理を集めたライブラリ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='reelib', 

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6'
    ],
)