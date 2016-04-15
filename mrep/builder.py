import mrep.pattern as pattern
import re


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
        raise InvalidCharacter(pos, ['(', '<', '.'], 'EOS')
    c = s[pos]
    if c == '(':
        p, t = seq(s, pos + 1)
        p = consume(s, p, ')')
        return (p, t)
    elif c == '<':
        m = re.match(r'<([^>]+)=~([^>]+)>', s[pos:])
        if m:
            p = pos + m.end()
            key = m.group(1)
            pat = m.group(2)
            return p, pattern.Condition(
                lambda x: key in x and re.search(pat, x[key]))

        m = re.match(r'<([^>]+)=([^>]+)>', s[pos:])
        if m:
            p = pos + m.end()
            key = m.group(1)
            value = m.group(2)
            return p, pattern.Condition(lambda x: key in x and x[key] == value)

        raise InvalidPattern(pos)

    elif c == '.':
        return pos + 1, pattern.Condition(lambda x: True)
    else:
        raise InvalidCharacter(pos, ['(', '<', '.'], c)
