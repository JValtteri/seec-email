#!/usr/bin/python
# SEEC - Secure Encrypted Email Client
# Programming project for Secure Programming course at TUNI
#
# Menu - Logged out
# 12. Apr. 2024

import config


def login_with(state, key):
    '''
    Logs in to each system
    '''
    # TODO: Main User login
    login = True

    # TODO: Decrypt config

    # Load config
    state.settings  = config.Config()

    # Login to email server
    status_message = state.mail_login()

    print(":: "+status_message)
    return "No Encryption", b"", login

def new_user(state, key):
    return "Not Implemented", b""

def menu(state, key, status_message):
    go = True
    login = False
    print("\t0 - Login")
    print("\t1 - New User")
    print("\tQ - Exit Program")
    print(f"\n:: {status_message}")
    selection = input("> ")

    if selection == "":
        status_message = ""

    elif selection in ["q", "Q"]:
        go = False

    elif selection == "0":
        status_message, key, login = login_with(state, key)

    else:
        status_message = f":: Woops, bad input: '{selection}'"
    return go, key, login, status_message
