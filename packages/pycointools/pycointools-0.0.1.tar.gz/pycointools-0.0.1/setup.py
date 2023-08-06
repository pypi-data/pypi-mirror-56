#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    # name="waykichain",
    name="pycointools",
    version="0.0.1",
    author='Paul Martin',
    author_email='paulmartinforwork@gmail.com',
    description="Python Crypto Coin Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/primal100/pybitcointools',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

from setuptools import setup, find_packages
# setup(name='pycointools',
#       version='0.0.1',
#       description='Python Crypto Coin Tools',
#       long_description=open('README.md').read(),
#       author='Paul Martin',
#       author_email='paulmartinforwork@gmail.com',
#       url='http://github.com/primal100/pybitcointools',
#       packages=find_packages(),
#       scripts=['cryptotool'],
#       include_package_data=True,
#       classifiers=[
#             # 'Development Status :: 5 - Production/Stable',
#             # 'Intended Audience :: Developers',
#             # 'Intended Audience :: Education',
#             # 'License :: OSI Approved :: MIT License',
#             # 'Operating System :: OS Independent',
#             # 'Programming Language :: Python',
#             # # 'Programming Language :: Python :: 2',
#             # 'Programming Language :: Python :: 3',
#             # 'Topic :: Security :: Cryptography',
#             "Programming Language :: Python :: 3",
#             "License :: OSI Approved :: MIT License",
#             "Operating System :: OS Independent",
#       ],
#       )
