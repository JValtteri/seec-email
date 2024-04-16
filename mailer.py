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

    @staticmethod
    def __get_timestamp():
        '''
        Gets the current datetime and formats a standard timestamp
        '''
        # Date and Time
        time_str = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S')
        # Time Offset
        timezone = datetime.datetime.now().astimezone()
        timedelta_in_s = timezone.utcoffset().total_seconds()
        timedelta_in_h = int( timedelta_in_s / 3600 * 100 )
        if timedelta_in_h < 0:
            sign = '-'
        else:
            sign = '+'
        abs_delta = str(abs(timedelta_in_h))
        zeros = '0' * ( 4-len(abs_delta) )
        return f"{time_str} {sign}{zeros}{abs_delta}"


    def create_message(self, message_body, from_addr, to_addr, subject="<no subject>"): # -> email.EmailMessage:
        '''Creates a EmailMessage object from the input'''
        # TODO: 'self' not necessary, but I don't want to re-import
        # the module again just to access this fuction as a static method #
        msg = email.message.EmailMessage()
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = to_addr
        #msg[ ] = cc_addr
        #msg[ ] = bcc_addr
        msg['Reply-To'] = from_addr
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
        try:
            smtp_addr = self.settings.get_smtp["addr"]
            smtp_port = self.settings.get_smtp["port"]
            with smtplib.SMTP(smtp_addr, smtp_port
                ) as server:

                server.starttls()
                server.login(
                    self.settings.get_address,
                    self.settings.get_password
                    )
                server.send_message(msg)
        except:
            raise   # TODO DEBUG
            return False
        return True

    def print_message(self, index=0):
        '''Print the message directly to standard output'''
        message = Mailbox.get_message(self.inbox[index][0][1])
        date      = message[0]
        subject   = message[1]
        from_addr = message[2]
        to_addr   = message[3]
        body      = message[4]
        print(f"\tFrom:\t{from_addr}\t\t{date}")
        print(f"Subject:\t{subject}")
        print(f"{body}".decode("utf-8"))
