from subprocess import Popen, PIPE

import json
import re

from . import ninja, outputs

def gen():
    compile_commands = []
    cmdline_re = re.compile('.* (.+?[.](cpp|m)m?) .*')
    p = Popen(ninja.run('-t', 'commands'), stdout=PIPE)
    for line in [l.decode('utf-8') for l in p.stdout.readlines()]:
        m = cmdline_re.match(line)
        if m is None:
            continue

        compile_commands.append({
            'directory': outputs.get_filename(''),
            'command': line[:-1],
            'file': m.group(1),
        })

    # TODO: Abort if previous Ninja failed

    with outputs.create_file('compile_commands.json') as f:
        json.dump(compile_commands, f, indent=2)
