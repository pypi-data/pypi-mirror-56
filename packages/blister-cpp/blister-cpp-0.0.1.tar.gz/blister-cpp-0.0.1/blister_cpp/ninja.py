class Statement:
    def __init__(self, line, vars):
        self.line = line
        self.vars = vars
    
    def __setitem__(self, key, value):
        self.vars[key] = value

    def __getitem__(self, key):
        return self.vars[key]

    def write(self, f):
        f.write(self.line)
        f.write('\n')

        for k, v in self.vars.items():
            f.write('  ')
            f.write(k)
            f.write(' = ')
            f.write(v)
            f.write('\n')

        f.write('\n')

class BuildStatement(Statement):
    def __init__(self, out, rule, inp = '', deps = [], vars = {}):
        line = "build {0}: {1} {2} | {3}".format(out, rule, inp, " ".join(deps))
        super().__init__(line, vars)

        self.out = out

    def add_dependency(self, dep):
        self.line += ' ' + dep

    def write_default(self, f):
        self.write(f)

        f.write('default ')
        f.write(self.out)
        f.write('\n\n')

class BuildPhonyStatement(BuildStatement):
    def __init__(self, name):
        super().__init__(name, 'phony')

def run(*args):
    return ['ninja', '-C', 'build'] + list(args)
