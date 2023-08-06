# _*_ coding:UTF-8 _*_
"""
__author__ = 'shede333'
"""

import re

from .termcolor import colored


class SWTermColor(object):
    _string = None
    _color = None
    _bg_color = None
    _text_attrs = None

    def __init__(self, text=None, prefix_text=None, sep=", ", color=None, bg_color=None,
                 attrs=None):
        self._string = text
        self._prefix_text = prefix_text
        self._sep = sep
        self.color = color
        self.bg_color = bg_color
        self.text_attrs = attrs

    def p(self, *args, **kwargs):
        # 由于"print"在py2上是关键字，所以这个方法就命令为：p
        print(self.colored(*args, **kwargs))

    def colored(self, *args, **kwargs):
        if "sep" in kwargs:
            sep = kwargs["sep"]
            del kwargs["sep"]
        else:
            sep = self._sep
        if args:
            text = sep.join(args)
        else:
            text = self._string
        if self._prefix_text:
            text = self._prefix_text + (text if text else "")

        params = dict(color=self.color, on_color=self.bg_color, attrs=self.text_attrs)
        if kwargs:
            if "bg_color" in kwargs:
                kwargs["on_color"] = kwargs["bg_color"]
                del kwargs["bg_color"]
            params.update(kwargs)
        on_color = params.get("on_color", None)
        if on_color and (not on_color.startswith("on_")):
            params["on_color"] = "on_{}".format(on_color)

        return colored(text, **params)

    def __call__(self, *args, **kwargs):
        return self.colored(*args, **kwargs)

    def __str__(self):
        return self.colored()

    def __add__(self, other):
        return self.__str__() + other

    def __radd__(self, other):
        return other + self.__str__()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color_value):
        if self._color and color_value:
            p_content = "* warning color: {} 将会覆盖 {}".format(color_value, self._color)
            print(SWTermColor(p_content).c_red())
        self._color = color_value

    @property
    def bg_color(self):
        return self._bg_color

    @bg_color.setter
    def bg_color(self, bg_color_value):
        if self._bg_color and bg_color_value:
            p_content = "* warning bg_color: {} 将会覆盖 {}".format(bg_color_value, self._bg_color)
            print(SWTermColor(p_content).c_red())
        self._bg_color = bg_color_value

    @property
    def text_attrs(self):
        return self._text_attrs

    @text_attrs.setter
    def text_attrs(self, text_attrs_value):
        if not text_attrs_value:
            return
        if not self._text_attrs:
            self._text_attrs = []
        if isinstance(text_attrs_value, list):
            self._text_attrs.extend(text_attrs_value)
        else:
            self._text_attrs.extend(re.split(r'\W+', text_attrs_value.strip()))

    def c_red(self):
        self.color = "red"
        return self

    def c_green(self):
        self.color = "green"
        return self

    def c_yellow(self):
        self.color = "yellow"
        return self

    def c_blue(self):
        self.color = "blue"
        return self

    def c_magenta(self):
        self.color = "magenta"
        return self

    def c_cyan(self):
        self.color = "cyan"
        return self

    def c_white(self):
        self.color = "white"
        return self

    def b_grey(self):
        self.bg_color = "grey"
        return self

    def b_red(self):
        self.bg_color = "red"
        return self

    def b_green(self):
        self.bg_color = "green"
        return self

    def b_yellow(self):
        self.bg_color = "yellow"
        return self

    def b_blue(self):
        self.bg_color = "blue"
        return self

    def b_magenta(self):
        self.bg_color = "magenta"
        return self

    def b_cyan(self):
        self.bg_color = "cyan"
        return self

    def b_white(self):
        self.bg_color = "white"
        return self

    def a_bold(self):
        self.text_attrs = "bold"
        return self

    def a_dark(self):
        self.text_attrs = "dark"
        return self

    def a_underline(self):
        self.text_attrs = "underline"
        return self

    def a_blink(self):
        self.text_attrs = "blink"
        return self

    def a_reverse(self):
        self.text_attrs = "reverse"
        return self

    def a_concealed(self):
        self.text_attrs = "concealed"
        return self
