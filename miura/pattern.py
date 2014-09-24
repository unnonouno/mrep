def find(s, m):
    result = []

    i = 0
    while i < len(s):
        skip = [None]
        def collect(s, pos):
            if skip[0] is None:
                result.append({
                    'match': s[0:pos],
                    'begin': i,
                    'end': i + pos,
                })
                skip[0] = pos

        m.match(s[i:], 0, collect)
        if skip[0] is not None:
            i += skip[0]
        else:
            i += 1

    return result

class Repeat(object):
    def __init__(self, matcher):
        self.matcher = matcher

    def match(self, s, pos, after):
        def check_after(s, nxt):
            if nxt != pos:
                self.match(s, nxt, after)
                after(s, nxt)

        self.matcher.match(s, pos, check_after)

    def __repr__(self):
        return '(* ' + repr(self.matcher) + ')'

class Condition(object):
    def __init__(self, func):
        self.func = func

    def match(self, s, pos, after):
        if pos < len(s) and self.func(s[pos]):
            after(s, pos + 1)

    def __repr__(self):
        return '.'

class Select(object):
    def __init__(self, left, right):
        self.left = left;
        self.right = right

    def match(self, s, pos, after):
        self.left.match(s, pos, after)
        self.right.match(s, pos, after)

    def __repr__(self):
        return '(OR ' + repr(self.left) + ' ' + repr(self.right) + ')'

class Sequence(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def match(self, s, pos, after):
        def apply_next(s, nxt):
            self.second.match(s, nxt, after)

        self.first.match(s, pos, apply_next)

    def __repr__(self):
        return repr(self.first) + ':' + repr(self.second)
