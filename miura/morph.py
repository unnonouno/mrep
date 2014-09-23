# encoding: utf-8

import MeCab

def parse(s):
    tagger = MeCab.Tagger()
    node = tagger.parseToNode(s)
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
    print(json.dumps(parse('今日は晴れです')))
