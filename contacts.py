#!/usr/bin/python
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Module for managing Contacts
## 22. Apr. 2024

import yaml


class AddressBook():
    """Address book object"""

    def __init__(self, filename="contacts.yml"):
        self.filename = filename
        self.contacts = []
        self.__load_contacts(filename)

    def __load_contacts(self, filename) -> str:
        """Loads contacts from file"""
        try:
            with open(filename, 'r', encoding="utf-8") as contactfile:
                contacts = yaml.safe_load(contactfile)
                if contacts:
                    self.contacts = contacts
        except FileNotFoundError:
            self.contacts = []
            return f"Error: Could not find {filename}"
        return ""

    def __save_contacts(self) -> None:
        """Writes contacts to file"""
        with open(self.filename, 'w', encoding="utf-8") as contactfile:
            yaml.dump(self.contacts, contactfile)

    def print_contacts(self) -> None:
        """Prints a formated list of contacts with their index numbers"""
        try:
            for index, contact in enumerate(self.contacts):
                print(f"[{index}]: {contact['name']}  \t{contact['addr']}")
        except KeyError:
            print(f"{self.filename} malformed")

    def get_address(self, index) -> dict:
        """
        Fetches the contact at [index]
        Returns a dict of the selected contact
        """
        return self.contacts[index]

    def add_address(self, name, address) -> None:
        """
        Adds the given contact information to address book
        """
        self.contacts.append({'name': name, 'addr': address})
        self.__save_contacts()
