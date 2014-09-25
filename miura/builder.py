import miura.pattern as pattern
import re

# exp = sub EOF
# sub = s|sub | s
# s = seq | e
# seq = star seq | star
# star = factor '*' | factor 
# factor = (sub) | . | <>


# t = t* | t|t | et
# e = <> | . | (t)
#
# t = (t)t' | <>t' | .t'
# t' = epsilon | *t' | |tt' | t

class ParseError(Exception):
    pass

class InvalidCharacter(ParseError):
    def __init__(self, pos, expect, actual):
        self.pos = pos
        self.expect = expect
        self.actual = actual

    def __str__(self):
        if len(self.expect) == 1:
            subject = '"%s" is' % self.expect[0]
        else:
            except_last = ', '.join(['"%s"' % s for s in self.expect[:-1]])
            last = self.expect[-1]
            subject = '%s or "%s" are' % (except_last, last)
        return '%s expected, but "%s" is given' % (subject, self.actual)

def parse(s):
    _, t = exp(s, 0)
    return t

def consume(s, pos, c):
    if s[pos] != c:
        raise Exception('"%s" is expected, but "%s" is given' % (c, s[pos]))
    return pos + 1

def exp(s, pos):
    p, t = seq(s, pos)
    if p != len(s):
        raise Exception('"%s"' % s[p:])
    return p, t

def seq(s, pos):
    p, t = star(s, pos)
    return seq_rest(s, p, t)

def seq_rest(s, pos, t):
    if pos >= len(s):
        return (pos, t)
    c = s[pos]
    if c == '|':
        p, t2 = star(s, pos + 1)
        p, t_r = seq_rest(s, p, t2)
        return (p, pattern.Select(t, t_r))
    elif c == '<' or c == '.' or c == '(':
        p, t2 = star(s, pos)
        return seq_rest(s, p, pattern.Sequence(t, t2))
    else:
        return (pos, t)

def star(s, pos):
    p, t = term(s, pos)
    if p < len(s) and s[p] == '*':
        return (p + 1, pattern.Repeat(t))
    else:
        return (p, t)

def term(s, pos):
    if pos >= len(s):
        raise Exception('unexpected eos is found')
    c = s[pos]
    if c == '(':
        p, t = seq(s, pos + 1)
        p = consume(s, p, ')')
        return (p, t)
    elif c == '<':
        m = re.match(r'<([^>]+)=([^>]+)>', s[pos:])
        if not m:
            raise Exception('invalid match pattern')
        p = pos + m.end()
        return p, pattern.Condition(lambda x: m.group(1) in x and x[m.group(1)] == m.group(2))

    elif c == '.':
        return pos + 1, pattern.Condition(lambda x: True)
    else:
        raise Exception('"(", "<" or "." is expected, but "%s" is given' % c)
