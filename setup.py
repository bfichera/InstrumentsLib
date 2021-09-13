import setuptools

with open('README.md', 'r') as fh:
    with open('CHANGES.md', 'r') as fc:
        long_description = fh.read()+'\n'+fc.read()

with open('.version', 'r') as fh:
    version = fh.read().splitlines()[0]

setuptools.setup(
    name='InstrumentsLib',  
    version=version,
    author='Bryan Fichera',
    author_email='bfichera@mit.edu',
    description=(
        'A couple of utilities to help with'
        'building PyVISA instruments.'
    )
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bfichera/InstrumentsLib',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
    ],
    python_requires='>=3.9',
    install_requires=[
        'appdirs',
    ],
)
