#-*- encoding: UTF-8 -*-
from setuptools import setup, find_packages

VERSION = "2.1.0"

setup(name='fucking',
      version=VERSION,
      description="a python tool which make English word to Chinese using the baidu translate.",
      long_description='Simply, this is a python tool which make English word to Chinese using the baidu translate. The feature is fucking once fetch the meaning of the word, it will save it to the local sqlite database. Then the next time you lookup the word, fucking will directly get the meaning of the word quickly from thr disk cache.',
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Terminals"
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python3 translate terminal',
      author='justin13',
      author_email='justin13wyx@gmail.com',
      url="https://github.com/Yaoxuannn/Python_Tools",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'requests',
        'PyExecJS'
      ],
      entry_points={
        'console_scripts':[
            'fucking = Fucking.fucking:main'
        ]
      },
)
