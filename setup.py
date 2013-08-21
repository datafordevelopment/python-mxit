from distutils.core import setup

setup(
    name='mxit',
    version='0.0.1',
    author='Donovan Schönknecht',
    author_email='don@tpyo.net',
    packages=['mxit'],
    url='https://github.com/Mxit/python-mxit',
    license='LICENSE',
    description="Python utility library for accessing Mxit's public APIs.",
    long_description=open('README.md').read(),
    install_requires=[
        "requests >= 1.2.3",
    ],
)

