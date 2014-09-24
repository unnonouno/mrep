import unittest
import miura.builder

class TermTest(unittest.TestCase):
    def testDot(self):
        p, t = miura.builder.term('.', 0)
        self.assertIsNotNone(t)
        self.assertEqual(1, p)
        self.assertEqual('.', repr(t))

    def testCondition(self):
        p, t = miura.builder.term('<x=y>', 0)
        self.assertIsNotNone(t)
        self.assertEqual(5, p)
        self.assertEqual('.', repr(t))

    def testParen(self):
        p, t = miura.builder.term('(.)', 0)
        self.assertIsNotNone(t)
        self.assertEqual(3, p)
        self.assertEqual('.', repr(t))

class StarTest(unittest.TestCase):
    def testStar(self):
        p, t = miura.builder.star('.*', 0)
        self.assertIsNotNone(t)
        self.assertEqual(2, p)
        self.assertEqual('(* .)', repr(t))
        
    def testNoStar(self):
        p, t = miura.builder.star('.', 0)
        self.assertIsNotNone(t)
        self.assertEqual(1, p)
        self.assertEqual('.', repr(t))

class SeqTest(unittest.TestCase):
    def testOne(self):
        p, t = miura.builder.seq('.', 0)
        self.assertIsNotNone(t)
        self.assertEqual(1, p)
        self.assertEqual('.', repr(t))

    def testTwo(self):
        p, t = miura.builder.seq('..', 0)
        self.assertIsNotNone(t)
        self.assertEqual(2, p)
        self.assertEqual('.:.', repr(t))

    def testThree(self):
        p, t = miura.builder.seq('...', 0)
        self.assertIsNotNone(t)
        self.assertEqual(3, p)
        self.assertEqual('.:.:.', repr(t))

    def testSelect(self):
        p, t = miura.builder.seq('.|.', 0)
        self.assertIsNotNone(t)
        self.assertEqual(3, p)
        self.assertEqual('(OR . .)', repr(t))

    def testSelectThree(self):
        p, t = miura.builder.seq('.|.|.', 0)
        self.assertIsNotNone(t)
        self.assertEqual(5, p)
        self.assertEqual('(OR . (OR . .))', repr(t))

    def testSelectSeq(self):
        p, t = miura.builder.seq('.|..|...', 0)
        self.assertIsNotNone(t)
        self.assertEqual(8, p)
        self.assertEqual('(OR . (OR .:. .:.:.))', repr(t))
