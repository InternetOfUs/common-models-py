import os

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [x.strip() for x in f.readlines()]

setuptools.setup(
    name="wenet-common",
    version=os.getenv("CI_COMMIT_TAG"),
    author="U-Hopper srl",
    author_email="carlo.caprini@u-hopper.com",
    description="A small package collecting utilities for the WeNet project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=requirements
)
