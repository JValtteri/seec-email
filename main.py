#!/usr/bin/python
# SEEC - Secure Encrypted Email Client
# Programming project for Secure Programming course at TUNI
#
# Main program
# 12. Mar. 2024


import menu_main, mailer

class ProgramState():
    '''
    Maintains the main program state
    '''

    def __init__(self):
        self.login    = False
        self.settings = None
        self.mailbox  = None

    def logout(self):
        self.mailbox.logout()
        return "Logged out"

    def mail_login(self):
        address      = self.settings.get_address
        pw           = "*"*len(self.settings.get_password)
        imap         = self.settings.get_map
        smtp         = self.settings.get_smtp
        print(f"Addr:\t{address}\npw:\t{pw}\n")
        print(f"IMAP:\t{imap['addr']},\t{imap['port']}")
        print(f"SMTP:\t{smtp['addr']},\t{smtp['port']}")
        self.mailbox   = mailer.Mailbox(self.settings)
        status_message = self.mailbox.status_message ## TODO HERE!!!
        return status_message

def main():
    state          = ProgramState()
    status_message = menu_main.menu(state)
    print(f"\n:: {status_message}")

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        sys.exit(e)
    except KeyboardInterrupt:
        sys.exit("\nCtrl + C was pressed. Terminating")
    # except:
    #     sys.exit("Error: Program terminated unexpectedly")
