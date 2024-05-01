#!/usr/bin/python
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Menu - Logged out
## 12. Apr. 2024

import getpass
import seecrypto, key_view
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
    if status_message != "Logged in to mailbox":
        state.logout()
        return status_message
    print(":: "+status_message)
    if passwd:
        return "Logged in"
    return "No Encryption"

def new_user():
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


def import_keys():
    print("Paste the key(s) here. Press ENTER two times to confirm")
    print("Ctrl+C to cancel")
    lines = []
    line = "<None>"
    empty_lines = 0
    print("="*43)
    while empty_lines < 2:
        line = input("")
        lines.append(line.strip())
        if line == "":
            empty_lines += 1
        else:
            empty_lines = 0
    print("="*43)
    key_data = "\n".join(lines)
    gpg = seecrypto.GPG()
    ret_obj = gpg.import_public_key(key_data)
    try: print(ret_obj.ok)
    except: pass
    return ""

def list_keys():
    key_view.print_keys(str(seecrypto.GPG().list_keys()))

def del_key():
    id = input("Key ID to delete\n> ")
    obj = seecrypto.GPG().delete_key(id, False)
    return obj.status

def menu(state, status_message):
    go = True
    print("\t0 - Login")
    print("\t1 - New User")
    print("\t2 - Import public key")
    print("\t3 - List public keys")
    print("\t4 - Delete public key")
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
        status_message = new_user()
    elif selection == "2":
        status_message =  import_keys()
    elif selection == "3":
        list_keys()
    elif selection == "4":
        status_message = del_key()
    else:
        status_message = f":: Woops, bad input: '{selection}'"
    return go, status_message
