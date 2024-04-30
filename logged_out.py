#!/usr/bin/python
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Menu - Logged out
## 12. Apr. 2024

import getpass
import seecrypto
import help


def login_with(state, passwd):
    '''
    Logs in to each system
    '''
    # Loads config
    success, status_message = state.login(passwd)
    if not success:
        return status_message
    # Login to email server
    status_message = state.mail_login()
    print(":: "+status_message)
    return "No Encryption"

def new_user(state):
    print("New User")

    # Print warnings about importing config.yml
    print("IMPORTING CONFIG\n")
    for warning in help.IMPORT_WARNING:
        print(warning.strip())
        input()
    choise = input("Do you want to proceed?\n(y/N)\n> ")

    if choise not in ['Y', 'y']:
        return "Aborted"

    # Print all the security warnings
    print("\nNOTE!")
    for disclaimer in help.SECURITY_DISCLAIMERS:
        print(disclaimer.strip())
        input()

    # Set the password
    name = input("Name: ")
    passwd   = getpass.getpass("       Password: ")
    passwd_1 = getpass.getpass("Retype Password: ")
    if passwd != passwd_1:
        status_message = "Passwords didn't match"
        return status_message

    # Generate PGP key
    gpg = seecrypto.GPG()
    status_message = f"Password set for: {name}"
    email = input("Email address: ")
    status_message = gpg.generate_key_pair(name, email, password=passwd)
    print("Your Public key:")
    print(gpg.export_public_key(uid=email))

    # (Set and) Encrypt config
    seecrypto.encrypt_file_in_place("config.yml", passwd)

    return status_message

def menu(state, status_message):
    go = True
    print("\t0 - Login")
    print("\t1 - New User")
    print("\t2 - Import public key")
    print("\t3 - Export public key")
    print("\tQ - Exit Program")
    print(f"\n:: {status_message}")
    selection = input("> ")

    if selection == "":
        status_message = ""

    elif selection in ["q", "Q"]:
        go = False
    elif selection == "0":
        passwd = getpass.getpass("password: ")
        status_message = login_with(state, passwd)
    elif selection == "1":
        status_message = new_user(state)
    elif selection == "2":
        print("Import not implemented")
    elif selection == "3":
        print("Export not implemented")
    else:
        status_message = f":: Woops, bad input: '{selection}'"
    return go, status_message
