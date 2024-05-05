#!/usr/bin/python
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## UI - SEEC UI Element: Textpad
## Class for handling email inbox.
## 19. Mar. 2024

import curses
import footer
import util


REVERSE = curses.A_REVERSE

KEY_UP = 65
KEY_DOWN = 66
ENTER = 10
KEY_Q = [113, 81]

class Inbox():
    """
    A key navigatable inbox UI object
    """

    def __init__(self, TITLE_HEIGHT, HEADER_HEIGHT, FOOTER_HEIGHT, screen_width, screen_height, mailbox):
        self.GREEN = curses.color_pair(4)
        self.WHITE = curses.color_pair(5)
        self.mailbox = mailbox
        self.pad_top = HEADER_HEIGHT + TITLE_HEIGHT
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pad_width = screen_width-1
        self.pad_height = screen_height - HEADER_HEIGHT - TITLE_HEIGHT - FOOTER_HEIGHT
        self.pad_content_length = len(mailbox.inbox)+3
        self.pad = curses.newpad(len(mailbox.inbox)+3, self.pad_width+1)
        self.foot = footer.Footer(self.screen_width, self.screen_height)

        self.focus_row = 0
        self.rows = 0

    def refresh(self):
        """Refreshes the inbox view"""
        self.pad.refresh(0, 0, self.pad_top, 0, self.pad_height, self.pad_width)

    def add_inbox_line(self, message, row):
        """
        Prints a single line of inbox
        """
        style = self.WHITE
        # Adapt to screen width
        column = []
        col_space = self.pad_width/3
        column.append(0)                # Index Number
        column.append(int(4))           # Date
        column.append(int(col_space))   # Subject
        column.append(int(col_space*2)) # From
        date, subject, addr, _ = self.mailbox.get_message_header(message)
        try:
            date = util.parse_date(date)
        except Exception:
            pass
        in_focus = row == self.focus_row
        if in_focus:
            style = REVERSE | self.GREEN
            self.pad.addstr(row, 0, " "*self.pad_width, style)  # Add inverted background
        else:
            self.pad.addstr(row, 0, " "*self.pad_width, style)  # Remove inverted background
        self.pad.addstr(row, column[0], str(row),       style)  # Add index
        self.pad.addstr(row, column[1], str(date),      style)  # Add date
        self.pad.addstr(row, column[2], str(subject),   style)  # Add subject
        self.pad.addstr(row, column[3], str(addr),      style)  # Add address

    def draw_inbox_lines(self):
        """
        Draws all inbox lines
        """
        max_height = self.pad_height
        index = 0
        for index, message in enumerate(self.mailbox.inbox):
            if not index < max_height:
                break
            self.add_inbox_line(message, index)
        self.rows = index
        self.foot.set_text("Inbox - Press Q to Quit", 2)
        self.foot.render()
        self.refresh()

    def __scroll(self, row):
        """
        Handles user input and movign focus between messages
        """
        key = self.pad.getch()
        if key == KEY_UP and row > 0:
            row -= 1
        elif key == KEY_DOWN and row < self.rows:
            row += 1
        return row, key

    def main(self):
        """
        Entrypoint for inbox
        """
        go = True
        row = self.focus_row
        self.draw_inbox_lines()
        while True:
            row, key = self.__scroll(row)
            self.focus_row = row
            self.draw_inbox_lines()
            if key == ENTER:
                break
                # go = True
                # row = row
            elif key in KEY_Q:
                go = False
                break
            self.refresh()
        return go, row
