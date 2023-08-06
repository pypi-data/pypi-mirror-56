from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.txt'), encoding='utf-8') as f:
    long_description = f.read()

setup(
      name='pco',
      packages=['pco'],
      version='0.0.15',
      license='MIT',

      description='This class provides basic methods for using pco cameras.',
      long_description=long_description,

      author='Andreas Ziegler',
      author_email='andreas.ziegler@pco.de',
      url='https://www.pco.de/',

      keywords=[
          'pco',
          'camera'
      ],

      install_requires=[
          'numpy'
      ],
      package_data={
          'pco': [
              'LICENSE.txt'
          ]
      },
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Microsoft :: Windows'
      ]
)
