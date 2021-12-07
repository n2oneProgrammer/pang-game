class Converters:
    @staticmethod
    def color_str_to_tuple(color):
        if not len(color) == 7:
            return ValueError("Color format is incorrect (correct form is #000000)")
        red = int(color[1:2], 16)
        green = int(color[3:4], 16)
        blue = int(color[5:6], 16)

        return red, green, blue
