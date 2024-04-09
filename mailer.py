## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Mailer, email handling back-end
## 13. Mar. 2024

import imaplib
import smtplib
from email.message import EmailMessage
from email.parser import Parser
from email.policy import default
import email

class Mailbox():

    def __init__(self, settings): #user, password):
        self.settings = settings
        self.status_message = "<uninitialized>"
        self.M = self.__get_mailbox()
        self.inbox = []

    @staticmethod
    def get_message(raw_message):
        #headers = Parser(policy=default).parsebytes(raw_message)
        message = email.message_from_bytes(raw_message)
        # ['Return-Path', 'Delivered-To', 'Received', 'DKIM-Signature', 'X-Virus-Scanned', 'Received', 'Received', 'DKIM-Signature', 'MIME-Version', 'Date', 'Content-Type', 'Content-Transfer-Encoding', 'X-Mailer', 'From', 'Message-ID', 'Subject', 'To', 'X-Originating-IP']
        #print('To: {}'.format(headers['to']))
        #print('From: {}'.format(headers['from']))
        #print('Subject: {}'.format(headers['subject']))
        # You can also access the parts of the addresses:
        #print('Recipient username: {}'.format(headers['to'].addresses[0].username))
        #print('Sender name: {}'.format(headers['from'].addresses[0].display_name))
        #return headers
        date = message.get("Date")
        subject = message.get("Received")
        from_addr = message.get("From")
        to_addr = message.get("To")
        #body = message.get_body(preferencelist=('plain'))
        body = message.get_payload()
        return date, subject, from_addr, to_addr, body

    def get_messages(self):
        pass

    def create_message(message_body, from_addr, to_addr) -> EmailMessage:
        msg = EmailMessage()
        msg.set_content(message_body)
        msg['Subject'] = f'The contents of {textfile}'
        msg['From'] = me
        msg['To'] = you
        return msg

    def __get_mailbox(self) -> imaplib.IMAP4:
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

    def close_mailbox(self):
        self.M.close()
        self.M.logout()

    def get_mail(self, message_no=None):
        typ, data = self.M.search(None, 'ALL')
        print(f"Subject\t\tFrom\t\tDate")
        self.inbox = []
        for num in data[0].split():
            _, mail = self.M.fetch(num, '(RFC822)')
            self.inbox.append(mail)
            # print(f'Message {num}\n{data[0][1]}\n')
            # print(f"Message {num}\nKeys: ")
            date, subject, from_addr, to_addr, body = Mailbox.get_message(mail[0][1]) # TODO decode

            #print(f"{subject}\t{from_addr}\t{date}")
            print(f"#{num}.\t\t{from_addr}\t\t{date}")
        return self.inbox

    def open_message(self, index=0):
        date, subject, from_addr, to_addr, body = Mailbox.get_message(self.inbox[index][0][1])
        print(f"\tFrom:\t{from_addr}\t\t{date}")
        print(f"Subject:\t{subject}")
        print(f"{body}") # .decode("utf-8")

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

