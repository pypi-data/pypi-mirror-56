import re
import io


def colorize(text, fg=None, bg=None, bold=False):

    output = io.StringIO()

    output.write('%{')

    if bold:
        output.write('[1m')

    if fg is not None:
        if isinstance(fg, Color):
            output.write('[3{}m'.format(fg.to_8bit()))
            output.write('[3{}m'.format(fg.to_24bit()))

    if bg is not None:
        if isinstance(bg, Color):
            output.write('[4{}m'.format(bg.to_8bit()))
            output.write('[4{}m'.format(bg.to_24bit()))

    output.write('%}')

    output.write(text)

    output.write('%{[0m%}')

    return output.getvalue()


RE_HEX_COLOR = re.compile(
    r'^#?'
    r'(?P<r>[0-9a-f]{2})'
    r'(?P<g>[0-9a-f]{2})'
    r'(?P<b>[0-9a-f]{2})'
    r'$')

RE_HEX_COLOR_SHORT = re.compile(
    r'^#?'
    r'(?P<r>[0-9a-f])'
    r'(?P<g>[0-9a-f])'
    r'(?P<b>[0-9a-f])'
    r'$')


class Color:

    def __init__(self):
        raise ValueError('Cannot instantiate directly')

    def to_24bit(self):
        raise NotImplementedError('')

    def to_8bit(self):
        raise NotImplementedError('')


class RGBColor(Color):

    def __init__(self, red, green, blue):
        self._red = red
        self._green = green
        self._blue = blue

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self._red == other._red and
            self._green == other._green and
            self._blue == other._blue)

    def __repr__(self):
        return '{}({}, {}, {})'.format(
            self.__class__.__name__,
            self._red, self._green, self._blue)

    @classmethod
    def from_hex(cls, hex_color):

        hex_color = hex_color.lower()

        m = RE_HEX_COLOR.match(hex_color)

        if m is not None:
            red = int(m.group('r'), 16) / 255.0
            green = int(m.group('g'), 16) / 255.0
            blue = int(m.group('b'), 16) / 255.0
            return cls(red, green, blue)

        m = RE_HEX_COLOR_SHORT.match(hex_color)

        if m is not None:
            red = int(m.group('r'), 16) / 15.0
            green = int(m.group('g'), 16) / 15.0
            blue = int(m.group('b'), 16) / 15.0
            return cls(red, green, blue)

        raise ValueError('Bad HEX RGB color: {}'.format(hex_color))

    def to_24bit(self):
        return '8;2;{};{};{}'.format(
            int(self._red * 255),
            int(self._green * 255),
            int(self._blue * 255))

    def to_8bit(self):
        return '8;5;{}'.format(
            16 +
            int(self._red * 5) * 36 +
            int(self._green * 5) * 6 +
            int(self._blue * 5))
