#!/usr/bin/python
# SEEC - Secure Encrypted Email Client
# Programming project for Secure Programming course at TUNI
#
# Menu - Main
# 12. Apr. 2024

import logged_in, logged_out

def menu(state, key=b"", login=False, status_message=""):
    go = True
    while go == True:
        print("\<<<<< SEEC - Secure Email Client >>>>>\n")
        if login:
            try:
                go, key, login, status_message = logged_in.menu(state, key, status_message)
            except:
                status_message = state.logout()
                print(f"\n:: {status_message}")
                raise   # for debug
        else:
            go, key, login, status_message = logged_out.menu(state, key, status_message)
    return status_message

