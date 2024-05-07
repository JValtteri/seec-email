#!/usr/bin/python3
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Texts and Disclaimers
## 30. Apr. 2024

IMPORT_WARNING = [
"""
Do you have a config file ready in the same directory
as SEEC is installed?""",
"""
If you proceed, 'config.yml' file will be imported
and encrypted with your password.
""","""
If you lose your password, you will lose access to
your configuration file and your private key, and
lose access to all your encrypted messages.
""","""
Keep your password safe.
"""]

SECURITY_DISCLAIMERS = [
"""
The passphrase you enter will be used to unlock the
email client and the private PGP key.
""","""
This program uses an external GPG program to handle
PGP encryption. It may be configured by default to
remember your passphrase for a few minutes, even if
you logged out of SEEC.
""","""
Be aware that during this time someone with access
to your computer could theoretically decrypt your
messages, if you save any of your messages to your
disk.
""","""
By default, SEEC does not save any of your messages
to disk. This is to protect your privacy.
""","""
It is always the best practice to lock your computer
before walking away.
"""
]
