import unittest
from csv2opd import DelimiterError, Parser


class CSV2OPDTest(unittest.TestCase):
    """Unit tests for csv2opd.py."""

    def test_delimiter_error(self):
        with self.assertRaises(DelimiterError):
            Parser(csvFile='./tests/input.csv', xmlFile='./', separator=',')

    def test_index_error(self):
        try:
            parser = Parser(csvFile='./tests/input_index_error.csv',
                            xmlFile='./', separator=';')
            parser.converter()
            self.assertGreater(parser.errors, 0)
        except SystemExit:
            self.assertRaises(SystemExit)


if __name__ == 'main':
    unittest.main()
