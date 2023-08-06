from makeprompt.utils.color import RGBColor


class Test__RGBColor:

    class Test__RGBColor__from_hex:

        def test_parse_valid_color(self):
            color = RGBColor.from_hex('#ff9900')
            assert color == RGBColor(1.0, 0.6, 0.0)

        def test_parse_valid_short_color(self):
            color = RGBColor.from_hex('#f90')
            assert color == RGBColor(1.0, 0.6, 0.0)
