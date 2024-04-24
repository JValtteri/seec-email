#!/usr/bin/python
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Menu - Main
## 12. Apr. 2024

import mailer


class ProgramState():
    '''
    Maintains the main program state
    '''

    def __init__(self):
        self.login    = False
        self.settings = None
        self.mailbox  = None

    def logout(self):
        self.mailbox.logout()
        return "Logged out"

    def mail_login(self):
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
