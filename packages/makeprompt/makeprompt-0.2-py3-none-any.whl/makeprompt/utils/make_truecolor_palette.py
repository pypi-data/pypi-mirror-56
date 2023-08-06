import sys
from makeprompt.utils.color import RGBColor


def main():
    print('MAKEPROMPT_COLORS=\'{}\''.format(
        ':'.join(_make_color_palette(sys.argv[1:]))
    ))


def _make_color_palette(items):
    for item in items:
        name, spec = item.split('=', 1)
        color = ';'.join(_make_color(spec))
        yield '{}={}'.format(name, color)


def _make_color(spec):

    colors = {
        idx: val
        for idx, val in enumerate(spec.split(';'))
    }

    fgcolor = colors.get(0)

    if fgcolor:
        col = RGBColor.from_hex(fgcolor)
        yield '3{}'.format(col.to_24bit())

    bgcolor = colors.get(1)

    if bgcolor:
        col = RGBColor.from_hex(bgcolor)
        yield '4{}'.format(col.to_24bit())


if __name__ == '__main__':
    main()
