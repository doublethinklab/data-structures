import setuptools


with open('version') as f:
    version = f.read().strip()


setuptools.setup(
    name='data_structures',
    version=version,
    author='Tim Niven',
    author_email='tim@doublethinklab.org',
    description='Explicitly defined data structures.',
    url=f'https://github.com/doublethinklab/data-structures.git#{version}',
    packages=setuptools.find_packages(),
    python_requires='>=3.9.5')
