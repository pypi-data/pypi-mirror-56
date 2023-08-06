from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='markov362m',  # Required
    version='0.0.10',  # Required

    # This is a one-line description or tagline of what your project does. This
    # corresponds to the "Summary" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#summary
    description='A Markov-chain class for M362M', # Optional
    long_description=long_description,  # Optional
    url='https://github.com/gordanz/Markov362M',  # Optional
    author='Gordan Zitkovic',
    author_email='gordanz@math.utexas.edu',  # Optional
    #keywords='sample setuptools development',  # Optional
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    python_requires='>=3.5, <4',
    install_requires=['numpy','scipy','networkx>=2.3'],  # Optional
    project_urls={  # Optional
        'Source': 'https://github.com/gordanz/MarkovM362M/'
    },
)
