from makeprompt.utils.color import RGBColor, colorize

COLOR_JOBS = RGBColor.from_hex('#00897B')
PREFIX = colorize('jobs:', fg=COLOR_JOBS)


def jobs_status():
    return '%1(j.{}%j .)'.format(PREFIX)
