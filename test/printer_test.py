import unittest
import sys

if sys.version_info >= (3, 0):
    from io import StringIO
else:
    from StringIO import StringIO

import mrep.printer


class OnlyMatchingPrinterTest(unittest.TestCase):
    def setUp(self):
        self.printer = mrep.printer.Printer('[', ']')
        self.out = StringIO()
        self.sequence = [
            {'surface': 'x'},
            {'surface': 'y'},
            {'surface': 'z'},
        ]

    def test_no_result(self):
        self.printer.print_result(self.sequence, [], self.out)
        self.assertEqual('x y z\n', self.out.getvalue())

    def test_one_result(self):
        result = [
            {'begin': 1, 'end': 2},
        ]
        self.printer.print_result(self.sequence, result, self.out)
        self.assertEqual('x [y] z\n', self.out.getvalue())

    def test_first(self):
        result = [
            {'begin': 0, 'end': 2},
        ]
        self.printer.print_result(self.sequence, result, self.out)
        self.assertEqual('[x y] z\n', self.out.getvalue())

    def test_last(self):
        result = [
            {'begin': 1, 'end': 3},
        ]
        self.printer.print_result(self.sequence, result, self.out)
        self.assertEqual('x [y z]\n', self.out.getvalue())

    def test_two(self):
        result = [
            {'begin': 0, 'end': 1},
            {'begin': 1, 'end': 2},
        ]
        self.printer.print_result(self.sequence, result, self.out)
        self.assertEqual('[x y] z\n', self.out.getvalue())


class PrinterTest(unittest.TestCase):
    def setUp(self):
        self.printer = mrep.printer.OnlyMatchPrinter('[', ']')
        self.out = StringIO()
        self.sequence = [
            {'surface': 'x'},
            {'surface': 'y'},
            {'surface': 'z'},
        ]

    def test_no_result(self):
        self.printer.print_result(self.sequence, [], self.out)
        self.assertEqual('', self.out.getvalue())

    def test_one_result(self):
        result = [
            {'begin': 1, 'end': 2},
        ]
        self.printer.print_result(self.sequence, result, self.out)
        self.assertEqual('[y]\n', self.out.getvalue())

    def test_first(self):
        result = [
            {'begin': 0, 'end': 2},
        ]
        self.printer.print_result(self.sequence, result, self.out)
        self.assertEqual('[x y]\n', self.out.getvalue())

    def test_last(self):
        result = [
            {'begin': 1, 'end': 3},
        ]
        self.printer.print_result(self.sequence, result, self.out)
        self.assertEqual('[y z]\n', self.out.getvalue())

    def test_two(self):
        result = [
            {'begin': 0, 'end': 1},
            {'begin': 1, 'end': 2},
        ]
        self.printer.print_result(self.sequence, result, self.out)
        self.assertEqual('[x]\n[y]\n', self.out.getvalue())
