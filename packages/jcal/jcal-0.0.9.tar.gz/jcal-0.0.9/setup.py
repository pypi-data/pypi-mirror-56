from setuptools import setup

version = '0.0.9'
name = 'jcal'
short_description = '`jcal` is a package for Japanese holiday.'
long_description = """\
`jcal` is a package for Japanese holiday.
::

   print(holiday(2019))
   >>>
   {datetime.date(2019, 2, 11), datetime.date(2019, 1, 14), datetime.date(2019, 4, 30),
    datetime.date(2019, 11, 4), datetime.date(2019, 10, 22), datetime.date(2019, 9, 23),
    datetime.date(2019, 1, 1), datetime.date(2019, 8, 12), datetime.date(2019, 4, 29),
    datetime.date(2019, 5, 6), datetime.date(2019, 10, 14), datetime.date(2019, 3, 21),
    datetime.date(2019, 5, 3), datetime.date(2019, 5, 2), datetime.date(2019, 5, 1),
    datetime.date(2019, 5, 4), datetime.date(2019, 7, 15), datetime.date(2019, 5, 5),
    datetime.date(2019, 11, 23), datetime.date(2019, 9, 16)}

Requirements
------------
* Python 3

Features
--------
* nothing

Setup
-----
::

   $ pip install jcal

History
-------
0.0.1 (2016-2-5)
~~~~~~~~~~~~~~~~~~
* first release

"""

classifiers = [
   "Development Status :: 1 - Planning",
   "License :: OSI Approved :: Python Software Foundation License",
   "Programming Language :: Python",
   "Topic :: Software Development",
   "Topic :: Scientific/Engineering",
]

setup(
    name=name,
    version=version,
    description=short_description,
    long_description=long_description,
    classifiers=classifiers,
    py_modules=['jcal'],
    keywords=['jcal',],
    author='Saito Tsutomu',
    author_email='tsutomu.saito@beproud.jp',
    url='https://pypi.python.org/pypi/jcal',
    license='PSFL',
    entry_points={
            'console_scripts':[
                'jcal = jcal:main',
            ],
        },
)