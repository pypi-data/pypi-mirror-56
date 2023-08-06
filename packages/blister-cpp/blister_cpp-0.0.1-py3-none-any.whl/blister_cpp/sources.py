import re, os

_import_re = re.compile('(?:export )?import ([A-Za-z0-9._]+);')
_export_re = re.compile('export module ([A-Za-z0-9._]+);')

def _list_imports(file):
    with open(file) as f:
        for line in f:
            m = _import_re.match(line)
            if m is None:
                continue
            
            yield '{0}'.format(m.group(1))

def _pch(basename):
    return 'modules/{0}.pcm'.format(basename)

def _build_deps(file):
    return [_pch(x) for x in _list_imports(file) if x[:3] != 'std']

def _find_module_name(file):
    with open(file) as f:
        for line in f:
            m = _export_re.match(line)
            if m is None:
                continue
            
            return '{0}'.format(m.group(1))

class Match:
    def __init__(self, folder, file):
        self.fold = folder
        self.rell = '{0}/{1}'.format(folder, file)
        self.full = '{0}/{1}/{2}'.format(os.getcwd(), folder, file)
        (self.base, ext) = os.path.splitext(file)
        if ext not in ['', '.png']:
            self.objf = '{0}.o'.format(self.rell)
            self.deps = _build_deps(self.full)
        if ext == '.cppm':
            self.pcmf = _pch(_find_module_name(self.full))

def list(folder, ext):
    extp = '.' + ext
    for file in os.listdir(folder):
        if file.endswith(extp):
            yield Match(folder, file)

def list_recursive(ext, prefix = './'):
    extp = '.' + ext
    for file in os.listdir(prefix):
        if file.endswith(extp):
            yield Match(prefix[2:-1], file)
        elif os.path.isdir(prefix + file):
            yield from list_recursive(ext, prefix + file + '/')

def list_dirs(folder):
    for file in os.listdir(folder):
        if os.path.isdir(folder + '/' + file):
            yield Match(folder, file)
