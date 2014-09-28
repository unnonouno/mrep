# encoding: utf-8

import unittest
import subprocess

ESCAPE = '\033[%sm'
RED = ESCAPE % '31'
ENDC = ESCAPE % '0'

class MiuraFunctionalTest(unittest.TestCase):
    def read_expect(self, index, name):
        with open('test/data/%d_%s.result' % (index, name), 'rb') as f:
            return f.read()

    def call(self, *args):
        command = ' '.join(['python', 'command/miura'] + list(args))
        env = {'PYTHONPATH': '.'}
        return subprocess.check_output(command, shell=True, env=env)

    def call_test(self, index, name, pattern):
        result = self.call('"%s"' % pattern, 'test/data/%d.txt' % index)
        expect = self.read_expect(index, name)
        self.assertEqual(expect, result)

    def test_dot(self):
        self.call_test(1, 'dot', '.')

    def test_verb(self):
        self.call_test(1, 'verb', '<pos=動詞>')

    def test_noun_particle(self):
        self.call_test(1, 'noun_particle', '<pos=名詞>*<pos=助詞>*')

    def test_noun(self):
        self.call_test(1, 'noun_or_verb', '<pos=名詞>|<pos=動詞>')

    def test_stdin(self):
        command = 'cat test/data/1.txt | python command/miura .'
        env = {'PYTHONPATH': '.'}
        result = subprocess.check_output(command, shell=True, env=env)
        expect = self.read_expect(1, 'dot')
        self.assertEqual(expect, result)

    
    def test_unknown_argument(self):
        with self.assertRaises(subprocess.CalledProcessError) as cm:
            self.call('--unknown-argument')

        self.assertEqual(2, cm.exception.returncode)

    def test_invalid_pattern(self):
        with self.assertRaises(subprocess.CalledProcessError) as cm:
            self.call('"<"', 'test/data/1.txt')

        self.assertEqual(3, cm.exception.returncode)
