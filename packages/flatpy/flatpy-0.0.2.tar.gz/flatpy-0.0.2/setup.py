"""
      Setup script for flatpy
"""
from setuptools import setup
import re


extra_args = {}


def get_property(prop, project):
    """
        Helper function for retrieving properties from a project's
        __init__.py file
        @In, prop, string representing the property to be retrieved
        @In, project, string representing the project from which we will
        retrieve the property
        @Out, string, the value of the found property
    """
    result = re.search(
        r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
        open(project + "/__init__.py").read(),
    )
    return result.group(1)


VERSION = get_property("__version__", "flatpy")


def long_description():
    """ Reads the README.rst file and extracts the portion tagged between
        specific LONG_DESCRIPTION comment lines.
    """
    description = ""
    recording = False
    with open("README.rst") as f:
        for line in f:
            if "END_LONG_DESCRIPTION" in line:
                return description
            elif "LONG_DESCRIPTION" in line:
                recording = True
                continue

            if recording:
                description += line


# Consult here: https://packaging.python.org/tutorials/distributing-packages/
setup(
    name="flatpy",
    packages=["flatpy"],
    version=VERSION,
    description="A library for computing samplings in arbitrary dimensions",
    long_description=long_description(),
    author="Dan Maljovec",
    author_email="maljovec002@gmail.com",
    license="BSD",
    test_suite="flatpy.tests",
    url="https://github.com/maljovec/flatpy",
    download_url="https://github.com/maljovec/flatpy/archive/"
    + VERSION
    + ".tar.gz",
    keywords=[""],
    # Consult here: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: C++",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    setup_requires=["scipy", "numpy"],
    install_requires=["scipy", "numpy"],
    python_requires=">=2.7, <4",
)
