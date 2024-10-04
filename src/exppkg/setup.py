from setuptools import setup, find_packages

setup(
    name='gac',
    version='1.0.0',
    author='Matthew Nesbitt',
    author_email='mingsqu@gmail.com',
    description='git-auto-commiter (GAC)',
    url='https://github.com/MFactor1/git-auto-commiter',
    python_requires='>=3.5',
    packages=find_packages(),
    install_requires=[
        'gevent'
    ],
    entry_points={
        'console_scripts': ['gac=gaccli:main'],
    },
)
