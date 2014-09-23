# encoding: utf-8

import morph
import builder
import pattern

ms = morph.parse('今日はおいしい焼肉定食を食べた')
#print ms

def show(s, pos):
    print(' '.join([s[i]['surface'] for i in range(pos)]))

matcher = builder.parse('<pos=形容詞><pos=名詞>*<pos=助詞><pos=動詞>')
print matcher
pattern.find(ms, matcher, show)
