from setuptools import setup, find_packages
from os import path


# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

if path.exists("requirements.txt"):
    with open(path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
        install_requires = f.read().split('\n')
else:
    install_requires = []

setup(
    name='mwtools',
    version='0.0.4',
    author='xuwei',
    license='MIT Liense',
    author_email='microwood.xyz@gmail.com',
    description='microwood python tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/microwood/mwtools',
    packages=find_packages(),
    install_requires=install_requires
)
