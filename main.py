## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Main program
## 12. Mar. 2024

import sys


def menu_logged_in(key=b"", status_message=""):
    go = True
    print("\t0 - Show Inbox")
    print("\t1 - Write Mail")
    print("\t2 - Address Book")
    print("\tQ - Exit Program")
    selection = input("> ")

    if selection == "":
        status_message = ""
    return status_message


def menu_logged_out():
    go = True
    print("\t0 - Login")
    print("\t1 - New User")
    print("\tQ - Exit Program")
    print("\n" + status_message)
    selection = input("> ")

    if selection == "":
        status_message = ""

    elif selection in ["q", "Q"]:
        go = False

    elif selection == "0":
        status_message, key = get_new_key(key)

    elif selection == "1":  # Encrypt
        status_message = encrypt_file(key)

    else:
        status_message = f":: Woops, bad input: '{selection}'"
    return status_message


def menu(key=b"", login=False, status_message=""):
    print("\<<<<< SEEC - Secure Email Client >>>>>\n")
    if login:
        go, key, status_message = menu_logged_in(key, status_message)
    else:
        go, key, status_message = menu_logged_out(status_message)

    return go, key, status_message


def main():

    # Login
    # Inbox
    # Read Mail
    #


    # go = True
    # key = b""
    # status_message = ""
    # while go == True:
    go, key, status_message = menu(key, status_message)


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        sys.exit(e)
    except KeyboardInterrupt:
        sys.exit("\nCtrl + C was pressed. Terminating")
    except:                  ## For debug ##
        sys.exit(e)
    # except:
    #     sys.exit("Error: Program terminated unexpectedly")
