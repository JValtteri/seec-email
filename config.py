#!/usr/bin/python3
# -*- coding: utf-8 -*-
## Programming project for Secure Programming course at TUNI
##
## UI - SEEC Config
## Class for readinng and storing configurations
## 6. Apr. 2024

import yaml
import seecrypto


class ConfigurationError(Exception):
    """Exception raised for errors in the configuration."""

class Config():
    """Class for reading and storing configuration data"""

    def __init__(self, filename="config.yml", password=None):

        self.__address = ""
        self.__password = ""

        # Incoming
        self.__map_addr = ""
        self.__map_port = None
        self.__map_security = False

        # Outgoing
        self.__smtp_addr = ""
        self.__smtp_port = None
        self.__smtp_security = False

        try:
            self.__settings = self.__read_config(filename, password)
            self.__parse_settings()
            self.__settings = {}    # Empty the __settings dict
        except Exception:
            print("Encountered an error while reading config.")
            raise

    @property
    def get_password(self):
        """returns the password"""
        return self.__password

    @property
    def get_address(self):
        """Returns the user email address/username"""
        return self.__address

    @property
    def get_map(self):
        """
        Returns a map of IMAP server configuration
        for incoming mail.
        addr: address
        port: port
        security: bool
        """
        return {
            "addr": self.__map_addr,
            "port": self.__map_port,
            "security": self.__map_security
            }

    @property
    def get_smtp(self):
        """
        Returns a map of SMTP server configuration
        for outgoing mail.
        addr: address
        port: port
        security: bool
        """
        return {
            "addr": self.__smtp_addr,
            "port": self.__smtp_port,
            "security": self.__smtp_security
            }

    def __read_config(self, filename, password=None):
        """
        Reads the config file
        Optional [password] for encrypted config files
        Returns a dict of all settings.
        """
        if password:
            configfile = seecrypto.decrypt_file_in_memory(filename, password)
            settings = yaml.safe_load(configfile)
        else:
            with open(filename, 'r', encoding='utf-8') as configfile:
                settings = yaml.safe_load(configfile)
        return settings

    def __parse_settings(self):
        """Parses settings to config object"""
        self.__address     = self.__settings["address"]
        self.__password    = self.__settings["password"]

        # Incoming
        self.__map_addr    = self.__settings["map"]
        self.__map_port    = self.__settings["map_port"]
        self.__map_security = self.__settings["map_security"]

        # Outgoing
        self.__smtp_addr    = self.__settings["smtp"]
        self.__smtp_port    = self.__settings["smtp_port"]
        self.__smtp_security = self.__settings["smtp_security"]
