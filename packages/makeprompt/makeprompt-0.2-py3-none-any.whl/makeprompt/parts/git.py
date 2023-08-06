import re
import subprocess

PREFIX_TEXT = 'git:'
MARKER_DIRTY = '✗'
MARKER_CLEAN = '✓'


def git_status(palette):
    git_ref = _get_git_ref_name()

    if git_ref is None:
        return None

    # Strip ``refs/heads/`` prefix
    git_ref = re.sub(r'^refs/heads/', '', git_ref)

    dirty = _get_git_dirty()

    return '{}{}{}'.format(
        palette['git.prefix'](PREFIX_TEXT),
        git_ref,
        palette['git.dirty'](MARKER_DIRTY)
        if dirty else palette['git.clean'](MARKER_CLEAN))


def _get_git_ref_name():

    commands = [
        'git symbolic-ref HEAD'.split(),
        'git rev-parse --short HEAD'.split(),
    ]

    for command in commands:

        try:
            return subprocess.check_output(
                command,
                stderr=subprocess.DEVNULL).decode().strip()

        except FileNotFoundError:
            return None  # git command not found

        except subprocess.CalledProcessError:
            # Just keep trying
            pass

    return None


def _get_git_dirty():

    command = [
        'git', 'status',
        '--porcelain',
        '--ignore-submodules=dirty',  # requires >=1.7.2
        # '--untracked-files=no',
    ]

    result = subprocess.check_output(
        command, stderr=subprocess.DEVNULL).decode().strip()

    # Result lists dirty files. Empty result means no dirty.
    return bool(result)
