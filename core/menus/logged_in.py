#!/usr/bin/python3
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Menu - Logged in
## 12. Apr. 2024

from tui import ui
from core import contacts
from core.crypto import seecrypto
from core.crypto import key_utility
from core.utils import util


PGB_START = "-----BEGIN PGP MESSAGE-----"
PGP_END = "-----END PGP MESSAGE-----"

def __print_inbox(state):
    """
    Prints the content of the inbox
    """
    print("")
    index = 0
    for mail in state.mailbox.inbox:
        date, subject, from_addr, _ = state.mailbox.get_message_header(mail)
        print(f"{index}:\t{date}\t\t{subject}\t\t{from_addr}")
        index += 1

def inbox(state) -> str:
    """
    Interface for inbox
    """
    status_message = state.mailbox.update_inbox()
    while True:
        go, selection = ui.show_inbox(state.mailbox)
        print(":: "+status_message)
        if not go:
            status_message = "Exit"
            break
        if selection == '':
            status_message = ""
        else:
            try:
                message = state.mailbox.inbox[int(selection)]
                _, subj, fromwho, _ = state.mailbox.get_message_header(message)
                body = state.mailbox.get_message_body(message)
                message_lines = body.splitlines()
                encrypted = False
                if PGB_START in message_lines and PGP_END in message_lines:
                    encrypted = True
                    note = "ENCRYPTED"
                    status_message = "Press D to decrypt - Q to Quit"
                else:
                    note = "PLAIN TEXT"
                    status_message = "Press Q to Quit"
                key = ui.show_message(
                    message=message_lines,
                    from_field=fromwho,
                    to_field=state.address,
                    subject=subj,
                    header_note=note,
                    footer_note=status_message
                    )
                status_message = ""
                if key in ui.KEY_D and encrypted:
                    gpg = seecrypto.GPG()
                    decrypted_body, status_message = gpg.decrypt_with_key(body, state.passwd)
                    key = ui.show_message(
                        message=decrypted_body.splitlines(),
                        from_field=fromwho,
                        to_field=state.address,
                        subject=subj,
                        header_note="Decrypted",
                        footer_note=status_message
                        )
            except ValueError:
                status_message = "Invalid option"
            except IndexError:
                status_message = "Out of range"
    return status_message

def compose_mail(state, to_addr=None, encrypt=False):
    """
    Interface for composing an email message
    """
    # Address
    if not to_addr:
        to_addr = util.valid_input("To Address:\t", name='address')
    subject     = util.valid_input("Subject:\t", name='subject')
    if seecrypto.GPG().public_key_available(to_addr):
        selection = input("Encrypt (Y/n)\n> ")
        if selection != 'n':
            encrypt = True
    else:
        print("Warning\nNo public KEY available for this recipient.")
        print("This message WILL NOT BE ENCRYPTED.")
        selection = input("Do you want to send anyway? (Y/n)")
        if selection.upper() == 'N':
            return "Aborted"
    # Start email editor
    message_body = util.text_editor("Write your Email. Press ENTER three times to send")
    from_addr = state.address
    if encrypt:
        message_body, status_message = seecrypto.GPG().encrypt_with_key(message_body, to_addr)
        print(f":: {status_message}")
        if message_body == '':
            return "Message not ecrypted, sending aborted"
    # Create EmailMessage object
    message = state.mailbox.create_message(message_body, from_addr, to_addr, subject)
    print(":: Sending...")
    success = state.mailbox.send_mail(message)
    if not success:
        return "Sending failed"
    return "Sent successfully"

def __add_contact(A) -> str:
    print("Add Contact")
    name = input("Name: ")
    if not util.is_valid_input(name, mode='wide'):
        return "Illegal name field"
    address = input("Address: ")
    if not util.is_valid_input(address, mode='wide'):
        return "Illegal address field"
    A.add_address(name, address)
    return ''

def address_book(state) -> str:
    """
    Address book
    """
    A = contacts.AddressBook()
    status_message = ""
    while True:
        print("Contacts:")
        A.print_contacts()
        print("\nChoose a contact by typing its number")
        print("a = Add contact")
        print("q = Quit")
        print(f":: {status_message}")
        selection = input("> ")
        if selection == "":
            status_message = ""
        elif selection == "a":
            status_message =  __add_contact(A)
        elif selection == "q":
            return ""
        else:
            try:
                contact = A.get_address(int(selection))
            except TypeError:
                status_message = "Not a number"
            else:
                status_message = compose_mail(state, contact['addr'])
                return status_message

def menu(state, status_message) -> (bool, str):
    """
    Main menu for logged in user
    """
    go = True
    print("\t0 - Show Inbox")
    print("\t1 - Address Book")
    print("\t2 - Write Mail Message")
    print("\t3 - Export public key")
    print("\tQ - Log out")
    print(f"\n:: {status_message}")
    selection = input("> ")
    try:
        if selection == "":
            status_message = ""
        elif selection == "0":
            status_message = inbox(state)
        elif selection == "1":
            status_message = address_book(state)
        elif selection == "2":
            status_message = compose_mail(state)
        elif selection == "3":
            status_message = key_utility.show_key(state.address)
        elif selection.upper() == "Q":
            status_message = state.logout()
        else:
            status_message = f"Woops, bad input: '{selection}'"
    except util.ValidationError as e:
        status_message = e.__str__()
    except ui.UIException as e:
        status_message = e.__str__()
    except KeyboardInterrupt:
        status_message = "Ctrl + C was pressed."
    return go, status_message
