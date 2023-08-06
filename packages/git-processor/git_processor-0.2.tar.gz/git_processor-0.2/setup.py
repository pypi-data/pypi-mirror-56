from setuptools import setup

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='git_processor',
    version='0.2',
    description='Process and parse through git log statistic',
    long_description=str(long_description),
    keywords='git processor data science',
    url='https://github.com/sylhare/git-processor',
    author='sylhare',
    author_email='sylhare@outlook.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
    ],
    packages=['processor'],
    install_requires=['pandas', 'matplotlib'],
)
