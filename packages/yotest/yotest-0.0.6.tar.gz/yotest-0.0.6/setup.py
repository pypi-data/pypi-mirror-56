import setuptools


try:
    from setuptools import setup, find_packages
except ImportError:
    from distils.core import setup, find_packages



setuptools.setup(
    name="yotest",
    version="0.0.6",
    author="Yoman",
    author_email="francis.b.lavoie@usherbrooke.ca",
    description="Yotest",
    long_description="iii",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)