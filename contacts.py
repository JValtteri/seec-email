#!/usr/bin/python
# SEEC - Secure Encrypted Email Client
# Programming project for Secure Programming course at TUNI
#
# Module for managing Contacts
# 22. Apr. 2024

import yaml

class AddressBook():

    def __init__(self, filename="contacts.yml"):
        self.filename = filename
        self.contacts = []
        self.__load_contacts(filename)

    def __load_contacts(self, filename):
        """Loads contacts from file"""
        try:
            with open(filename, 'r') as contactfile:
                contacts = yaml.safe_load(contactfile)
                if contacts:
                    self.contacts = contacts
        except FileNotFoundError:
            self.contacts = []
            return f"Error: Could not find {filename}"
        else:
            return ""

    def __save_contacts(self):
        """Writes contacts to file"""
        with open(self.filename, 'w') as contactfile:
            yaml.dump(self.contacts, contactfile)

    def print_contacts(self):
        """Prints a formated list of contacts with their index numbers"""
        c = self.contacts
        try:
            for index in range(len(c)):
                print(f"[{index}]: {c[index]['name']}  \t{c[index]['addr']}")
        except KeyError:
            print(f"{self.filename} malformed")

    def get_address(self, index):
        """
        Fetches the contact at [index]
        Returns a dict of the selected contact
        """
        return self.contacts[index]

    def add_address(self, name, address):
        """
        Adds the given contact information to address book
        """
        self.contacts.append({'name': name, 'addr': address})
        self.__save_contacts()

