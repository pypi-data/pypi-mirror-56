import io
from setuptools import setup

from v_time import __version__

setup(
    name="v_time",
    version=__version__,
    author="Arnau Villoro",
    author_email="arnau@villoro.com",
    packages=["v_time"],
    include_package_data=True,
    license="MIT",
    description=("Time related functions"),
    long_description=io.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/villoro/v-time",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
)
