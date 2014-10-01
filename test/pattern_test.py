import unittest
import miura.pattern

class Collector(object):
    def __init__(self):
        self.results = []

    def collect(self, s, pos):
        self.results.append(pos)

class PatternTest(unittest.TestCase):
    def setUp(self):
        self.collector = Collector()

class ConditionTest(PatternTest):
    def setUp(self):
        PatternTest.setUp(self)
        self.pattern = miura.pattern.Condition(lambda x: 'x'==x)

    def testMatch(self):
        self.pattern.match('x', 0, self.collector.collect)
        self.assertEqual([1], self.collector.results)

    def testUnmatch(self):
        self.pattern.match('y', 0, self.collector.collect)
        self.assertEqual([], self.collector.results)

    def testTooShort(self):
        self.pattern.match('', 0, self.collector.collect)
        self.assertEqual([], self.collector.results)

class SequenceTest(PatternTest):
    def setUp(self):
        PatternTest.setUp(self)
        c1 = miura.pattern.Condition(lambda x: 'x'==x)
        c2 = miura.pattern.Condition(lambda x: 'y'==x)
        self.pattern = miura.pattern.Sequence(c1, c2)

    def testMatch(self):
        self.pattern.match('xy', 0, self.collector.collect)
        self.assertEqual([2], self.collector.results)

    def testMatchFirst(self):
        self.pattern.match('xz', 0, self.collector.collect)
        self.assertEqual([], self.collector.results)

    def testNoMatch(self):
        self.pattern.match('', 0, self.collector.collect)
        self.assertEqual([], self.collector.results)

    def testOnlyFirst(self):
        self.pattern.match('x', 0, self.collector.collect)
        self.assertEqual([], self.collector.results)


class SelectTest(PatternTest):
    def setUp(self):
        PatternTest.setUp(self)
        c1 = miura.pattern.Condition(lambda x: 'x'==x)
        c2 = miura.pattern.Condition(lambda x: 'y'==x)
        self.pattern = miura.pattern.Select(c1, c2)

    def testMatchFirst(self):
        self.pattern.match('x', 0, self.collector.collect)
        self.assertEqual([1], self.collector.results)

    def testMatchSecond(self):
        self.pattern.match('y', 0, self.collector.collect)
        self.assertEqual([1], self.collector.results)

    def testUnmatch(self):
        self.pattern.match('z', 0, self.collector.collect)
        self.assertEqual([], self.collector.results)

class RepeatTest(PatternTest):
    def setUp(self):
        PatternTest.setUp(self)
        c = miura.pattern.Condition(lambda x: 'x'==x)
        self.pattern = miura.pattern.Repeat(c)

    def testMatchOne(self):
        self.pattern.match('x', 0, self.collector.collect)
        self.assertEqual([1], self.collector.results)

    def testMatchTwo(self):
        self.pattern.match('xx', 0, self.collector.collect)
        self.assertEqual([2, 1], self.collector.results)

    def testMatchThree(self):
        self.pattern.match('xxxy', 0, self.collector.collect)
        self.assertEqual([3, 2, 1], self.collector.results)

class FindTest(unittest.TestCase):
    def testFind(self):
        c = miura.pattern.Repeat(miura.pattern.Condition(lambda x: 'x'==x))
        result = miura.pattern.find('xxyxxxy', c)
        expect = [
            {'match': 'xx', 'begin': 0, 'end': 2},
            {'match': 'xxx', 'begin': 3, 'end': 6},
        ]
        self.assertEqual(expect, result)

class ExpTimeTest(unittest.TestCase):
    def testFind(self):
        from miura.pattern import Repeat
        # This pattern matches exponential combination
        c = Repeat(Repeat(Repeat(Repeat(miura.pattern.Condition(lambda x: 'x'==x)))))
        result = miura.pattern.find('xxxxxxxxxx', c)
