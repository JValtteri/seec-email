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


def get_header():
    headers = Parser(policy=default).parsestr(raw_message)
    # 'From: Foo Bar <user@example.com>\n'
    # 'To: <someone_else@example.com>\n'
    # 'Subject: Test message\n'
    # '\n'
    # 'Body would go here\n')

    print('To: {}'.format(headers['to']))
    print('From: {}'.format(headers['from']))
    print('Subject: {}'.format(headers['subject']))
    # You can also access the parts of the addresses:
    print('Recipient username: {}'.format(headers['to'].addresses[0].username))
    print('Sender name: {}'.format(headers['from'].addresses[0].display_name))
    return headers


def create_message(message_body, from_addr, to_addr) -> EmailMessage:
    msg = EmailMessage()
    msg.set_content(message_body)
    msg['Subject'] = f'The contents of {textfile}'
    msg['From'] = me
    msg['To'] = you
    return msg


def get_mailbox(mail_user, mail_passwd) -> imaplib.IMAP4:
    M = imaplib.IMAP4()
    M.login(mail_user, mail_passwd)
    M.select()
    return M


def get_mail():
    typ, data = M.search(None, 'ALL')
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        print(f'Message {num}\n{data[0][1]}\n')
    M.close()
    M.logout()
    return typ, data


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

