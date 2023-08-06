from . import infoplist, preamble

def write_preamble(f):
    preamble.write(f)

def write_infoplist(f, **kwargs):
    infoplist.write(f, **kwargs)
