import unittest
import glob
import os
from csv2opd.csv2opd import DelimiterError, Parser


class CSV2OPDTest(unittest.TestCase):
    """Unit tests for csv2opd.py."""

    def tearDown(self):
        dir_name = '.'
        dir = os.listdir(dir_name)
        for file in dir:
            if file.endswith('.opd'):
                os.remove(os.path.join(dir_name, file))

    def test_conversion(self):
        parser = Parser(csvFile='./tests/input.csv',
                        xmlFile='./tests/', separator=';')
        parser.converter()
        converted_files = len(glob.glob1('.', '*.opd'))
        self.assertEqual(converted_files, 3)

    def test_delimiter_error(self):
        with self.assertRaises(DelimiterError):
            Parser(csvFile='input.csv', xmlFile='.', separator=',')

    def test_index_error(self):
        with self.assertRaises(IndexError):
            parser = Parser(csvFile='input_index_error.csv',
                            xmlFile='.', separator=';')
            parser.converter()

    def test_oserror(self):
        with self.assertRaises(OSError):
            Parser(csvFile='nothing.csv', xmlFile='.', separator=';')


if __name__ == 'main':
    unittest.main()
