#!/usr/bin/python3
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## UI - SEEC UI Element: Footer
## Class for handling footer elements
## 19. Mar. 2024

import curses


class Footer():
    """
    An email message footer UI object
    """

    def __init__(self, screen_width, screen_height):
        REVERSE = curses.A_REVERSE
        #   Format: [["Text", Style, col_x_location], [...], [...]]
        self.cols = [["", 0, 0], ["", curses.A_REVERSE, 5], ["", REVERSE, 10]]
        self.foot = curses.newwin( 1, screen_width-1, screen_height-1, 0 )

    def render(self):
        """Draws the footer with the set content"""
        self.foot.clear()
        for col in self.cols:
            self.foot.addstr(0, col[2], col[0], col[1])
        self.foot.refresh()

    def set_text(self, txt, col=0, style=None, pos=None):
        """Sets the content of particular footer column"""
        self.cols[col][0] = txt
        if style != None:
            self.cols[col][1] = style
        if pos != None:
            self.cols[col][2] = pos

    def clear_all(self):
        """Clears the contents of the footer element"""
        self.foot.clear()
        for col in self.cols:
            col[0] = ""

    def show_key(self, key, txt=""):
        """
        A function to simultanously
        - set the content of two columns
        - and render the footer
        """
        self.set_text(str(key), 0)
        self.set_text(txt, 1)
        self.render()
