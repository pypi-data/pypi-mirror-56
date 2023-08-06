import os
import re
import subprocess


def virtualenv_info(palette):

    VIRTUAL_ENV = os.environ.get('VIRTUAL_ENV')
    if not VIRTUAL_ENV:
        return None

    # Run using virtualenv's Python interpreter
    py_version_tag = subprocess.check_output([
        'python', '-c',
        "import sys;"
        "print('{0.name}-{0.version[0]}.{0.version[1]}.{0.version[2]}'"
        ".format(sys.implementation))"]).decode().strip()

    venv_path = shorten_path(VIRTUAL_ENV)

    prefix = palette['virtualenv.prefix'](py_version_tag + ':')
    path = palette['virtualenv.path'](venv_path)

    return ''.join((prefix, path))


def shorten_path(path):

    # re.sub('^' + os.environ.get('HOME') + '(/.*)?$', '~\\1', '/home/samu/a')

    start_list = os.getcwd().split(os.path.sep)
    path_list = path.split(os.path.sep)
    i = len(os.path.commonprefix([start_list, path_list]))

    if i > 1:
        rel_path_list = path_list[i:]
        if len(rel_path_list) == 0:
            return '.'
        return os.path.join(*rel_path_list)

    return user_prefix(path)


def user_prefix(path):
    try:
        home = os.environ['HOME']
    except KeyError:
        return path

    re_user_folder = r'^{}(/.*)?$'.format(re.escape(home))
    return re.sub(re_user_folder, '~\\1', path)
