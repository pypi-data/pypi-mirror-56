PREFIX_TEXT = 'jobs:'


def jobs_status(palette):
    prefix = palette['jobs.prefix'](PREFIX_TEXT)
    return '%1(j.{}%j .)'.format(prefix)
