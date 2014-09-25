# encoding: utf-8

import MeCab

def parse(s):
    model = MeCab.Model_create('')
    tagger = model.createTagger()
    lattice = model.createLattice()
    lattice.set_sentence(s)
    tagger.parse(lattice)
    node = lattice.bos_node()
    morphs = []
    while node:
        if node.surface != '':
            feature = node.feature
            morphs.append({
                'surface': node.surface,
                'pos': feature.split(',')[0],
                'feature': feature,
            })
        node = node.next
    return morphs

if __name__ == '__main__':
    import json
    text = '今日は晴れです'
    print(json.dumps(parse(text)))
    print(text)
