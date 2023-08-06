import os
import subprocess

from makeprompt.utils.color import RGBColor, colorize

COLOR_PREFIX = RGBColor.from_hex('#E91E63')
COLOR_FADE = RGBColor.from_hex('#880E4F')


def virtualenv_info():
    VIRTUAL_ENV = os.environ.get('VIRTUAL_ENV')
    if not VIRTUAL_ENV:
        return None

    # Run using virtualenv's Python interpreter
    py_version_tag = subprocess.check_output([
        'python', '-c',
        "import sys;"
        "print('{0.name}-{0.version[0]}.{0.version[1]}.{0.version[2]}'"
        ".format(sys.implementation))"]).decode().strip()

    venv_rel_path = os.path.relpath(VIRTUAL_ENV)

    return '{}{}'.format(
        colorize(py_version_tag, fg=COLOR_PREFIX),
        colorize('[{}]'.format(venv_rel_path), fg=COLOR_FADE))
