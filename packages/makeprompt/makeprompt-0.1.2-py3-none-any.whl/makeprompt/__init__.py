import io
from .utils.color import colorize, RGBColor
from .parts.git import git_status
from .parts.jobs import jobs_status
from .parts.virtualenv import virtualenv_info


# COLOR_USER = RGBColor.from_hex('#00695C')
# COLOR_HOST = RGBColor.from_hex('#009688')
# COLOR_PATH = RGBColor.from_hex('#FBC02D')
# COLOR_PROMPT = RGBColor.from_hex('#009688')

COLOR_USER = RGBColor.from_hex('#388E3C')
COLOR_HOST = RGBColor.from_hex('#C6FF00')
COLOR_PATH = RGBColor.from_hex('#F57C00')
COLOR_PROMPT = RGBColor.from_hex('#C6FF00')


def build_prompt():

    output = io.StringIO()
    output.write(colorize('%n', fg=COLOR_USER))
    output.write(colorize('@%m', fg=COLOR_HOST))
    output.write(' ')
    output.write(colorize('%~', fg=COLOR_PATH))
    output.write(' ')

    output.write(jobs_status())

    extra = filter(None, [
        git_status(),
        virtualenv_info(),
    ])
    output.write(' '.join(extra))

    output.write('\n')
    output.write(colorize('%#', fg=COLOR_PROMPT))
    output.write(' ')
    return output.getvalue()
