#!/usr/bin/python3
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## UI - SEEC UI Element: Textpad
## Class for handling scrollable text in an email.
## 19. Mar. 2024

import curses
from tui import footer


KEY_UP = 65
KEY_DOWN = 66
KEY_Q = [113, 81]
KEY_D = [100, 68]

class TextPad():
    """
    A scrollable text display UI object
    """

    def __init__(self, TITLE_HEIGHT, HEADER_HEIGHT, FOOTER_HEIGHT, screen_width, screen_height, len_msg):
        start_and_end_lines = 2                 # Refers to '===' decoration lines
        self.pad_top = HEADER_HEIGHT + TITLE_HEIGHT
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pad_width = screen_width-1
        self.pad_height = screen_height - HEADER_HEIGHT - TITLE_HEIGHT - FOOTER_HEIGHT
        self.pad_bottom = screen_height - FOOTER_HEIGHT - 2
        self.pad_content_length = len_msg + start_and_end_lines
        self.pad = curses.newpad(len_msg+3, self.pad_width+1)
        self.foot = footer.Footer(self.screen_width, self.screen_height)

    def show_message(self, msg):
        """Adds the [msg] text to the element, wrapping it"""
        self.pad.addstr(0, 0, "="*self.pad_width) ## Add start line
        row = self.__print_message(msg)
        self.pad.addstr(row+1, 0, "="*self.pad_width)
        row = 0
        key = ''
        status = ''
        go = True
        while go:
            self.foot.show_key(key, status)
            go, row, key, status = self.__scroll(row)
        return key

    def refresh(self, row=0):
        """Wrapper for curses.pad.refresh"""
        self.pad.refresh(row, 0, self.pad_top, 0, self.pad_bottom, self.pad_width)

    def __print_message(self, msg):
        """
        Splits text in to rows that fit in the window
        show_message() uses this for wrapping the text
        """
        row = 1
        for line in msg:
            line_done = False
            while not line_done:
                if len(line) > self.pad_width:
                    part_line = line[:self.pad_width]
                    line = line[self.pad_width:]
                    self.pad.addstr(row, 0, part_line)
                else:
                    self.pad.addstr(row, 0, line)
                    line_done = True
                row += 1
                self.refresh(0)
                if row >= self.pad_content_length-2:
                    self.pad_content_length += 1
                    self.pad.resize(self.pad_content_length, self.pad_width)
                    self.refresh(0)
        return row

    def __scroll(self, row):
        """
        Gets key presses and translates them in to
        scroll and other actions.
        """
        self.refresh(row)
        status = ""
        key = self.pad.getch()
        if key == KEY_UP and row > 0:
            row -= 1
            status = " UP "
        elif key == KEY_DOWN and row < self.pad_content_length - self.pad_height:
            row += 1
            status = "DOWN"
        elif key in KEY_Q:
            status = "QUIT"
            return False, row, key, status
        elif key in KEY_D:
            status = "DECR"
            return False, row, key, status
        if row < 1:
            status = "TOP"
        if row >= self.pad_content_length - self.pad_height:
            status="END"
        return True, row, key, status
