#!/usr/bin/python
# -*- coding: utf-8 -*-
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
import email.message
import datetime


class MailboxError(Exception):
    """Exception raised for errors in imap connection"""

class Mailbox():
    """Object for handling mailbox data and connections"""

    def __init__(self, settings):
        self.settings = settings
        self.status_message = "<uninitialized>"
        self.M = self.__get_mailbox()
        self.__inbox = []

    def __get_mailbox(self) -> imaplib.IMAP4:
        """
        Authenticate with IMAP server
        Returns an IMAP4 object
        """
        try:
            if not self.settings.get_map["security"]:
                self.status_message = "Security Error: Insecre IMAP4 not suupported"
                return None
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
        except ConnectionRefusedError as e:
            raise MailboxError("Error 111: Connection Refused") from e
        except imaplib.IMAP4.error as e:
            raise MailboxError("IMAP4 Error: email authentication failed") from e

    @staticmethod
    def __parse_message(raw_message) -> email.message.EmailMessage:
        """returns a message object from a raw message"""
        message = email.parser.BytesParser(policy=email.policy.default).parsebytes(
                raw_message,
                headersonly=False
                )
        return message

    def logout(self) -> str:
        """Close active IMAP server connection"""
        try:
            self.M.close()
            self.M.logout()
        except (imaplib.IMAP4.error, imaplib.IMAP4.abort):
            return "Is alredy logged out"
        return "Logged out"

    def update_inbox(self) -> str:
        """Fetch messages from inbox"""
        _, data = self.M.search(None, 'ALL')
        self.__inbox = []
        for num in reversed(data[0].split()):
            _, mail = self.M.fetch(num, '(RFC822)')
            self.__inbox.append(Mailbox.__parse_message(mail[0][1]))
        return "Fetched new messages"

    @property
    def inbox(self) -> [email.message.EmailMessage]:
        """
        Fetch messages from inbox
        returns a list of raw messages
        """
        return self.__inbox

    @staticmethod
    def get_message_header(message) -> (str, str, str, str):
        """Extracts header fields from a message object"""
        date = message.get("Date")
        subject = message.get("Subject")
        from_addr = message.get("From")
        to_addr = message.get("To")
        return date, subject, from_addr, to_addr

    @staticmethod
    def get_message_body(msg) -> str:
        """Extracts message body from a message object"""
        body_blob = msg.get_body(preferencelist=('plain','html'))
        if body_blob:
            body = body_blob.get_content()
        return body

    @staticmethod
    def __time_offset() -> str:
        """
        Get current timezone offset in email timestap fortmat
        e.g. '+0300'
        """
        timezone = datetime.datetime.now().astimezone()
        timedelta_in_s = timezone.utcoffset().total_seconds()
        timedelta_in_h = int( timedelta_in_s / 3600 * 100 )
        if timedelta_in_h < 0:
            sign = '-'
        else:
            sign = '+'
        abs_delta = str(abs(timedelta_in_h))
        zeros = '0' * ( 4-len(abs_delta) )
        return f"{sign}{zeros}{abs_delta}"

    @staticmethod
    def __get_timestamp() -> str:
        """
        Gets the current datetime and formats a standard timestamp
        """
        time_str = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S')
        # Time Offset
        timedelta = Mailbox.__time_offset()
        return f"{time_str} {timedelta}"

    def create_message(self, message_body, from_addr, to_addr, subject="<no subject>") -> email.message.EmailMessage:
        """Creates a EmailMessage object from the input"""
        # 'self' not necessary, but I don't want to re-import
        # the module again just to access this fuction as a static method
        #
        # Useful header fields, not yet supported by SEEC, are commented out
        msg = email.message.EmailMessage()
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = to_addr
        #msg[ ] = cc_addr
        #msg[ ] = bcc_addr
        #msg['Reply-To'] = from_addr
        msg['Date'] = Mailbox.__get_timestamp()
        msg['X-Mailer'] = 'SEEC - Secure Encrypted Email Client'
        msg['MIME-Version'] = '1.0'
        #msg['Importance'] = 'Normal'
        #msg['Message-ID'] = 'message-id'
        #msg['In-Reply-To'] = 'original-message-id'
        #msg['References'] = 'original-message-id'
        #msg['Content-Transfer-Encoding'] = 'quoted-printable'
        msg['Content-Type'] = 'text/plain; charset=UTF-8'
        msg.set_content(message_body)
        return msg

    def send_mail(self, msg) -> bool:
        """
        Sends the message object
        """
        try:
            smtp_addr = self.settings.get_smtp["addr"]
            smtp_port = self.settings.get_smtp["port"]
            with smtplib.SMTP(smtp_addr, smtp_port) as server:
                server.starttls()
                server.login(
                    self.settings.get_address,
                    self.settings.get_password
                    )
                server.send_message(msg)
        except Exception:
            return False
        return True
