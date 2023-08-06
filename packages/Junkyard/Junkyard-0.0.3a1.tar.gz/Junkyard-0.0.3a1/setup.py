import os
import re

import setuptools


# thanks colorama
def read_file(path):
    with open(os.path.join(os.path.dirname(__file__), path)) as f:
        return f.read()


# thanks colorama
def _get_version_match(content):
    # Search for lines of the form: # __version__ = 'ver'
    regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    version_match = re.search(regex, content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# thanks colorama
def get_version(path):
    return _get_version_match(read_file(path))


NAME = "Junkyard"
# thanks colorama
setuptools.setup(
    name=NAME,
    version=get_version(os.path.join('junkyard', '__init__.py')),
    author="CKD",
    author_email="crushkilldestroy@tuta.io",
    description="A collection of [certifiable garbage] dev helpers/handlers created by and for the author",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    keywords='personal library, not for you, unless you want it',
    url="https://github.com/crushkilldestroy/Junkyard",
    packages=[NAME],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ],
    install_requires=[
        'colorama',
        'wget',
    ],
    python_requires='>=3.7',
)
