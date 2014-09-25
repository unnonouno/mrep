import unittest
from StringIO import StringIO
import miura.printer

class PrinterTest(unittest.TestCase):
    def setUp(self):
        self.printer = miura.printer.Printer('[', ']')
        self.out = StringIO()
        self.sequence = [
            {'surface': 'x'},
            {'surface': 'y'},
            {'surface': 'z'},
        ]

    def test_no_result(self):
        self.printer.print_result(self.sequence, [], self.out)
        self.assertEqual('x y z', self.out.getvalue())

    def test_one_result(self):
        result = [
            {'begin': 1, 'end': 2},
        ]
        self.printer.print_result(self.sequence, result, self.out)
        self.assertEqual('x [y] z', self.out.getvalue())

    def test_first(self):
        result = [
            {'begin': 0, 'end': 2},
        ]
        self.printer.print_result(self.sequence, result, self.out)
        self.assertEqual('[x y] z', self.out.getvalue())

    def test_last(self):
        result = [
            {'begin': 1, 'end': 3},
        ]
        self.printer.print_result(self.sequence, result, self.out)
        self.assertEqual('x [y z]', self.out.getvalue())

    def test_two(self):
        result = [
            {'begin': 0, 'end': 1},
            {'begin': 1, 'end': 2},
        ]
        self.printer.print_result(self.sequence, result, self.out)
        self.assertEqual('[x y] z', self.out.getvalue())

