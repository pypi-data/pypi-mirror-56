import io
import sys
from glob import glob

from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
from os.path import abspath

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

# Upload version to PyPi:
#   \-> python setup.py sdist bdist_wheel
#   \-> python -m twine upload dist/*  # (requires PyPi username & password)
HERE = abspath(dirname(__file__))


class PyTest(TestCommand):  # TODO: actually implement tests
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        import shlex

        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


about = {}
exec(read(join(HERE, "src", "traindiagnostics", "__version__.py")), about)

requirements = ["ticts>=0.3.3"]

setup(
    name="traindiagnostics",
    version=about["__version__"],  # TODO: implement bumpversion (bump2version) versioning
    author="Timo Lesterhuis",
    author_email="Timo.Lesterhuis@gmail.com",
    description="A toolbox to analyse diagnostic train data!",
    long_description=read("README.rst"),
    long_description_content_type="text/x-rst",
    url="https://github.com/timolesterhuis/traindiagnostics/",
    project_urls={
        #'Documentation': 'https://diagnostics.readthedocs.io/',
        # 'Changelog': 'https://python-nameless.readthedocs.io/en/latest/changelog.html',
        "Source": "https://github.com/timolesterhuis/traindiagnostics",
        'Issue Tracker': 'https://github.com/timolesterhuis/traindiagnostics/issues',
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    tests_require=["pytest", "pytest-cov", "pytest-mpl"],
    cmdclass={"pytest": PyTest},
    license="GNU GPLv3",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
