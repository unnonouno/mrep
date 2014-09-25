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

    def testInvalidCharacter(self):
        with self.assertRaises(miura.builder.InvalidCharacter) as cm:
            miura.builder.term('|.', 0)
        self.assertEqual(0, cm.exception.pos)
        self.assertEqual('|', cm.exception.actual)

    def testInvalidPattern(self):
        with self.assertRaises(miura.builder.InvalidPattern) as cm:
            miura.builder.term('<x', 0)
        self.assertEqual(0, cm.exception.pos)

    def testUnclosedParen(self):
        with self.assertRaises(miura.builder.InvalidCharacter) as cm:
            miura.builder.term('(.**', 0)
        self.assertEqual(3, cm.exception.pos)
        self.assertEqual('*', cm.exception.actual)

    def testEOSbeforeClose(self):
        with self.assertRaises(miura.builder.InvalidCharacter) as cm:
            miura.builder.term('(.', 0)
        self.assertEqual(2, cm.exception.pos)
        self.assertEqual('EOS', cm.exception.actual)

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

class ExpTest(unittest.TestCase):
    def testRedundant(self):
        with self.assertRaises(miura.builder.RedundantCharacters) as cm:
            miura.builder.exp('.*XYZ', 0)
        self.assertEqual(2, cm.exception.pos)
        self.assertEqual('XYZ', cm.exception.redundant)

class InvalidCharacterTest(unittest.TestCase):
    def testOne(self):
        e = miura.builder.InvalidCharacter(1, ['x'], 'a')
        self.assertEqual('"x" is expected, but "a" is given', str(e))

    def testTwo(self):
        e = miura.builder.InvalidCharacter(1, ['x', 'y'], 'a')
        self.assertEqual('"x" or "y" are expected, but "a" is given', str(e))

    def testThree(self):
        e = miura.builder.InvalidCharacter(1, ['x', 'y', 'z'], 'a')
        self.assertEqual('"x", "y" or "z" are expected, but "a" is given', str(e))
