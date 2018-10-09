import csv
import os
import pytest

def test_converter():

    csvFile = 'myData.csv'
    xmlFile = './'
    separator = ';'

    csvData = csv.reader(open(csvFile, 'r'), delimiter = separator)

    os.chdir(xmlFile)

    rowNum = 0
    for row in csvData:
        xmlData = open('xmlFile.xml', 'w')
        if rowNum == 0:
            tags = row
        else:
            xmlData.write('<OPDObject type="PD_DOCS">\n<ListAttr>\n')
            for i in range(len(tags)):
                xmlData.write('<Attr Name="' + tags[i] + '">' \
                              + row[i] + '</Attr>' + "\n")
                if tags[i] == 'Name':
                    os.rename ('xmlFile.xml', row[i] + '.opd')
            xmlData.write('</ListAttr></OPDObject>\n')

        rowNum +=1
        xmlData.close()

test_converter()
