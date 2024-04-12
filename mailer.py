## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Mailer, email handling back-end
## 13. Mar. 2024

import imaplib
import smtplib
import email
import email.parser
import email.policy

class Mailbox():
    '''
    Object for handling mailbox data and connections
    '''

    def __init__(self, settings):
        self.settings = settings
        self.status_message = "<uninitialized>"
        self.M = self.__get_mailbox()
        self.__inbox = []

    def __get_mailbox(self) -> imaplib.IMAP4:
        '''
        Authenticate with IMAP server
        Returns an IMAP4 object
        '''
        try:
            if not self.settings.get_map["security"]:
                return None, "Security Error: Insecre IMAP4 not suupported"
            M = imaplib.IMAP4_SSL(
                host=self.settings.get_map["addr"],
                port=self.settings.get_map["port"]
                )
            M.login(
                user=self.settings.get_address,
                password=self.settings.get_password
                )
            M.select()
            self.status_message = "Logged in to mailbox"
            return M
        except ConnectionRefusedError:
            self.status_message = "Error 111: Connection Refused"
            return None
        except imaplib.IMAP4.error:
            self.status_message = "IMAP4 Error: email authentication failed"
            return None

    @staticmethod
    def __parse_message(raw_message):
        '''
        returns a message object from a raw message
        '''
        message = email.parser.BytesParser(policy=email.policy.default).parsebytes(
                raw_message,
                headersonly=False
                )
        return message

    def logout(self):
        '''
        CLose active IMAP server connection
        '''
        try:
            self.M.close()
            self.M.logout()
        except (imaplib.IMAP4.error, imaplib.IMAP4.abort):
            return "Is alredy logged out"
        return "Logged out"

    def update_inbox(self):
        '''
        Fetch messages from inbox
        '''
        typ, data = self.M.search(None, 'ALL')
        self.__inbox = []
        for num in data[0].split():
            _, mail = self.M.fetch(num, '(RFC822)')
            self.__inbox.append(Mailbox.__parse_message(mail[0][1]))
        return "Fetched new messages"

    @property
    def inbox(self):
        '''
        Fetch messages from inbox
        returns a list of raw messages
        '''
        return self.__inbox

    @staticmethod
    def get_message_header(message):
        '''
        Extracts header fields from a message object
        '''
        date = message.get("Date")
        subject = message.get("Subject")
        from_addr = message.get("From")
        to_addr = message.get("To")
        return date, subject, from_addr, to_addr

    @staticmethod
    def get_message_body(msg):
        '''
        Extracts message body from a message object
        '''
        body_blob = msg.get_body(preferencelist=('plain','html'))
        if body_blob:
            body = body_blob.get_content()
        return body


    ### Refactored up to this point ###


    def create_message(message_body, from_addr, to_addr): # -> email.EmailMessage:
        msg = email.EmailMessage()
        msg.set_content(message_body)
        msg['Subject'] = f'The contents of {textfile}'
        msg['From'] = me
        msg['To'] = you
        return msg

    def get_mail(self, message_no=None):
        typ, data = self.M.search(None, 'ALL')
        print(f"Subject\t\tFrom\t\tDate")
        self.inbox = []
        for num in data[0].split():
            _, mail = self.M.fetch(num, '(RFC822)')
            self.inbox.append(mail)
            date, subject, from_addr, to_addr, body = Mailbox.get_message(mail[0][1]) # TODO decode
            print(f"#{num}.\t\t{from_addr}\t\t{date}")
        return self.inbox

    def print_message(self, index=0):
        date, subject, from_addr, to_addr, body = Mailbox.get_message(self.inbox[index][0][1])
        print(f"\tFrom:\t{from_addr}\t\t{date}")
        print(f"Subject:\t{subject}")
        print(f"{body}".decode("utf-8"))

    def send_mail() -> bool:
        fromaddr = prompt("From: ")
        toaddrs  = ", ".join(prompt("To: ").split())
        print("Enter message, end with ^D (Unix) or ^Z (Windows):")

        # Add the From: and To: headers at the start!
        msg = (f"From: {fromaddr}\r\nTo: {toaddrs}\r\n\r\n")


        print("Message length is", len(msg))

        # Send the message via our own SMTP server.
        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()

