class Timing:
    def __init__(self, delta):
        self.min = delta
        self.max = delta
        self.acc = delta
        self.n = 1

    def add(self, delta):
        if delta < self.min: self.min = delta
        if delta > self.max: self.max = delta
        self.acc += delta
        self.n += 1

    def avg(self):
        return int(self.acc / self.n)

def run():
    timings = {}

    with open('build/.ninja_log') as ninja_log:
        for line in ninja_log:
            if line[0] == '#':
                continue

            (start, end, _, file, _) = line.split('\t')

            delta = int(end) - int(start)
            if file in timings:
                timings[file].add(delta)
            else:
                timings[file] = Timing(delta)

    with open('build/.bli_ninja_log', 'w') as bli_log:
        for file, timing in sorted(timings.items(), key=lambda kv: kv[1].avg()):
            bli_log.write(str(timing.avg()))
            bli_log.write('\t')
            bli_log.write(str(timing.min))
            bli_log.write('\t')
            bli_log.write(str(timing.max))
            bli_log.write('\t')
            bli_log.write(file)
            bli_log.write('\n')
