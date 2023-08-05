#!/usr/bin/python

"""
Setup for Feersum NLU SDK
"""

# https://packaging.python.org/en/latest/distributing.html
# https://github.com/pypa/sampleproject

import re
from codecs import open

from setuptools import find_packages
from setuptools import setup


def get_version(fname):
    """
    Extracts __version__ from {fname}
    """
    verstrline = open(fname, "rt").read()
    mob = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", verstrline, re.M)
    if mob:
        return mob.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % (fname,))


def get_requirements(fname):
    """
    Extracts requirements from requirements-file <fname>
    """
    reqs = open(fname, "rt").read().strip("\r").split("\n")
    requirements = [
        req for req in reqs
        if req and not req.startswith("#") and not req.startswith("--")
    ]
    return requirements


setup(
    name='feersum_nlu',

    version=get_version('feersum_nlu/__init__.py'),
    description='Feersum Natural Language Processing SDK',
    long_description=open('README.rst', 'r').read(),

    # The project's main homepage.
    url='https://github.com/praekelt/feersum_nlu_sdk',

    # Author details
    author='bernardt@feersum.io',
    author_email='bernardt@feersum.io',

    # Choose your license
    license='???',

    # What does your project relate to?
    keywords='Natural language processing understanding',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=get_requirements('requirements.txt'),
    scripts=[
    ],

    package_data={'': ['nlp_engine_data/lid_za.text_clsfr_pickle',
                       'nlp_engine_data/chunk_af_NCHLT-phrases.csv',
                       'nlp_engine_data/pos_af_GOV-ZA.csv',
                       'rest_api/flask_server/swagger/swagger.yaml']},
    include_package_data=True,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 2 - Pre-Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',

        # Pick your license as you wish (should match "license" above)
        'License :: Other/Proprietary License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],

    zip_safe=False,
)
