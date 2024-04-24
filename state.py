#!/usr/bin/python
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Menu - Main
## 12. Apr. 2024

import config, mailer


class ProgramState():
    '''
    Maintains the main program state
    '''

    def __init__(self):
        self.__logged_in = False
        self.__settings  = None
        self.mailbox     = None
        self.uid         = "<no name>"
        self.__passwd    = b''

    @property
    def logged_in(self) -> bool:
        """
        Returns whether state is "logged_in"
        """
        return self.__logged_in

    @property
    def address(self) -> str:
        """
        Returns the users email address
        """
        return __settings.get_address

    def login(self, passwd: bytes, uid=None) -> bool:
        """
        Loads configs and logs in to SEEC client
        """
        self.__logged_in = True
        if uid:
            self.uid     = uid
        self.__passwd    = passwd
        ########################
        # TODO: Decrypt config #
        ########################
        self.__settings  = config.Config()
        return True

    def logout(self) -> str:
        """
        Performs log out actions:
        - Closes email connection,
        - Clears configs
        - Clears passwords
        """
        self.mailbox.logout()
        self.__passwd    = b''
        self.uid         = "<no name>"
        self.mailbox     = None
        self.__settings  = None
        self.__logged_in = False
        return "Logged out"

    def mail_login(self) -> str:
        """
        Logs in to the configured email server.
        Returns a status message
        """
        ## Prints the email config ##
        address      = self.__settings.get_address
        pw           = "*"*len(self.__settings.get_password)
        imap         = self.__settings.get_map
        smtp         = self.__settings.get_smtp
        print(f"Addr:\t{address}\npw:\t{pw}\n")
        print(f"IMAP:\t{imap['addr']},\t{imap['port']}")
        print(f"SMTP:\t{smtp['addr']},\t{smtp['port']}")
        ####                     ####
        self.mailbox   = mailer.Mailbox(self.__settings)
        status_message = self.mailbox.status_message
        return status_message
