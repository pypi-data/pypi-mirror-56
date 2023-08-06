import os
import json
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as f:
    README = f.read()

package = json.load(open("package.json", "r"))

setup(
    name="watched-schema",
    version=package['version'],
    description=package['description'],
    long_description=README,
    long_description_content_type="text/markdown",
    url=package['repository'],
    author="WATCHED",
    author_email="dev@watched.com",
    packages=find_packages(),
    install_requires=["pyyaml", "jsonschema"],
    package_data={"src": ["schema.yaml"]},
    python_requires=">=3.4",
)
