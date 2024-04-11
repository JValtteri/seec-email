#!/usr/bin/python
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Main program
## 12. Mar. 2024

import sys
import config, mailer
from imaplib import IMAP4

class ProgramState():
    '''
    Maintains the main program state
    '''

    def __init__(self):
        self.login    = False
        self.settings = None
        self.mailbox  = None

    def login_with(self, key):
        '''
        Logs in to each system
        '''
        # TODO: Main User login
        login = True
        # TODO: Decrypt config
        # Load config
        self.settings = config.Config()
        # Login to email server
        status_message = self.__mail_login()
        print(":: "+status_message)
        return "No Encryption", b"", login

    def __mail_login(self):
        address      = self.settings.get_address
        pw           = "*"*len(self.settings.get_password)
        imap         = self.settings.get_map
        smtp         = self.settings.get_smtp
        print(f"Addr:\t{address}\npw:\t{pw}\n")
        print(f"IMAP:\t{imap['addr']},\t{imap['port']}")
        print(f"SMTP:\t{smtp['addr']},\t{smtp['port']}")
        self.mailbox   = mailer.Mailbox(self.settings)
        status_message = self.mailbox.status_message ## TODO HERE!!!
        return status_message

    def __print_inbox(self):
        index = 0
        for mail in self.mailbox.inbox:
            date, subject, from_addr, to_addr = self.mailbox.get_message_header(mail)
            print(f"{index}:\t{date}\t\t{subject}\t\t{from_addr}")
            index += 1

    def new_user(self, key):
        return "Not Implemented", b""

    def inbox(self):
        status_message = self.mailbox.update_inbox()
        self.__print_inbox()
        while True:
            print(":: "+status_message)
            selection = input("> ")
            if selection in ['q', 'Q']:
                status_message = "Exit"
                break
            elif selection == '':
                status_message = ""
            else:
                try:
                    #self.mailbox.open_message(int(selection))
                    message = self.mailbox.inbox[int(selection)]
                    date, subj, fromwho, _ = self.mailbox.get_message_header(message)
                    body = self.mailbox.get_message_body(message)
                    print(f"{date}, {subj}, {fromwho}")
                    print(body)
                except ValueError:
                    status_message = "Invalid option"
                except IndexError:
                    status_message = "Out of range"

        return status_message

    def logout(self):
        self.mailbox.logout()
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
                    status_message = self.logout()
                    print(f"\n:: {status_message}")
                    raise   # for debug
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
