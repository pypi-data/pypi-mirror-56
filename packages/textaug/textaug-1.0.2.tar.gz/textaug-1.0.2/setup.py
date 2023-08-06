"""
Copyright 2019, NIA(정보화진흥원), All rights reserved.
Mail : rocketgrowthsj@gmail.com
"""
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="textaug",
    version="1.0.2",
    description="Text Image Augmentor: data generator for text recognition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email="rocketgrowthsj@gmail.com",
    license="MIT",
    platforms=['linux', 'macosx', 'win'],
    python_requires='>=3.5',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="text-recognition training-set-generator ocr dataset",
    package_dir={'': 'textaug'},
    packages=find_packages(where='textaug', exclude=["contrib", "samples", "tests"]),
    include_package_data=True,
    install_requires=[
        "numpy<1.17",
        "tqdm>=4",
        "imgaug>=0.2",
        "opencv_python>=3.4"
    ],
    entry_points={
        'console_scripts': [
            'textaug=textaug:cli'
        ]
    },
    zip_safe=False,
)
