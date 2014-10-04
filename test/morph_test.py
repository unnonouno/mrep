# encoding: utf-8

import unittest
import miura.morph

class ParseTest(unittest.TestCase):

    def test_mecab_parser(self):
        parser = miura.morph.MeCabParser()
        self.run_test_parse(parser)

    def test_mecabproc_parser(self):
        parser = miura.morph.MeCabProcParser('mecab')
        self.run_test_parse(parser)

    def run_test_parse(self, parser):
        ms = parser.parse('我輩は猫だ')
        expect = [
            {'surface': '我輩', 'pos': '名詞'},
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
                          lambda: miura.morph.MeCabParser('--invalid-arg'))
