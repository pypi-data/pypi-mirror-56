#

import setuptools

with open('readme.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="flask-xinidea",
    version="0.0.4",
    author="phiix",
    author_email="phiix@qq.com",
    description="Some Flask custom extension",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
