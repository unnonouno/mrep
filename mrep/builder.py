import mrep.pattern as pattern
import re
from cStringIO import StringIO


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


class RedundantCharacters(ParseError):
    def __init__(self, pos, redundant):
        self.pos = pos
        self.redundant = redundant

    def __str__(self):
        return 'Redundant characters remain: "%s"' % self.redundant


class InvalidPattern(ParseError):
    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return 'Invalid morpheme pattern'


def parse(s):
    _, t = exp(s, 0)
    return t


def consume(s, pos, c):
    if pos >= len(s):
        raise InvalidCharacter(pos, c, 'EOS')
    if s[pos] != c:
        raise InvalidCharacter(pos, c, s[pos])
    return pos + 1


def exp(s, pos):
    p, t = seq(s, pos)
    if p != len(s):
        raise RedundantCharacters(p, s[p:])
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
    elif c == ')':
        return (pos, t)
    else:
        p, t2 = star(s, pos)
        return seq_rest(s, p, pattern.Sequence(t, t2))


def star(s, pos):
    p, t = term(s, pos)
    if p < len(s) and s[p] == '*':
        return (p + 1, pattern.Repeat(t))
    else:
        return (p, t)


def term(s, pos):
    if pos >= len(s):
        raise InvalidCharacter(pos, ['(', '<', '.'], 'EOS')
    c = s[pos]
    if c == '(':
        p, t = seq(s, pos + 1)
        p = consume(s, p, ')')
        return (p, t)
    elif c == '<':
        m = re.match(r'<([^>]+)=([^>]+)>', s[pos:])
        if not m:
            raise InvalidPattern(pos)
        p = pos + m.end()
        key = m.group(1)
        value = m.group(2)
        return p, pattern.Condition(lambda x: key in x and x[key] == value)

    elif c == '.':
        return pos + 1, pattern.Condition(lambda x: True)
    elif c in ['|', '*', ')']:
        raise InvalidCharacter(pos, ['(', '<', '.'], c)
    else:
        return surface(s, pos)


def surface(s, pos):
    buf = StringIO()
    escape = False
    for i, c in enumerate(s[pos:]):
        if escape:
            if c not in ['(', ')', '<', '.', '*', '|']:
                raise InvalidCharacter(pos + i,
                                       ['(', ')', '<', '.', '*', '|'], c)
                
            buf.write(c)
            escape = False

        else:
            if c in ['(', ')', '<', '.', '*', '|']:
                suf = buf.getvalue()
                return pos + i, pattern.Surface(suf)

            elif c == '\\':
                escape = True

            else:
                buf.write(c)

    if escape:
        raise InvalidCharacter(len(s),
                               ['(', ')', '<', '.', '*', '|'], 'EOS')

    return len(s), pattern.Surface(buf.getvalue())
