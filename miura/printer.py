class Printer(object):
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def print_result(self, seq, results, out):
        matched = [False] * len(seq)
        for result in results:
            for i in range(result['begin'], result['end']):
                matched[i] = True

        for i, m in enumerate(seq):
            if i != 0:
                out.write(' ')
            if matched[i] and (not matched[i - 1] or i == 0):
                out.write(self.begin)
            out.write(m['surface'])
            if (i == len(seq) - 1 or not matched[i + 1]) and matched[i]:
                out.write(self.end)
        out.write('\n')


class OnlyMatchPrinter(object):
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def print_result(self, seq, results, out):
        for match in results:
            subseq = seq[match['begin']: match['end']]
            out.write(self.begin)
            out.write(' '.join([m['surface'] for m in subseq]))
            out.write(self.end)
            out.write('\n')
