from os import path
from setuptools import setup
# Tensorflow is provided by two packages, tensorflow and tensorflow-gpu.
# This check will check if something is already installed: if that is the case,
# it will just require a given version, otherwise it will require the CPU
# only version.
from pkg_resources import DistributionNotFound, get_distribution

try:
    get_distribution('tensorflow-gpu')
    tf_name = 'tensorflow-gpu>=2.0'
except DistributionNotFound:
    tf_name = 'tensorflow>=2.0'

# Read the contents of the README file
directory = path.abspath(path.dirname(__file__))
with open(path.join(directory, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='cnn2snn',
      version='1.7.0',
      description='Keras to Akida CNN Converter',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Alvaro Moran',
      author_email='amoran@brainchip.com',
      url='https://www.akidalab.com',
      license='Apache 2.0',
      packages=['cnn2snn'],
      install_requires=['akida', 'numpy', tf_name],
     )
