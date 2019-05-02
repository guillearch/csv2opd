# CSV2OPD - A CSV to XML converter for OpenProdoc

This desktop application transforms the metadata stored in a CSV file into XML files compatible with the open source DMS [OpenProdoc](https://github.com/JHierrot/openprodoc).

This application was created by [Guillermo Castellano](https://guillearch.github.io/), from [Nosturi](https://nosturi.es/).

The code is licensed under the [GNU General Public License v3.0](https://github.com/guillearch/atom-installer/blob/master/LICENSE). Feel free to adapt the script for your specific needs!

## Requirements

This application can be used on any operating system which supports Python 3.x.

Check if you have Python 3.x installed by entering the following command into your terminal:

```
python --version
```

You should see something like this:

```
$ python --version
Python 3.7.0
```

Otherwise, [download and install Python](https://www.python.org/downloads/) before moving forward.

## Downloading

The easiest way to download CSV2OPD is to clone this repository:

```
git clone https://github.com/guillearch/csv2opd.git
```

Alternatively, you can download it as a ZIP:

```
wget https://github.com/guillearch/csv2opd/archive/master.zip
```

Then unzip the file:

```
unzip master.zip
```

## Running the application

1. Open the directory `/csv2opd` and run the application by entering the following command: `python csv2opd.py`.
2. Select the input CSV file. It must have a header.
3. Select the output directory for the XML files.
4. Select the type of field separator (delimiter) used by your CSV file.
5. Click the button Convert.

Once the conversion is completed, you can import the documents and the metadata into OpenProdoc following the instructions provided in the [official documentation](https://jhierrot.github.io/openprodoc/help/EN/ImpExpFold.html).

We're all set!

 **Important**: The name of each document must be the same than the value of the Name field on its related OPD file.

## Additional information

This application is intended for OpenProdoc 2.x.

Please read the [changelog](https://github.com/guillearch/csv2opd/tree/master/docs/changelog.md) and the [docstring](https://github.com/guillearch/csv2opd/tree/master/docs/helpfile.txt).

If you need any further assistance, don't hesitate to [contact me](mailto:gcastellano@nosturi.es).
