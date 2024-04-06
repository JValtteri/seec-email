#!/usr/bin/python
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Main program
## 12. Mar. 2024

import sys
import config

def login(key):
    c = config.Config()
    address = c.get_address()
    pw = c.get_password()
    maddr, mport = c.get_map()
    saddr, sport = c.get_smtp()
    print(f"Addr: {address}\npw: {pw}\nMAP: {maddr}, {mport}\nSMTP: {saddr}, {sport}")
    return "Not Implemented", b""

def new_user(key):
    return "Not Implemented", b""

def inbox():
    return "Not Implemented"

def compose_mail():
    return "Not Implemented"

def address_book():
    return "Not Implemented"


def menu_logged_in(key=b"", status_message=""):
    go = True
    print("\t0 - Show Inbox")
    print("\t1 - Write Mail")
    print("\t2 - Address Book")
    print("\tQ - Exit Program")
    selection = input("> ")

    if selection == "":
        status_message = ""
    elif selection == "0":
        status_message = inbox()
    elif selection == "1":
        status_message = compose_mail()
    elif selection == "2":
        status_message = address_book()
    elif selection in ["q", "Q"]:
        go = False

    return go, key, status_message


def menu_logged_out(key, status_message=""):
    go = True
    print("\t0 - Login")
    print("\t1 - New User")
    print("\tQ - Exit Program")
    print("\n" + status_message)
    selection = input("> ")

    if selection == "":
        status_message = ""

    elif selection in ["q", "Q"]:
        go = False

    elif selection == "0":
        status_message, key = login(key)

    else:
        status_message = f":: Woops, bad input: '{selection}'"
    return go, key, status_message


def menu(key=b"", login=False, status_message=""):
    print("\<<<<< SEEC - Secure Email Client >>>>>\n")
    if login:
        go, key, status_message = menu_logged_in(key, status_message)
    else:
        go, key, status_message = menu_logged_out(key, status_message)

    return go, key, status_message


def main():

    # Login
    # Inbox
    # Read Mail
    #

    go = True
    key = b""
    status_message = ""
    while go == True:
        go, key, status_message = menu(key, status_message)


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        sys.exit(e)
    except KeyboardInterrupt:
        sys.exit("\nCtrl + C was pressed. Terminating")
    # except:
    #     sys.exit("Error: Program terminated unexpectedly")
