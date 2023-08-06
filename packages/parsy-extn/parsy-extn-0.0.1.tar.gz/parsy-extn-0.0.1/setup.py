import os.path
from setuptools import setup, find_packages


def read_file(fn):
    with open(os.path.join(os.path.dirname(__file__), fn)) as f:
        return f.read()

setup(
    name="parsy-extn",
    version="0.0.1",
    description="Small extensions to Parsy",
    url="http://github.com/jan-g/parsy_extn",
    long_description=read_file("README.md"),
    author="jang",
    author_email="parsy-extn@ioctl.org",
    license="Apache License 2.0",

    packages=find_packages(exclude=["test*"]),

    install_requires=[
                      "parsy",
    ],

    tests_require=[
                    "pytest",
                    "flake8",
                    "wheel",
    ],

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Text Processing",
    ],
)
