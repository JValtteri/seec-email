#!/usr/bin/python
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Menu - Logged out
## 12. Apr. 2024

import getpass
import seecrypto
import key_utility
import util
import texts


def login_with(state, passwd) -> str:
    """
    Logs in to each system
    """
    # Loads config
    success, status_message = state.login(passwd)
    if not success:
        return status_message
    # Login to email server
    status_message = state.mail_login()
    if status_message != "Logged in to mailbox":
        state.logout()
        return status_message
    print(":: "+status_message)
    if passwd:
        return "Logged in"
    return "No Encryption"

def new_user() -> str:
    """
    Create a new user with a PGP key and Config
    """
    print("New User")
    print("IMPORTING CONFIG\n")
    for warning in texts.IMPORT_WARNING:
        print(warning.strip())
        input()
    choise = input("Do you want to proceed?\n(y/N)\n> ")
    if choise.upper() == 'Y':
        return "Aborted"
    print("\nNOTE!")
    for disclaimer in texts.SECURITY_DISCLAIMERS:
        print(disclaimer.strip())
        input()

    # Creates the PGP Key
    status_message, name, passwd = key_utility.make_gpg_key()

    # Encrypts the Config
    seecrypto.encrypt_file_in_place("config.yml", passwd)
    status_message = f"Password set for: {name}, {status_message}"
    return status_message

def menu(state, status_message) -> (bool, str):
    """
    Main Menu
    """
    go = True
    print("\t0 - Login")
    print("\t1 - New User")
    print("\t2 - Import public key")
    print("\t3 - Key Utilities")
    print("\tQ - Exit Program")
    print(f"\n:: {status_message}")
    selection = input("> ")
    try:
        if selection == "":
            status_message = ""
        elif selection in ["q", "Q"]:
            go = False
        elif selection == "0":
            passwd = util.valid_passwd("password: ")
            status_message = login_with(state, passwd)
        elif selection == "1":
            status_message = new_user()
        elif selection == "2":
            status_message =  key_utility.import_keys()
        elif selection == "3":
            key_utility.main()
        else:
            status_message = f":: Woops, bad input: '{selection}'"
    except util.ValidationError as e:
        status_message = e.__str__()
    return go, status_message
