import os
import sys
from shutil import rmtree
import subprocess

from setuptools import find_packages, setup, Command
from setuptools.command.test import test

base_dir = os.path.abspath(os.path.dirname(__file__))

NAME = "sonora"
DESCRIPTION = "gRPC-Web for Python"
URL = "https://github.com/public/sonora"
EMAIL = "alexs@prol.etari.at"
AUTHOR = "Alex Stapleton"
REQUIRES_PYTHON = ">=3.7.0"

REQUIRED = ["grpcio", "requests"]

TESTS_REQUIRED = [
    "grpcio-tools",
    "pytest",
    "pytest-mockservers",
    "pytest-asyncio",
    "requests",
    "daphne",
]

EXTRAS = {"tests": TESTS_REQUIRED}

with open(os.path.join(base_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

about = {}
with open(os.path.join(base_dir, NAME, "__version__.py")) as f:
    exec(f.read(), about)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(base_dir, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system(f"{sys.executable} setup.py sdist bdist_wheel")

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload --verbose dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    tests_require=TESTS_REQUIRED,
    include_package_data=True,
    license="Apache License, Version 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    cmdclass={"upload": UploadCommand},
)
