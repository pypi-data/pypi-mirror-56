"""Setup for the chocobo package."""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Thierno Ibrahima DIOP",
    author_email="thierno.diop@baamtu.com",
    name='regtester',
    license="MIT",
    description='RegEx Tester is a module to build unit test of regex in python',
    version='v1.2',
    long_description=README,
    url='https://github.com/bayethiernodiop/regtester',
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=["regex==2019.11.1","colorama==0.4.1"],
    entry_points ={ 
            'console_scripts': [ 
                'regtester = regtester.RegExTester:main',
                'regtester-test = regtester.RegExTester:test'
            ] 
        }, 
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)