# encoding: utf-8

import unittest
import mrep.morph


class ParseTest(unittest.TestCase):
    def test_parse(self):
        parser = mrep.morph.MeCabParser()
        ms = parser.parse('我輩は猫だ')
        expect = [
            {'surface': '我輩', 'pos': '代名詞'},
            {'surface': 'は', 'pos': '助詞'},
            {'surface': '猫', 'pos': '名詞'},
            {'surface': 'だ', 'pos': '助動詞'},
        ]
        self.assertEqual(len(expect), len(ms))
        for e, m in zip(expect, ms):
            self.assertEqual(e['surface'], m['surface'])
            self.assertEqual(e['pos'], m['pos'])

    def test_invalid_argument(self):
        self.assertRaises(Exception,
                          lambda: mrep.morph.MeCabParser('--invalid-arg'))
