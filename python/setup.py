# Copyright (c) 2018, NVIDIA CORPORATION.
import os
import shutil
import sysconfig
from distutils.sysconfig import get_python_lib

from Cython.Build import cythonize
from setuptools import find_packages, setup
from setuptools.extension import Extension

install_requires = ["cython"]

cython_files = ["nvtx/**/*.pyx"]

try:
    nthreads = int(os.environ.get("PARALLEL_LEVEL", "0") or "0")
except Exception:
    nthreads = 0

extensions = [
    Extension(
        "*",
        sources=cython_files,
        include_dirs=[
            os.path.dirname(sysconfig.get_path("include")),
        ],
        library_dirs=[get_python_lib()],
        language="c",
    )
]

setup(
    name="nvtx",
    version="0.1",
    description="PyNVTX - Python code annotation library",
    url="https://github.com/NVIDIA/nvtx",
    author="NVIDIA Corporation",
    license="Apache 2.0",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Database",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    # Include the separately-compiled shared library
    setup_requires=["cython"],
    ext_modules=cythonize(
        extensions,
        nthreads=nthreads,
        compiler_directives=dict(
            profile=False, language_level=3, embedsignature=True
        ),
    ),
    packages=find_packages(include=["nvtx", "nvtx.*"]),
    package_data=dict.fromkeys(
        find_packages(include=["nvtx._lib*"]), ["*.pxd"],
    ),
    install_requires=install_requires,
    zip_safe=False,
)