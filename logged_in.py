#!/usr/bin/python
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Menu - Logged in
## 12. Apr. 2024

import getpass
import ui, contacts, seecrypto

PGB_START = "-----BEGIN PGP MESSAGE-----"
PGP_END = "-----END PGP MESSAGE-----"

def __print_inbox(state):
    print("")
    index = 0
    for mail in state.mailbox.inbox:
        date, subject, from_addr, to_addr = state.mailbox.get_message_header(mail)
        print(f"{index}:\t{date}\t\t{subject}\t\t{from_addr}")
        index += 1


def inbox(state):
    status_message = state.mailbox.update_inbox()
    while True:
        __print_inbox(state)
        print(":: "+status_message)
        selection = input("> ")
        if selection in ['q', 'Q']:
            status_message = "Exit"
            break
        elif selection == '':
            status_message = ""
        else:
            try:
                #state.mailbox.open_message(int(selection))
                message = state.mailbox.inbox[int(selection)]
                date, subj, fromwho, _ = state.mailbox.get_message_header(message)
                body = state.mailbox.get_message_body(message)
                message_lines = body.splitlines()
                encrypted = False
                if PGB_START in message_lines and PGP_END in message_lines:
                    encrypted = True
                    note = "ENCRYPTED"# todo
                    status_message = "Press D to decrypt"
                else:
                    note = "PLAIN TEXT"
                    status_message = ""
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
                    decrypted_body, status_message = seecrypto.GPG().decrypt_with_key(body, state.passwd)
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
    # Address
    if not to_addr:
        to_addr = input("To Address:\t")
    # TODO: Option to use contacts
    subject = input("Subject:\t")
    # Start email editor
    print("Write your Email. Press ENTER three times to send")
    print("="*43)
    lines = []
    line = "<None>"
    empty_lines = 0
    while empty_lines < 2:
        line = input("")
        lines.append(line)
        if line == "":
            empty_lines += 1
        else:
            empty_lines = 0
    print("="*43)
    message_body = "\n".join(lines)
    from_addr = state.address
    # TODO Encrypt if public key available
    if encrypt:
        message_body, status_message = seecrypto.GPG().encrypt_with_key(message_body, to_addr)
        print(f":: {status_message}")
        if message_body == '':
            return "Message not ecrypted, sending aborted"
    # Create EmailMessage object
    message = state.mailbox.create_message(message_body, from_addr, to_addr, subject)
    # Send message
    print(":: Sending...")
    success = state.mailbox.send_mail(message)
    if not success:
        return "Sending failed"
    return "Sent successfully"

def __add_contact(A):
    print("Add Contact")
    name = input("Name: ")
    address = input("Address: ")
    A.add_address(name, address)

def address_book(state):
    A = contacts.AddressBook()
    status_message = ""
    while True:
        encrypt = False
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
            __add_contact(A)
        elif selection == "q":
            return ""
        else:
            try:
                contact = A.get_address(int(selection))
            except TypeError:
                status_message = "Not a number"
                raise # TODO DEBUG
            else:
                if contact['key']:
                    selection = input("Encrypt (Y/n)\n> ")
                    if selection != 'n':
                        encrypt = True
                status_message = compose_mail(state, contact['addr'], encrypt)
                return status_message

def show_public_key(state):
    pub_key = seecrypto.GPG().export_public_key(state.address)
    print(pub_key)
    print("Copy the key, including the START and END lines.\n"+
          "and give to anyone you want to be able to send you\n"+
          "encrypted mail.\n")
    input("Press ENTER to return to menu.")
    return ""

def menu(state, status_message):
    go = True
    login = True
    print("\t0 - Show Inbox")
    print("\t1 - Write Mail")
    print("\t2 - Address Book")
    print("\t3 - Export public key")
    print("\tQ - Exit Program")
    print(f"\n:: {status_message}")
    selection = input("> ")

    if selection == "":
        status_message = ""
    elif selection == "0":
        status_message = inbox(state)
    elif selection == "1":
        status_message = compose_mail(state)
    elif selection == "2":
        status_message = address_book(state)
    elif selection == "3":
        status_message = show_public_key(state)
    elif selection in ["q", "Q"]:
        status_message = state.logout()
        go = False

    return go, status_message


