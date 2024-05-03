#!/usr/bin/python
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## UI - SEEC UI Elements
## 13. Mar. 2024

import curses
import textpad
import footer
import header


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

class UI():
    """
    Main UI class
    Handles all curses Text UI elements
    """

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
        """Returns screen (width, height)"""
        return self.screen_width, self.screen_height

    def clear_scr(self):
        """Clears the screen from all elements"""
        self.scr.clear()
        self.scr.refresh()

    def addstr_cntr(self, text, line=0, parm=0, env=None):
        """
        Adds center justified text
        text = Displayed text
        line = Distance from the top of the screen
        parm = Style parameters
        env  = screen or window to draw on
        """
        if env is None:
            env = self.scr
        x = int( self.screen_width / 2 - len(text)/2 )
        env.addstr(line, x, text, parm)

    def show_title(self):
        """Draws a title element on the main screen"""
        self.addstr_cntr(TITLE, parm= self.YELLOW | BOLD, env=self.title)
        self.title.refresh()

    def show_header(self, from_field, to_field, subject, note=""):
        """
        Creates and draws an email header object on screen
        from_field = from email address
        to_field,  = to email address
        subject    = subject field
        note       = note in the corner about encryption status
        """
        head = header.Header(TITLE_HEIGHT, HEADER_HEIGHT, self.screen_width)
        head.set_text(from_field, to_field, subject, note)
        head.render()

    def show_message(self, msg, note=""):
        """
        Creates a TextPad object and renders the message [msg] body on it
        """
        pad = textpad.TextPad(
            TITLE_HEIGHT, HEADER_HEIGHT, FOOTER_HEIGHT,
            self.screen_width, self.screen_height, len(msg)
            )
        pad.foot.set_text(note, 2)
        key = pad.show_message(msg)
        return key


def __show_message(scr, message, from_field, to_field, subject, header_note, footer_note=""):
    """
    Renders a complete message UI
    Creates the UI instance, adds a title, header and shows the message
    """
    ui  = UI(scr)
    ui.show_title()
    ui.show_header(from_field, to_field, subject, header_note)
    key = ui.show_message(message, footer_note)
    ui.clear_scr()
    return key

def show_message(message="<empty>",
                 from_field=None,
                 to_field=None,
                 subject=None,
                 header_note="",
                 footer_note=""

    ):
    """
    Public entrypoint for showing a message
    """
    return curses.wrapper(
        __show_message,
        message,
        from_field,
        to_field,
        subject,
        header_note,
        footer_note
        )
