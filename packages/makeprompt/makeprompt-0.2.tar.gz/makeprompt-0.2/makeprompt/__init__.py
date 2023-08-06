import io
import os

from .parts.git import git_status
from .parts.jobs import jobs_status
from .parts.virtualenv import virtualenv_info
from .utils.palette import load_color_palette, ColorPalette


def build_prompt():

    palette = ColorPalette({

        # Green / orange default palette
        'user': '38;2;56;142;60',
        'host': '38;2;198;255;0',
        'path': '38;2;245;124;0',
        'prompt': '38;2;198;255;0',
        'prompt_root': '38;2;244;67;54',

        'git.prefix': '38;2;30;136;229',
        'git.dirty': '38;2;244;67;54',
        'git.clean': '38;2;76;175;80',

        'jobs.prefix': '38;2;0;137;123',

        'virtualenv.prefix': '38;2;245;0;87',
        'virtualenv.path': '38;2;136;14;79',

        **load_color_palette(os.environ.get('MAKEPROMPT_COLORS')),
    })

    output = io.StringIO()
    output.write(palette['user']('%n'))
    output.write(palette['host']('@%m'))
    output.write(' ')
    output.write(palette['path']('%~'))
    output.write(' ')

    # Visibility is handled by the shell.
    # Trailing space is only added if visible.
    output.write(jobs_status(palette=palette))

    extra = filter(None, [
        git_status(palette=palette),
        virtualenv_info(palette=palette),
    ])
    output.write(' '.join(extra))

    output.write('\n')

    prompt_root = palette['prompt_root']('#')
    prompt_user = palette['prompt']('%%')
    output.write('%(!.{}.{})'.format(prompt_root, prompt_user))

    output.write(' ')
    return output.getvalue()
