import math


# properties

class DrawingChars:
    def __init__(self):
        self.ud = '│'
        self.ur = '┌'
        self.dr = '└'
        self.ru = '┘'
        self.rd = '┐'
        self.lr = '─'

        self.ilr = '_'
        self.oin = '┼'
        self.din = '╳'
        self.dru = '╱'
        self.drd = '╲'


chrs = DrawingChars()


# fuctions

def calc_angle(v1, v2):
    return math.acos(clamp(v1.dot(v2)/abs(v1)*abs(v2), 0, 1))


def calc_distance(p1, p2, factors=(1, 1)):
    dx = (p2[0] - p1[0]) * factors[0]
    dy = (p2[1] - p1[1]) * factors[1]
    return math.hypot(dx, dy)


def clamp(val, minval, maxval):
    return max(min(val, maxval), minval)


def force_list(var):
    if isinstance(var, (int, float)):
        var = [var]
    elif not isinstance(var, list):
        var = list(var)
    return var


# text formatters

def assign_aspect(value, aspect):
    def deco(formatter):
        def wrapper():
            if aspect == 'style':
                formatter.style = value
            if aspect == 'color':
                formatter.color = value
            if aspect == 'bgcolor':
                if formatter.color == '38':
                    formatter.color = '30'
                formatter.background_color = value
        return wrapper
    return deco


ESCAPE = ['\033[', '\033[0m']
STYLES = {
    'none':         assign_aspect('0', 'style'),
    'bold':         assign_aspect('1', 'style'),
    'negative':     assign_aspect('2', 'style'),
    'negative2':    assign_aspect('5', 'style'),
    'underline':    assign_aspect('4', 'style'),
}
COLORS = {
    'black':    assign_aspect('30', 'color'),
    'red':      assign_aspect('31', 'color'),
    'green':    assign_aspect('32', 'color'),
    'yellow':   assign_aspect('33', 'color'),
    'blue':     assign_aspect('34', 'color'),
    'purple':   assign_aspect('35', 'color'),
    'cyan':     assign_aspect('36', 'color'),
    'white':    assign_aspect('37', 'color'),
    'none':     assign_aspect('38', 'color'),
}
BACKGROUND_COLORS = {
    'black':    assign_aspect('40m', 'bgcolor'),
    'red':      assign_aspect('41m', 'bgcolor'),
    'green':    assign_aspect('42m', 'bgcolor'),
    'yellow':   assign_aspect('43m', 'bgcolor'),
    'blue':     assign_aspect('44m', 'bgcolor'),
    'purple':   assign_aspect('45m', 'bgcolor'),
    'cyan':     assign_aspect('46m', 'bgcolor'),
    'white':    assign_aspect('47m', 'bgcolor'),
    'none':     assign_aspect('48m', 'bgcolor'),
}


class Formatter:
    class _AspectSetter:
        def __init__(self, outer, aspect_dict):
            aspects = aspect_dict.copy()
            [aspects.update({key: val(outer)}) for key, val in aspects.items()]
            self.__dict__ = aspects

    def __init__(self):
        # init aspacts
        self.style = None
        self.color = None
        self.background_color = None
        # formats
        self.set_style = self._AspectSetter(self, STYLES)
        self.set_color = self._AspectSetter(self, COLORS)
        self.set_background_color = self._AspectSetter(self, BACKGROUND_COLORS)
        # config
        self.set_style.none()
        self.set_color.none()
        self.set_background_color.none()

    def __repr__(self):
        return self.format('Hello! I am Formatter ' + str(id(self)))

    def format(self, text):
        fmt = [self.style, self.color, self.background_color]
        if all(fmt):
            text_out = (';'.join(fmt) + text).join(ESCAPE)
        else:
            text_out = text
        return text_out


# decorators
