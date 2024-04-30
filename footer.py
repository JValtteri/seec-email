## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## UI - SEEC UI Element: Footer
## Class for handling footer elements
## 19. Mar. 2024

import curses

class Footer():

    def __init__(self, screen_width, screen_height):

        #   Format: [["Text"],   [Style],              [col_x_location]]
        self.cols = [["", 0, 0], ["", curses.A_REVERSE, 5], ["", 0, 10]]
        # Footer window
        self.foot = curses.newwin( 1, screen_width-1, screen_height-1, 0 )

    def render(self):
        self.foot.clear()
        for col in self.cols:
            self.foot.addstr(0, col[2], col[0], col[1])
        self.foot.refresh()

    def set_text(self, txt, col=0, style=None, pos=None):
        self.cols[col][0] = txt
        if style != None:
            self.cols[col][1] = style
        if pos != None:
            self.cols[col][2] = pos

    def clear_all():
        self.foot.clear()
        for col in self.cols:
            col[0] = ""

    def show_key(self, key, txt=""):
        self.set_text(str(key), 0)
        self.set_text(txt, 1)
        self.render()
