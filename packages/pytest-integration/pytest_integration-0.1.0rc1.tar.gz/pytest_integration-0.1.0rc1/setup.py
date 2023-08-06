from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pytest_integration',
    version='0.1.0rc1',
    author='Johan B.W. de Vries',
    author_email='jbwdevries@gmail.com',
    description='Organizing pytests by integration or not',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jbwdevries/pytest-integration',
    packages=['pytest_integration'],
    # the following makes a plugin available to pytest
    entry_points={
        'pytest11': ['name_of_plugin = pytest_integration.pytest_plugin'],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Framework :: Pytest',
    ],
    python_requires='>=3.6',
    setup_requires=[
        'wheel',
    ],
)
