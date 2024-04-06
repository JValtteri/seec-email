#!/usr/bin/python
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Main program
## 12. Mar. 2024

import sys
import config, mailer

class ProgramState():

    def __init__(self):
        self.login = False
        self.settings = None
        self.mailbox = None

    def login_with(self, key):
        settings = config.Config()
        self.settings = settings

        login = True

        address = settings.get_address()
        pw = settings.get_password()
        maddr, mport = settings.get_map()
        saddr, sport = settings.get_smtp()
        print(f"Addr: {address}\npw: {pw}\nMAP: {maddr}, {mport}\nSMTP: {saddr}, {sport}")

        return "No Security", b"", login

    def new_user(self, key):
        return "Not Implemented", b""

    def inbox(self):
        self.mailbox = mailer.Mailbox(self.settings.get_address(), self.settings.get_password())
        return "Inbox"

    def compose_mail(self):
        return "Not Implemented"

    def address_book(self):
        return "Not Implemented"


    def menu_logged_in(self, key=b"", status_message=""):
        go = True
        login = True
        print("\t0 - Show Inbox")
        print("\t1 - Write Mail")
        print("\t2 - Address Book")
        print("\tQ - Exit Program")
        print(f"\n:: {status_message}")
        selection = input("> ")

        if selection == "":
            status_message = ""
        elif selection == "0":
            status_message = self.inbox()
        elif selection == "1":
            status_message = self.compose_mail()
        elif selection == "2":
            status_message = self.address_book()
        elif selection in ["q", "Q"]:
            login = False
            go = False

        return go, key, login, status_message


    def menu_logged_out(self, key, status_message=""):
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
            status_message, key, login = self.login_with(key)

        else:
            status_message = f":: Woops, bad input: '{selection}'"
        return go, key, login, status_message


    def menu(self, key=b"", login=False, status_message=""):
        print("\<<<<< SEEC - Secure Email Client >>>>>\n")
        if login:
            go, key, login, status_message = self.menu_logged_in(key, status_message)
        else:
            go, key, login, status_message = self.menu_logged_out(key, status_message)

        return go, key, status_message


def main():

    # Login
    # Inbox
    # Read Mail
    #
    p = ProgramState()
    go = True
    key = b""
    status_message = ""
    while go == True:
        go, key, status_message = p.menu(key, status_message)


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        sys.exit(e)
    except KeyboardInterrupt:
        sys.exit("\nCtrl + C was pressed. Terminating")
    # except:
    #     sys.exit("Error: Program terminated unexpectedly")
