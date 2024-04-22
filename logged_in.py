#!/usr/bin/python
# SEEC - Secure Encrypted Email Client
# Programming project for Secure Programming course at TUNI
#
# Menu - Logged in
# 12. Apr. 2024

import ui, contacts

def __print_inbox(state):
    index = 0
    for mail in state.mailbox.inbox:
        date, subject, from_addr, to_addr = state.mailbox.get_message_header(mail)
        print(f"{index}:\t{date}\t\t{subject}\t\t{from_addr}")
        index += 1


def inbox(state):
    status_message = state.mailbox.update_inbox()
    __print_inbox(state)
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
                #state.mailbox.open_message(int(selection))
                message = state.mailbox.inbox[int(selection)]
                date, subj, fromwho, _ = state.mailbox.get_message_header(message)
                body = state.mailbox.get_message_body(message)

                ui.show_message(
                    message=body.splitlines(),
                    from_field=fromwho,
                    subject=subj,
                    note=" DEBUG "
                    )

                #print(f"{date}, {subj}, {fromwho}")
                #print(body)
            except ValueError:
                status_message = "Invalid option"
            except IndexError:
                status_message = "Out of range"

    return status_message


def compose_mail(state, to_addr=None):
    # Address
    if not to_addr:
        to_addr = input("To Address:\t")
    # TODO: Option to use contacts
    subject = input("Subject:\t")
    # Start email editor
    print("Write your Email. Press ENTER twice to send")
    print("="*43)
    lines = []
    line = "<None>"
    while line != "":
        line = input("")
        lines.append(line)
    print("="*43)
    print(":: Sending...")
    message_body = "\n".join(lines)
    from_addr = state.settings.get_address
    # TODO Encrypt if public key available
    # Create EmailMessage object
    message = state.mailbox.create_message(message_body, from_addr, to_addr, subject)
    # Send message
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
            break
        else:
            try:
                contact = A.get_address(int(selection))
            except TypeError:
                status_message = "Not a number"
                raise # TODO DEBUG
            else:
                compose_mail(state, contact['addr'])

def menu(state, key, status_message):
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
        status_message = inbox(state)
    elif selection == "1":
        status_message = compose_mail(state)
    elif selection == "2":
        status_message = address_book(state)
    elif selection in ["q", "Q"]:
        status_message = state.logout()
        login = False
        go = False

    return go, key, login, status_message


