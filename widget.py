# -*- coding: utf-8 -*-

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"


class Widget(object):
    def __init__(self):
        pass

    def update(self):
        pass

    def on_event(self, event):
    	pass

    def destroy(self):
        pass


def Text(Widget):
    pass


def Image(Widget):
    pass


def Button(Widget):
    def __init__(self):
    	pass

    def on_event(self, event):
    	pass

    def on_click(self):
    	pass

    def on_hover(self):
    	pass