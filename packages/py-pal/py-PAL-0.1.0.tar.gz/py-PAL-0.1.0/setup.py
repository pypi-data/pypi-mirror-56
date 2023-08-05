import os
import pathlib

try:
    # Allow installing package without any Cython available. This
    # assumes you are going to include the .c files in your sdist.
    import Cython
except ImportError:
    Cython = None

from setuptools import setup, find_packages, Extension

compiler_options = {
    "language_level": "3str",
    "boundscheck": False,
    "wraparound": False,
    "infer_types": True
}

ext = '.pyx' if Cython else '.c'

root_dir = os.path.dirname(__file__)
extensions = [Extension("pyPAL.tracer", [os.path.join(root_dir, "pyPAL/tracer") + ext])]

if Cython:
    from Cython.Build import cythonize

    extensions = cythonize(extensions, compiler_directives=compiler_options)

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="py-PAL",
    version="0.1.0",
    description="Estimate Asymptotic Runtime Complexity from Bytecode executions",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/segroup-uni-trier/jung-ma-asymptotic-performance-testing.git",
    author="Lukas Jung",
    author_email="mail@lukasjung.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 4 - Beta",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib"
    ],
    entry_points={
        "console_scripts": [
            "pyPAL=pyPAL.__main__:main",
        ]
    },
    setup_requires=[
        'cython',
    ] if Cython else [],
    ext_modules=extensions
)
