import MeCab

class MeCabParser(object):
    def __init__(self, arg=''):
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
