## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## UI - SEEC UI Elements
## 13. Mar. 2024

import curses, textpad

TITLE = "<<< SEEC - Secure Encrypted Email Client >>>"

KEY_UP = 65
KEY_DOWN = 66
KEY_Q = [113, 81]

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
        self.foot = curses.newwin( 1, w-1, h-1, 0 )     # Footer Window
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

    def show_message(self, msg):
        pad = textpad.TextPad(TITLE_HEIGHT, HEADER_HEIGHT, FOOTER_HEIGHT, self.screen_width, self.screen_height, len(examplemsg))
        pad.show_message(msg)

    def show_status_message(self, msg):
        self.addstr_cntr(msg, env=self.foot)
        self.foot.refresh()

    def show_key(self, key):
        self.foot.clear()
        if key in KEY_Q:
            self.foot.addstr(0,5, "QUIT", REVERSE)
        elif key == KEY_UP:
            self.foot.addstr(0,5, " UP ", REVERSE)
        elif key == KEY_DOWN:
            self.foot.addstr(0,5, "DOWN", REVERSE)
        else:
            self.foot.addstr(0,5, "    ", REVERSE)
        if key == "end":
            self.foot.addstr(0,5, "END ", REVERSE)
        elif key == "top":
            self.foot.addstr(0,5, "TOP ", REVERSE)
        self.foot.addstr(0,0,str(key))
        self.foot.refresh()

def main(scr):
    ui  = UI(scr)
    screen_width, screen_height = ui.get_size()
    ui.show_title()
    ui.show_message(examplemsg)

    #scr.getch()

curses.wrapper(main)
