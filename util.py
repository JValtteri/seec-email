#!/usr/bin/python
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## General utilities
## 2. May. 2024

from datetime import datetime
import getpass


class ValidationError(Exception):
    """Error raised by valid_input() on invalid inputs"""

def text_editor(prompt, max_empty=2, strip_lines=False) -> str:
    """
    A basic input for writing multiline text
    """
    print(prompt)
    print("="*43)
    lines = []
    line = "<None>"
    empty_lines = 0
    while empty_lines < max_empty:
        line = input("")
        if strip_lines:
            lines.append(line.strip())
        else:
            lines.append(line)
        if line == "":
            empty_lines += 1
        else:
            empty_lines = 0
    print("="*43)
    return "\n".join(lines)

def __strip_from_time(time):
    """
    Strips the last two digits from a time
    00:00[:00]
    """
    return time.rsplit(':', 1)[0]

def parse_date(date):
    """
    Converts verbose email timestamp to compact form
    """
    date = date.split('+')[0]
    date = date.split('-')[0]
    date_split = date.split(' ', 1)
    day = date_split[0]
    date = date_split[1].rsplit(' ', 2)
    time = __strip_from_time(date[1])
    parsed_date = datetime.strptime(date[0], "%d %b %Y")
    formatted_date = parsed_date.strftime("%d.%m.%Y")
    return f"{day} {formatted_date} {time}"

def is_valid_input(s, length=40, mode='wide'):
    """
    Returns true if input complies with the set rules
    """
    if len(s) > length:
        print("Too long")
        return "", False
    if not s.isprintable():
        return "", False
    if mode == 'anum':
        return s.isalnum()
    return s, True

def valid_input(prompt, length=40, mode='wide', name=''):
    """
    Returns input string if input complies with the set rules
    otherwise raises a ValidationError

    Use the exception like so:
    except ValidationError as e:
        status_message = e.__str__()
    """
    s = input(prompt)
    if len(s) > length:
        raise ValidationError(f"Too long {name}")
    if not s.isprintable():
        raise ValidationError(f"Illegal {name}")
    if mode == 'anum':
        if not s.isalnum():
            raise ValidationError(f"Invalid {name}")
    return s

def valid_passwd(prompt, length=40):
    """
    Returns input password if input complies with the set rules
    otherwise raises a ValidationError

    Use the exception like so:
    except ValidationError as e:
        status_message = e.__str__()
    """
    pw = getpass.getpass(prompt)
    if len(pw) > length:
        raise ValidationError("Too long password")
    if not pw.isprintable():
        raise ValidationError("Illegal password")
    return pw

