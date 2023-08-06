import os
from io import open
import hashlib
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

requires = [
    "pillow",
    "click",
]

console_scripts = []
for method in hashlib.algorithms_available:
    method = method.replace("-", "_")
    console_scripts.append("{method} = imagespack:{method}".format(method=method))

setup(
    name="imagespack",
    version="0.1.0",
    description="Package images into one PDF file or GIF file or TIFF file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="zencore",
    author_email="dobetter@zencore.cn",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["imagespack"],
    requires=requires,
    install_requires=requires,
    packages=find_packages("."),
    py_modules=["imagespack"],
    entry_points={
        "console_scripts": [
            "imagespack = imagespack:imagespack",
        ],
    },
)