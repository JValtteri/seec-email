#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Programming project for Secure Programming course at TUNI
#
# UI - SEEC Config
# Class for readinng and storing configurations
# 6. Apr. 2024

import yaml, sys

class ConfigurationError(Exception):
    """Exception raised for errors in the configuration."""

class Config():

    def __init__(self, filename="config.yml"):

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
            self.__settings = self.__read_config(filename)
            self.__parse_settings()
            self.__settings = {}    # Empty the __settings dict
        except:
            print("Encountered a critical error while reading config.")
            raise

    @property
    def get_password(self):
        # TODO Change this to return a hashed password
        return self.__password

    @property
    def get_address(self):
        return self.__address

    @property
    def get_map(self):
        return {
            "addr": self.__map_addr,
            "port": self.__map_port,
            "security": self.__map_security
            }

    @property
    def get_smtp(self):
        return {
            "addr": self.__smtp_addr,
            "port": self.__smtp_port,
            "security": self.__smtp_security
            }

    def __read_config(self, filename):
        """
        Reads the config file
        returns a dict of all settings.
        """
        try:
            with open(filename, 'r') as configfile:
                settings = yaml.safe_load(configfile)

        except FileNotFoundError:
            sys.exit("Error: Could not find %s" % filename)

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

        print(f"{self.__settings['address']} -> {self.__address}")
