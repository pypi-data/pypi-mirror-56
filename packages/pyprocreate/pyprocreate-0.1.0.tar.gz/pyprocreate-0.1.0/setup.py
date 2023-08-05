from setuptools import setup
import os

install_requires = ['biplist', 'pillow']
if os.environ.get('READTHEDOCS', None) is None:
    install_requires.append('python-lzo')

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyprocreate',
    author="InkLab",
    author_email="inklabapp@gmail.com",
    version='0.1.0',
    packages=['pyprocreate',],
    license='MIT License',
    description="A package to parse and interact with Apple's Procreate (.pro) file format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/inklabapp/pyprocreate",
    setup_requires=['wheel'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires
)