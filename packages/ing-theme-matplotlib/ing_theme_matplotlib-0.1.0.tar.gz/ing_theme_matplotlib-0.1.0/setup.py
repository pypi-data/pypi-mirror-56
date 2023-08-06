import re
import os
from os import path

from setuptools import find_packages, setup

name = "ing_theme_matplotlib"
here = path.abspath(path.dirname(__file__))

# get package version
try:
    if os.environ.get('CI_COMMIT_TAG'):
        version = os.environ['CI_COMMIT_TAG']
    else:
        version = os.environ['CI_JOB_ID']
except:
    version = 'local'


# get the dependencies and installs
with open("requirements.txt", "r", encoding="utf-8") as f:
    requires = [x.strip() for x in f if x.strip()]

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()

setup(
    name=name,
    version=version,
    description="ING styles for common plotting libraries",
    long_description=readme,
    long_description_content_type='text/markdown',
    url="https://gitlab.com/ing_rpaa/ing_theme_matplotlib",
    author="Ahmet Emre Bayraktar - ING",
    author_email="aemrebayraktar@gmail.com",
    python_requires=">=3.5",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    license="Apache 2.0",
)
