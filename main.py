#!/usr/bin/python
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Main program
## 12. Mar. 2024

import sys
import state as s
import menu_main


def main():
    state             = s.ProgramState()
    status_message = menu_main.menu(state)
    print(f"\n:: {status_message}")

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        sys.exit(e)
    except KeyboardInterrupt:
        sys.exit("\nCtrl + C was pressed. Terminating")
    except:
         sys.exit("Error: Program terminated unexpectedly")
         raise      # TODO DEBUG
