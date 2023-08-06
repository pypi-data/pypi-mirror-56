import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sight_machine',
    version='0.1',
    author="Denis Bajet",
    author_email="dbajet@gmail.com",
    description='Simple binary logger',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/dbajet/sight_machine/',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
