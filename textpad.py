#!/usr/bin/python
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## UI - SEEC UI Element: Textpad
## Class for handling scrollable text in an email.
## 19. Mar. 2024

import curses, footer

KEY_UP = 65
KEY_DOWN = 66
KEY_Q = [113, 81]
KEY_D = [100, 68]

class TextPad():

    def __init__(self, TITLE_HEIGHT, HEADER_HEIGHT, FOOTER_HEIGHT, screen_width, screen_height, len_msg):
        self.pad_top = HEADER_HEIGHT + TITLE_HEIGHT
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pad_width = screen_width-1
        self.pad_height = screen_height - HEADER_HEIGHT - TITLE_HEIGHT - FOOTER_HEIGHT
        self.pad_content_length = len_msg+1
        self.pad = curses.newpad(len_msg+1, self.pad_width+1)
        self.foot = footer.Footer(self.screen_width, self.screen_height)

    def show_message(self, msg):
        self.pad.addstr(0, 0, "="*self.pad_width) ## Add start line
        row = self.__print_message(msg)
        self.pad.addstr(row+1, 0, "="*self.pad_width)
        row = 0
        go = True
        while go:
            go, row, key, status = self.__scroll(row)
            self.foot.show_key((key, status))
        return key

    def __print_message(self, msg):
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
                self.pad.refresh(0, 0, self.pad_top, 0, self.pad_height, self.pad_width)
                if row >= self.pad_content_length-2:
                    self.pad_content_length += 10
                    self.pad.resize(self.pad_content_length, self.pad_width)
                    self.pad.refresh(0, 0, self.pad_top, 0, self.pad_height, self.pad_width)
        return row

    def __scroll(self, row):
        self.pad.refresh(row, 0, self.pad_top, 0, self.pad_height, self.pad_width)
        status = ""
        key = self.pad.getch()
        if key == KEY_UP and row > 0:
            row -= 1
            status = " UP "
        elif key == KEY_DOWN and row < self.pad_content_length-1:
            row += 1
            status = "DOWN"
        elif key in KEY_Q:
            status = "QUIT"
            return False, row, key, status
        elif key in KEY_D:
            status = "DECR"
            return False, row, key, status
        if row <= 1:
            status = "TOP"
        if row >= self.pad_content_length-2:
            status="END"
        return True, row, key, status

