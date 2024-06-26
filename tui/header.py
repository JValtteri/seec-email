#!/usr/bin/python3
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## UI - SEEC UI Element: Header
## Class for handling Header elements
## 5. Apr. 2024

import curses


class Header():
    """
    An email message header UI object
    Creates also a corresponding footer object
    """

    def __init__(self, TITLE_HEIGHT, HEADER_HEIGHT, screen_width):
        # Colors
        self.YELLOW = curses.color_pair(1)
        self.RED = curses.color_pair(2)
        self.BLUE = curses.color_pair(3)
        self.BOLD = curses.A_BOLD
        self.REVERSE = curses.A_REVERSE

        self.note = "<plaintext>"
        self.from_field = "from@mail.domain"
        self.to_field = "to@mail.domain"
        self.subject = " <no subject>"
        self.indent = 4
        self.screen_width = screen_width
        self._head = curses.newwin( HEADER_HEIGHT, screen_width-1, TITLE_HEIGHT, 0 )

    def set_text(self, from_field=None, to_field=None, subject=None, note=None):
        """Set the content the header fields"""
        if from_field:
            self.from_field = from_field
        if to_field:
            self.to_field = to_field
        if subject:
            self.subject = subject
        if note:
            self.note = note

    def render(self):
        """Draws the header object"""
        reverse_indent = self.screen_width-self.indent-len(self.note)-9
        self._head.clear()
        self._head.addstr(0, self.indent, "From:    "+self.from_field, self.YELLOW)
        self._head.addstr(1, self.indent, "To:      "+self.to_field, self.YELLOW)
        self._head.addstr(2, self.indent, "Subject: "+self.subject, self.YELLOW)
        self._head.addstr(1, reverse_indent, self.note, self.BOLD | self.BLUE | self.REVERSE)
        self._head.refresh()

    def clear_all(self):
        """clears the contents of the header element"""
        self._head.clear()
