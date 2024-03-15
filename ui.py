## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## UI - SEEC UI Elements
## 13. Mar. 2024

import curses, time

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
        self.h = h
        self.w = w

        self.scr = scr                                  # Main screen
        self.title = curses.newwin( 1, w-1, 0, 0 )      # Title Window
        self.foot = curses.newwin( 1, w-1, h-1, 0 )     # Footer Window
        self.win = curses.newwin( h-1, w-1, 1, 1 )      # Content Window

    def clear_scr():
        self.scr.clear()
        self.scr.refresh()

    def addstr_cntr(self, text, line=0, parm=0, env=None):
        if env == None:
            env = self.scr
        x = int( self.w / 2 - len(text)/2 )
        env.addstr(line, x, text, parm)

    def show_title(self):
        self.addstr_cntr(TITLE, parm= self.YELLOW | BOLD, env=self.title)
        self.title.refresh()

    def show_message(self, msg):
        PAD_TOP = HEADER_HEIGHT + TITLE_HEIGHT
        pad_width = self.w-1
        pad_height = self.h - HEADER_HEIGHT - TITLE_HEIGHT - FOOTER_HEIGHT
        pad_content_length = len(msg)+1
        PAD_TOP = HEADER_HEIGHT + TITLE_HEIGHT
        pad = curses.newpad(len(msg)+1, pad_width+1)
        #self.scr.refresh()
        pad.addstr(0, 0, "===============") ################
        ###pad.addstr(pad_height-1, 0, "===============") ################
        row = 1
        #pad.getch() #############
        for line in msg:
            #print(f"=={len(line)}==")
            pad.getch() #############
            line_done = False
            while not line_done:
                if len(line) > pad_width:
                    part_line = line[:pad_width]
                    line = line[pad_width:]
                    #print(part_line) #######################
                    pad.addstr(row, 0, part_line)
                else:
                    pad.addstr(row, 0, line)
                    line_done = True
                row += 1
                pad.refresh(0, 0, PAD_TOP, 0, pad_height, pad_width)
                if row >= pad_content_length-2:
                    self.show_status_message(f"====resize {pad_content_length} -> ___ ===")
                    old_length = pad_content_length
                    #pad.getch()
                    #pad.addstr(f"====resize {pad_height} ->")
                    pad_content_length += 10
                    pad.resize(pad_content_length, pad_width)
                    pad.refresh(0, 0, PAD_TOP, 0, pad_height, pad_width)
                    #pad_addstr(f" {pad_height}====", end='')
                    self.show_status_message(f"====resize {old_length} -> {pad_content_length} ===")
            pad.getch()
#            break

        row = 0
        while True:
            pad.refresh(row, 0, PAD_TOP, 0, pad_height, pad_width)
            key = pad.getch()
            if key == KEY_UP:
                row -= 1
            elif key == KEY_DOWN:
                row += 1
            elif key in KEY_Q:
                break
            self.show_key(key)

    def show_status_message(self, msg):
        self.addstr_cntr(msg, env=self.foot)
        self.foot.refresh()

    def show_key(self, key):
        self.foot.clear()
        if key in KEY_Q: #
            self.foot.addstr(0,5, "QUIT", REVERSE)
        elif key == KEY_UP:
            self.foot.addstr(0,5, " UP ", REVERSE)
        elif key == KEY_DOWN:
            self.foot.addstr(0,5, "DOWN", REVERSE)
        else:
            self.foot.addstr(0,5, "    ", REVERSE)
        self.foot.addstr(0,0,str(key))
        self.foot.refresh()

def main(scr):
    ui=UI(scr)
    ui.show_title()
    ui.show_message(examplemsg)
    #scr.getch()

curses.wrapper(main)
