import setuptools
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(

     name='pycartool',

     version='0.0.6',

     author="Victor Férat",

     author_email="victor.ferat@live.fr",

     description="A simple open source Python package for I/O between Cartool"
                 " and MNE ( and more generally python)",

     long_description=long_description,

     long_description_content_type="text/markdown",

     url="https://github.com/vferat/PyCartool",

     license="BSD-3-Clause",

     python_requires='>=3.6',

     install_requires=["mne", "numpy"],

     packages=setuptools.find_packages(exclude=['docs', 'tests']),

     classifiers=[

        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
 )
