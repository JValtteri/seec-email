#!/usr/bin/python
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Menu - Logged out
## 12. Apr. 2024

import getpass
import config, seecrypto


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
    print("New User")
    name = input("Name: ")
    passwd_0 = getpass.getpass("       Password: ")
    passwd_1 = getpass.getpass("Retype Password: ")
    if passwd_0 != passwd_1:
        status_message = ":: Passwords didn't match"
        return status_message, b''
    # Salt and Hash the password
    # (Set and) Encrypt config
    # Generate PGP key
    gpg = seecrypto.GPG()
    status_message = f":: Password set for: {name}"
    email = input("Email address: ")
    status_message = gpg.generate_key_pair(name, email, password=passwd_0)
    return status_message, b'no key'

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
    elif selection == "1":
        status_message, key = new_user(state, key)

    else:
        status_message = f":: Woops, bad input: '{selection}'"
    return go, key, login, status_message
