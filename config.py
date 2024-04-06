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

        try:
            self.__settings = self.__read_config(filename)
            self.__parse_settings()
            self.__settings = {}    # Empty the setting dict
        except:
            print("Encountered a critical error while reading config.")
            raise

        self.__address = ""
        self.__password = ""

        # Incoming
        self.__map_addr = ""
        self.__map_port = None
        self.__map_encrypt = ""

        # Outgoing
        self.__smpt_addr = ""
        self.__smpt_port = None
        self.__smpt_encrypt = ""


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
        self.__map_encrypt = ""

        # Outgoing
        self.__smpt_addr    = self.__settings["smtp"]
        self.__smpt_port    = self.__settings["smtp_port"]
        self.__smpt_encrypt = ""

