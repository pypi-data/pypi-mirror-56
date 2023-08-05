from setuptools import setup
import os

install_requires = ['biplist', 'pillow']
if os.environ.get('READTHEDOCS', None) is None:
    install_requires.append('python-lzo')

setup(
    name='pyprocreate',
    version='0.1dev0',
    packages=['pyprocreate',],
    license='MIT License',
    description="A package to parse and interact with Apple's Procreate (.pro) file format.",
    setup_requires=['wheel'],
    install_requires=install_requires
)