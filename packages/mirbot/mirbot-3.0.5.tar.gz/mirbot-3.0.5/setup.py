from setuptools import setup

with open('README.md') as f:
  long_description = f.read()

setup(
  name='mirbot',
  version='3.0.5',
  description='Modular Information Retrieval Bot (MIRbot)',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/PyratLabs/MIRbot',
  author='PyratLabs',
  author_email='xan@manning.io',
  license='MIT',
  packages=['mirbot'],
  scripts=['bin/mirbot'],
  install_requires=['python-daemon'],
  test_suite='nose.collector',
  tests_require=['nose'],
  classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
  ],
  zip_safe=False
)
