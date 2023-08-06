from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='trooper',
    version='0.0.1',
    packages=['trooper'],
    url='https://github.com/elvisdsz/trooperproject',
    license='MIT',
    author='Elvis Louis Dsouza',
    author_email='elvis.dsouza666@gmail.com',
    description='A simple user-friendly library for multi-user applications.',
    long_description=long_description,
    install_requires=['tornado==6.0.3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
