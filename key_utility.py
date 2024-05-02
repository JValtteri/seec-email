#!/usr/bin/python
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## PGP Key Management Utility
##   and utility functions
## 2. May. 2024

import getpass
import seecrypto, key_view, util


def make_password(passwd=None):
    """
    Ask a password twice. Useful for crating a new password
    Returns (passwd, status_message)
    """
    passwd   = getpass.getpass("       Password: ")
    if not util.is_valid_input(passwd, 'wide'):
        return None, "Illegal password"
    passwd_1 = getpass.getpass("Retype Password: ")
    if passwd != passwd_1:
        return None, "Passwords didn't match"
    return passwd, ""

def __make_gpg_key(name, passwd) -> str:
    """Generates a new GPG key"""
    gpg            = seecrypto.GPG()
    email          = input("Email address: ")
    if not util.is_valid_input(email, 'wide'):
        return "Illegal address field"
    status_message = gpg.generate_key_pair(name, email, password=passwd)
    print("Your Public key:")
    print(gpg.export_key(uid=email))
    return status_message

def make_gpg_key() -> str:
    """Interafce to make PGP keys"""
    name = input("           Name: ")
    if not util.is_valid_input(name, 'wide'):
        return "Illegal name field"
    passwd, status_message = make_password()
    if not passwd:
        return status_message, '', ''
    # Generate PGP key
    status_message = __make_gpg_key(name, passwd)
    return status_message, name, passwd

def list_keys(private=False):
    """
    Pretty prints the list of keys
    """
    key_view.print_keys(str(seecrypto.GPG().list_keys(private)))

def show_key(uid, secret=False, passwd=''):
    """
    Shows a public key corresponding to the provided uid or address
    """
    pub_key = seecrypto.GPG().export_key(uid, secret, passwd)
    print(pub_key)
    if secret:
        print("Copy the key, including the START and END lines.\n"+
            "THIS IS YOUR  S E C R E T  KEY. DO NOT GIVE THIS TO\n"+
            "ANYONE! KEEP IT SAFE.\n")
    else:
        print("Copy the key, including the START and END lines.\n"+
            "and give to anyone you want to be able to send you\n"+
            "encrypted mail.\n")
    input("Press ENTER to return to menu.")
    return ""

def del_key(secret=False):
    """Interface to delete a key"""
    uid = input("Key ID to delete\n> ")
    if not util.is_valid_input(uid, 'wide'):
        return "Illegal ID field"
    obj = seecrypto.GPG().delete_key(uid, secret)
    return obj.status

def import_keys():
    """Interface to import PGP keys"""
    prompt = ("Paste the key(s) here. Press ENTER two times to confirm\n"+
              "Ctrl+C to cancel")
    key_data = util.text_editor(prompt, strip_lines=True)
    gpg = seecrypto.GPG()
    ret_obj = gpg.import_public_key(key_data)
    try:
        print(ret_obj)
    except: pass
    return ""

def encrypt():
    """Interface to encrypt"""
    addr = input("Email: ")
    if not util.is_valid_input(addr, 'wide'):
        return "Illegal address field"
    message_body = util.text_editor("Write your message. Press ENTER three times to send")
    cryptext, status_message = seecrypto.GPG().encrypt_with_key(message_body, addr)
    print(cryptext)
    input("Press ENTER to continue")
    return status_message

def decrypt():
    """Interface to decrypt"""
    passwd = getpass.getpass("Password: ")
    cryptext = util.text_editor("Write your message. Press ENTER three times to send", strip_lines=True)
    message, status_message = seecrypto.GPG().decrypt_with_key(cryptext, passwd)
    print(message.decode('utf-8'))
    print("="*43)
    input("Press ENTER to continue")
    return status_message

def menu(status_message='') -> bool:
    """
    The main menu of the utility
    """
    print("\t1 - Import keys")
    print("\t2 - List public keys  \t\t2s - List secret keys")
    print("\t3 - Export public key \t\t3s - Export secret key")
    print("\t4 - Delete public key \t\t4s - Delete secret key")
    print("\t5 - Create new key pair")
    print("\n\tE - Encrypt \t\t\t D - Decrypt")
    print("\tQ - Exit")
    print(f"\n:: {status_message}")
    selection = input("> ")
    try:
        if selection == "":
            status_message = ""
        elif selection in ["q", "Q"]:
            return False, ''
        elif selection == "1":
            status_message =  import_keys()
        elif selection == "2":
            list_keys()
        elif selection == "3":
            uid = input("Email or ID: ")
            if not util.is_valid_input(uid, 'wide'):
                return True, "Illegal UID"
            status_message = show_key(uid, False)
        elif selection == "4":
            status_message = del_key()
        elif selection == "5":
            status_message, _, _ = make_gpg_key()
        elif selection == "2s":
            list_keys(True)
        elif selection == "3s":
            uid = input("Email or ID: ")
            if not util.is_valid_input(uid, 'wide'):
                return True, "Illegal UID"
            passwd = getpass.getpass("Password: ")
            if not util.is_valid_input(passwd, 'wide'):
                return True, "Illegal password"
            status_message = show_key(uid, True, passwd)
        elif selection == "4s":
            status_message = del_key(secret=True)
        elif selection.upper() == "E":
            status_message = encrypt()
        elif selection.upper() == "D":
            status_message = decrypt()
        else:
            status_message = f":: Woops, bad input: '{selection}'"
    except KeyboardInterrupt:
        status_message = "Ctrl + C was pressed. Aborted"
    return True, status_message

def main(status_message=''):
    """
    Main loop and entry point for key management utility
    """
    try:
        go = True
        while go:
            print("\n<<<<< Key Management Utility >>>>>\n")
            go, status_message = menu(status_message)
    except KeyboardInterrupt:
        print("\nCtrl + C was pressed. Exiting")

if __name__ == "__main__":
    main()
