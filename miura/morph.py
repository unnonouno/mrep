import re
import subprocess
import sys

def make_mecab_parser(mecab_command=None, arg=''):
    if mecab_command:
        return MeCabProcParser(mecab_command)

    try:
        import MeCab
    except ImportError:
        return MeCabProcParser('mecab')

    return MeCabParser(arg)

class MeCabParser(object):
    def __init__(self, arg=''):
        import MeCab
        model = MeCab.Model_create(arg)
        if model is None:
            raise Exception('Cannot initialize mecab')
        self.model = model
        
    def parse(self, s):
        tagger = self.model.createTagger()
        lattice = self.model.createLattice()
        lattice.set_sentence(s)
        tagger.parse(lattice)
        node = lattice.bos_node()
        morphs = []
        while node:
            if node.surface != '':
                feature = node.feature
                morphs.append({
                    'surface': node.surface,
                    'pos': feature[0:feature.find(',')],
                    'feature': feature,
                })
            node = node.next
        return morphs

class MeCabProcParser(object):
    def __init__(self, command):
        self.command = command

    def parse(self, s):
        # TODO(unno): need to check error
        proc = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        if sys.version_info >= (3, 0):
            import locale
            encoding = locale.getpreferredencoding()
            out = proc.communicate(s.encode(encoding))[0].decode(encoding)
        else:
            out = proc.communicate(s)[0]
        morphs = []

        if sys.version_info >= (3, 0):
            from io import StringIO
        else:
            from cStringIO import StringIO

        for l in StringIO(out):
            line = l.strip()
            if line == 'EOS':
                break
            m = re.match(r'(.*)\t(.*)', line)
            if m:
                surface = m.group(1)
                feature = m.group(2)
                pos = feature.split(',')[0]
                morphs.append({
                    'surface': surface,
                    'pos': pos,
                    'feature': feature,
                })

        return morphs
