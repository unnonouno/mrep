import unittest
import mrep.builder


class TermTest(unittest.TestCase):
    def testDot(self):
        p, t = mrep.builder.term('.', 0)
        self.assertIsNotNone(t)
        self.assertEqual(1, p)
        self.assertEqual('.', repr(t))

    def testCondition(self):
        p, t = mrep.builder.term('<x=y>', 0)
        self.assertIsNotNone(t)
        self.assertEqual(5, p)
        self.assertEqual('.', repr(t))
        ps = []
        t.match([{'x': 'y'}], 0, lambda s, p: ps.append(p))
        self.assertEqual([1], ps)

    def testPatternCondition(self):
        p, t = mrep.builder.term('<x=~y>', 0)
        self.assertIsNotNone(t)
        self.assertEqual(6, p)
        self.assertEqual('.', repr(t))
        ps = []
        t.match([{'x': 'zyw'}], 0, lambda s, p: ps.append(p))
        self.assertEqual([1], ps)

    def testParen(self):
        p, t = mrep.builder.term('(.)', 0)
        self.assertIsNotNone(t)
        self.assertEqual(3, p)
        self.assertEqual('.', repr(t))

    def testInvalidCharacter(self):
        with self.assertRaises(mrep.builder.InvalidCharacter) as cm:
            mrep.builder.term('|.', 0)
        self.assertEqual(0, cm.exception.pos)
        self.assertEqual('|', cm.exception.actual)

    def testInvalidPattern(self):
        with self.assertRaises(mrep.builder.InvalidPattern) as cm:
            mrep.builder.term('<x', 0)
        self.assertEqual(0, cm.exception.pos)

    def testUnclosedParen(self):
        with self.assertRaises(mrep.builder.InvalidCharacter) as cm:
            mrep.builder.term('(.**', 0)
        self.assertEqual(3, cm.exception.pos)
        self.assertEqual('*', cm.exception.actual)

    def testEOSbeforeClose(self):
        with self.assertRaises(mrep.builder.InvalidCharacter) as cm:
            mrep.builder.term('(.', 0)
        self.assertEqual(2, cm.exception.pos)
        self.assertEqual('EOS', cm.exception.actual)


class StarTest(unittest.TestCase):
    def testStar(self):
        p, t = mrep.builder.star('.*', 0)
        self.assertIsNotNone(t)
        self.assertEqual(2, p)
        self.assertEqual('(* .)', repr(t))

    def testNoStar(self):
        p, t = mrep.builder.star('.', 0)
        self.assertIsNotNone(t)
        self.assertEqual(1, p)
        self.assertEqual('.', repr(t))


class SeqTest(unittest.TestCase):
    def testOne(self):
        p, t = mrep.builder.seq('.', 0)
        self.assertIsNotNone(t)
        self.assertEqual(1, p)
        self.assertEqual('.', repr(t))

    def testTwo(self):
        p, t = mrep.builder.seq('..', 0)
        self.assertIsNotNone(t)
        self.assertEqual(2, p)
        self.assertEqual('.:.', repr(t))

    def testThree(self):
        p, t = mrep.builder.seq('...', 0)
        self.assertIsNotNone(t)
        self.assertEqual(3, p)
        self.assertEqual('.:.:.', repr(t))

    def testSelect(self):
        p, t = mrep.builder.seq('.|.', 0)
        self.assertIsNotNone(t)
        self.assertEqual(3, p)
        self.assertEqual('(OR . .)', repr(t))

    def testSelectThree(self):
        p, t = mrep.builder.seq('.|.|.', 0)
        self.assertIsNotNone(t)
        self.assertEqual(5, p)
        self.assertEqual('(OR . (OR . .))', repr(t))

    def testSelectSeq(self):
        p, t = mrep.builder.seq('.|..|...', 0)
        self.assertIsNotNone(t)
        self.assertEqual(8, p)
        self.assertEqual('(OR . (OR .:. .:.:.))', repr(t))


class ExpTest(unittest.TestCase):
    def testRedundant(self):
        with self.assertRaises(mrep.builder.RedundantCharacters) as cm:
            mrep.builder.exp('.*XYZ', 0)
        self.assertEqual(2, cm.exception.pos)
        self.assertEqual('XYZ', cm.exception.redundant)


class InvalidCharacterTest(unittest.TestCase):
    def testOne(self):
        e = mrep.builder.InvalidCharacter(1, ['x'], 'a')
        self.assertEqual('"x" is expected, but "a" is given', str(e))

    def testTwo(self):
        e = mrep.builder.InvalidCharacter(1, ['x', 'y'], 'a')
        self.assertEqual('"x" or "y" are expected, but "a" is given', str(e))

    def testThree(self):
        e = mrep.builder.InvalidCharacter(1, ['x', 'y', 'z'], 'a')
        self.assertEqual('"x", "y" or "z" are expected, but "a" is given',
                         str(e))
