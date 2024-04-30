#!/usr/bin/python
# SEEC - Secure Encrypted Email Client
# Programming project for Secure Programming course at TUNI
#
# Menu - Main
# 12. Apr. 2024

import logged_in, logged_out

def menu(state, key=b"", status_message=""):
    go = True
    while go == True:
        print("\n<<<<< SEEC - Secure Email Client >>>>>\n")
        if state.logged_in:
            try:
                go, status_message = logged_in.menu(state, status_message)
            except:
                status_message = state.logout()
                print(f"\n:: {status_message}")
                raise   # for debug
        else:
            go, status_message = logged_out.menu(state, status_message)
    return status_message
