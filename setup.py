from setuptools import setup, Extension, Command, find_packages
import platform


# find packages in vsm subdirectory
# this will skip the unittests, etc.
packages = ['hyperbrain.'+pkg for pkg in find_packages('hyperbrain')]
packages.append('hyperbrain')

install_requires=[
        "numpy>=1.6.1",
        "scipy>=0.13.0",
        'bottle>=0.12',
        'wget',
        'topicexplorer',
        'wsgiproxy'
        ]

if platform.python_version_tuple()[0] == 2:
    install_requires.append("futures>=3.0.0")

setup(
    name = "hyperbrain",
    version = "0.1",
    description = ('HyperBrain Project'),
    author = "Jaimie Murdock",
    author_email = "jammurdo@indiana.edu",
    url = "http://hyperbrain.org/",
    download_url = "http://github.com/JaimieMurdock/hyperbrain",
    keywords = [],
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
        ],
    install_requires=install_requires,
    packages=packages,
    entry_points={
        'console_scripts' : ['hyperbrain = hyperbrain.serve:main']
    }
    
)
