#!/usr/bin/python
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## UI - SEEC UI Elements
## 13. Mar. 2024

import curses, textpad, footer, header

TITLE = "<<< SEEC - Secure Encrypted Email Client >>>"

KEY_UP = 65
KEY_DOWN = 66
KEY_Q = [113, 81]
KEY_D = [100, 68]

BOLD = curses.A_BOLD
REVERSE = curses.A_REVERSE

TITLE_HEIGHT  = 1
HEADER_HEIGHT = 4
FOOTER_HEIGHT = 1

################## FOR TESTING #################
import lorem_ipsum
examplemsg = lorem_ipsum.LOREM_IPSUM.split('\n')
################## FOR TESTING #################


class UI():

    def __init__(self, scr):
        # Init colors
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

        # Define styles
        self.YELLOW = curses.color_pair(1)
        self.WARNING = curses.color_pair(2)
        self.BLUE = curses.color_pair(2)

        h = curses.LINES
        w = curses.COLS
        self.screen_height = h
        self.screen_width = w

        self.scr = scr                                  # Main screen
        self.title = curses.newwin( 1, w-1, 0, 0 )      # Title Window
        self.foot = footer.Footer(self.screen_width, self.screen_height)
        # self.foot = curses.newwin( 1, w-1, h-1, 0 )     # Footer Window
        self.win = curses.newwin( h-1, w-1, 1, 1 )      # Content Window

    def get_size(self):
        return self.screen_width, self.screen_height

    def clear_scr():
        self.scr.clear()
        self.scr.refresh()

    def addstr_cntr(self, text, line=0, parm=0, env=None):
        if env == None:
            env = self.scr
        x = int( self.screen_width / 2 - len(text)/2 )
        env.addstr(line, x, text, parm)

    def show_title(self):
        self.addstr_cntr(TITLE, parm= self.YELLOW | BOLD, env=self.title)
        self.title.refresh()

    def show_header(self, from_field, to_field, subject, note):
        head = header.Header(
            TITLE_HEIGHT, HEADER_HEIGHT,
            self.screen_width, self.screen_height
            )
        head.set_text(from_field, to_field, subject, note)
        head.render()

    def show_message(self, msg):
        pad = textpad.TextPad(
            TITLE_HEIGHT, HEADER_HEIGHT, FOOTER_HEIGHT,
            self.screen_width, self.screen_height, len(examplemsg)
            )
        key = pad.show_message(msg)
        return key


def __show_message(scr, message, from_field, to_field, subject, note):
    ui  = UI(scr)
    ui.show_title()
    ui.show_header(from_field, to_field, subject, note)
    ui.show_message(message)

def show_message(message="<empty>", from_field=None,
                 to_field=None, subject=None, note=None):
    curses.wrapper(__show_message, message, from_field, to_field, subject, note)

if __name__ == "__main__":

    #scr.getch()
    show_message(examplemsg)
