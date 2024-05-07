#!/usr/bin/python3
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## PGP Key Management Utility
##   and utility functions
## 2. May. 2024

import getpass
import seecrypto, key_view, util


class KeyGenerationError(Exception):
    """Raised when key generation fails"""

def make_password(passwd=None):
    """
    Ask a password twice. Useful for crating a new password
    Returns (passwd, status_message)
    """
    passwd   = util.valid_passwd("       Password: ")
    passwd_1 = getpass.getpass("Retype Password: ")
    if passwd != passwd_1:
        return None, "Passwords didn't match"
    return passwd, ""

def __make_gpg_key(name, passwd) -> str:
    """Generates a new GPG key"""
    gpg            = seecrypto.GPG()
    email          = util.valid_input("Email address: ", name='address')
    status_message = gpg.generate_key_pair(name, email, password=passwd)
    print("Your Public key:")
    print(gpg.export_key(uid=email))
    return status_message

def make_gpg_key() -> str:
    """Interafce to make PGP keys"""
    name = util.valid_input("           Name: ", name='name')
    passwd, status_message = make_password()
    if not passwd:
        raise KeyGenerationError("Password empty or didn't match")
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
    obj = seecrypto.GPG().delete_key(uid, secret)
    status_message = obj.status
    return status_message

def import_keys():
    """Interface to import PGP keys"""
    prompt = ("Paste the key(s) here. Press ENTER two times to confirm\n"+
              "Ctrl+C to cancel")
    key_data = util.text_editor(prompt, strip_lines=True)
    gpg = seecrypto.GPG()
    gpg.import_public_key(key_data)
    return ""

def encrypt():
    """Interface to encrypt"""
    addr = util.valid_input("Email: ", name='email')
    message_body = util.text_editor("Write your message. Press ENTER three times to send")
    cryptext, status_message = seecrypto.GPG().encrypt_with_key(message_body, addr)
    print(cryptext)
    input("Press ENTER to continue")
    return status_message

def decrypt():
    """Interface to decrypt"""
    passwd = getpass.getpass("Password: ")
    prompt = "Write your message. Press ENTER three times to send"
    cryptext = util.text_editor(prompt, strip_lines=True)
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
    print("\t2 - List public keys  \t\t2s - List private keys")
    print("\t3 - Export public key \t\t3s - Export private key")
    print("\t4 - Delete public key \t\t4s - Delete private key")
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
            uid = util.valid_input("Email or ID: ", name='UID')
            status_message = show_key(uid, False)
        elif selection == "4":
            status_message = del_key()
        elif selection == "5":
            status_message, _, _ = make_gpg_key()
        elif selection == "2s":
            list_keys(True)
        elif selection == "3s":
            uid = util.valid_input("Email or ID: ", name='ID')
            passwd = util.valid_passwd("Password: ")
            status_message = show_key(uid, True, passwd)
        elif selection == "4s":
            status_message = del_key(secret=True)
        elif selection.upper() == "E":
            status_message = encrypt()
        elif selection.upper() == "D":
            status_message = decrypt()
        else:
            status_message = f":: Woops, bad input: '{selection}'"
    except util.ValidationError as e:
        status_message = e.__str__()
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
