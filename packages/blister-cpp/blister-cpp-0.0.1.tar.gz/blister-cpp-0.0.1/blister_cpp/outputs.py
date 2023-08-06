from os import getcwd, makedirs

def get_filename(file):
    return '{0}/build/{1}'.format(getcwd(), file)

def create_file(file):
    return open(get_filename(file), 'w')

def create_dir(rel=''):
    try:
        makedirs(get_filename(rel))
    except OSError:
        pass
