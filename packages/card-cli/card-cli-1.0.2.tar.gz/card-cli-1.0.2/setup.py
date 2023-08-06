import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="card-cli",
    version="1.0.2",
    author='Wietse Gielen',
    author_email='giertz@inuits.eu',
    description='card-cli is a command line utility for reading smartcards and magnetic stripe cards.',
    long_description=long_description,
    url='https://github.com/WietseGielen/card-reader-cli',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=[
        'pyscard==1.9.9',
            'pyusb==1.0.0b2',
    ],
    entry_points={
        'console_scripts': [
            'card-cli = card_reader:main',
        ]
    },
)
