import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csv2opd",
    version="1.1.1",
    author="Guillermo Castellano",
    author_email="gcastellano@protonmail.com",
    description="A CSV to XML converter for OpenProdoc",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guillearch/csv2opd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'gui_scripts': [
            'csv2opd = csv2opd.csv2opd:main',
            ],
    },
)
