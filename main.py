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
        self.settings = config.Config()
        login = True
        address      = self.settings.get_address
        pw           = "*"*len(self.settings.get_password)
        maddr, mport, _ = self.settings.get_map
        saddr, sport, _ = self.settings.get_smtp
        print(f"Addr:\t{address}\npw:\t{pw}\nMAP:\t{maddr},\t{mport}\nSMTP:\t{saddr},\t{sport}")
        return "No Security", b"", login

    def new_user(self, key):
        return "Not Implemented", b""

    def inbox(self):
        self.mailbox   = mailer.Mailbox(self.settings)
        status_message = self.mailbox.status_message
        self.mailbox.get_mail()
        return status_message

    def logout(self):
        self.mailbox.close_mailbox()
        return "Logged out"

    def compose_mail(self):
        return "Not Implemented"

    def address_book(self):
        return "Not Implemented"


    def menu_logged_in(self, key, status_message):
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
            status_message = self.logout()
            login = False
            go = False

        return go, key, login, status_message


    def menu_logged_out(self, key, status_message):
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
        go = True
        while go == True:
            print("\<<<<< SEEC - Secure Email Client >>>>>\n")
            if login:
                try:
                    go, key, login, status_message = self.menu_logged_in(key, status_message)
                except:
                    try:
                        status_message = self.logout()
                    except imaplib.IMAP4.error:
                        pass # If already logged out
                    print(f"\n:: {status_message}")
                    raise
            else:
                go, key, login, status_message = self.menu_logged_out(key, status_message)
        return status_message


def main():

    # Login
    # Inbox
    # Read Mail
    #
    p = ProgramState()
    status_message = p.menu()
    print(f"\n:: {status_message}")


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        sys.exit(e)
    except KeyboardInterrupt:
        sys.exit("\nCtrl + C was pressed. Terminating")
    # except:
    #     sys.exit("Error: Program terminated unexpectedly")
