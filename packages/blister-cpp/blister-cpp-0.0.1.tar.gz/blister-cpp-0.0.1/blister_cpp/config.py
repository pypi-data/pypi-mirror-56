from os import getcwd

import yaml

with open('{0}/bli.yaml'.format(getcwd())) as f:
    cached = yaml.full_load(f)

cached['variables'] = { 
    'clang': 'clang++',
    'linker': 'clang++',
    'cflags': '-O2',
    'ldflags': '-O2',
    **cached.get('variables', {})
}
