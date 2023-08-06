from setuptools import setup, find_packages
from os.path import join, dirname
import webchains

setup(
    name='webchains',
    version=webchains.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    install_requires=[
        'numpy >= 1.14.3',
        'matplotlib >= 2.2.2',
        'pandas>=0.24.2',
        'datetime'
    ]

)