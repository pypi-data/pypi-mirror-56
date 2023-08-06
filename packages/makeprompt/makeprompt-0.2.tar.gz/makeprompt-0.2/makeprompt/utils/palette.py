import io


class ColorPalette:

    def __init__(self, colors):
        self.colorizers = {
            name: self._make_colorizer(color)
            for name, color in colors.items()
        }

    def __getitem__(self, key):
        return self.colorizers[key]

    def _make_colorizer(self, color):

        if not color:
            # Shortcut
            return lambda text: text

        def colorizer(text):

            output = io.StringIO()

            output.write('%{')
            output.write('[')
            output.write(color)
            output.write('m')
            output.write('%}')

            output.write(text)

            output.write('%{')
            output.write('[0m')
            output.write('%}')

            return output.getvalue()

        return colorizer


def load_color_palette(value):
    """Load a color palette, similar to LS_COLORS.

    Format looks like:

        red=31:bold_green=1;32
    """

    if not value:
        return {}

    colors = {}
    for item in value.split(':'):
        key, val = item.split('=', 1)
        colors[key] = val

    return colors
