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
            if matched[i] and (not matched[i - 1] or i == 0):
                out.write(self.begin)
            out.write(m['surface'])
            if (i == len(seq) - 1) or not matched[i + 1] and matched[i]:
                out.write(self.end)
            out.write(' ')
