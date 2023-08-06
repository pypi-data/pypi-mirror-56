import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as f:
    README = f.read()

setup(
    name="watched-schema",
    version="0.0.0",
    description="JSON schema files for WATCHED",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/watchedcom/schema",
    author="WATCHED",
    author_email="dev@watched.com",
    packages=["watched_schema"],
    install_requires=["pyyaml", "jsonschema"],
    data_files=[["src", ["src/schema.yaml"]]],
    python_requires=">=3.4",
)
