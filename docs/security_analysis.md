# Security Concerns and Mitigations

This document follows the principles laid out in [OWAP Secure Coding Practices Checklist](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/stable-en/02-checklist/05-checklist).
## Intercepted messages

#### Mitigations

- Message body is, by default, encrypted with PGP encryption
- Communication with the server uses SSL/TLS encryption

## Malicious access to local files

#### Scenario

Adversary gets access to files stored on the system and tries to find the keyfiles, or any files containing any exploitable information.

#### Mitigations

- PGP key is stored encrypted
- Server login information and credentials are stored encrypted
- No cleartext messages or keys are written to disk

## Memory inspection or memory dump

#### Scenario

Adversary plants malware on computer and analyzes the RAM memory during the use of SEEC. Any unencrypted data may leak as a result.

#### Mitigations

- Most of the sensitive processing will happen in imported libraries. Choosing ones with good implementation.
- *"if your memory is constantly being compromised, I would re-think your security setup."*
- `cryptography.fernet` is secure in its memory management. It claims not to leak any unencrypted bits.
- `Python-gpg` functions as a wrapper for GPG. GPG itself is considered safe, while python-gpg library is a mature library, and has mitigations against injection attacks.

#### Residual risk

- Python manages its own memory and there is no defined way of removing anything from memory. Python itself doesn't offer features to do so.

## Leak from email provider

#### Scenario 1

A data breach at the email provider leaks the login information for the service.

#### Mitigations

- Use a different key for logging in to the email server and encrypting the private key
- Login info and settings are encrypted with the same key as the private key

#### Scenario 2

A data breach at the email provider leaks all messages.

#### Mitigations

- All message bodies are encrypted with PGP by default.

## Mistake/misconfiguration

#### Scenario

User misconfigures the program or forgets to enable security features

#### Mitigations

- If a suitable public key is preset, encryption is always offered as default.
- If a private key is not present, the user is warned about it before sending the message.
## Secure Source Libraries

#### Python Mitigations

- Requiring `Python >= 3.7`. Many security and stability issues were fixed by 3.7.
- The number of source libraries is low
- Recommended/most secure methods are used.
- Minimum required version is defined for each library.
- Only reputable libraries are used.
#### YAML Mitigations

- Using `yaml.safe_load()` to strip unsafe input
- Requiring `pyyaml >= 5.4` to mitigate `CVE-2020-14343`

#### PGP implementation mitigations

`Python-gpg` was chosen as a mature library. The library is a wrapper for GNU Privacy Guard, a well trusted application.

https://wiki.python.org/moin/GnuPrivacyGuard
## Injections

#### Mitigations: malicious injection in to input fields

##### Input sanitazion

The library `pyyaml` library used to store configurations and contacts, handles inputs well and prevents malicious injections, both while writing and while reading yaml. Also see [Risk: YAML](#Risk:_YAML) for further info on yaml security.

Python's `input()` function handles all input as strings. Pythons `str.isprintable()` is used to check for special characters in input, that might cause issues. The input length is also limited for most fields.

## Authentication

- All sensitive data is stored in encrypted form.
- Unencrypted data is never written to disk.
- In case an unexpected exception occurs, the user is logged out and private info is cleared from the session object.
- Messages for login failure are generic.
## Encryption

For encrypting messages, SEEC uses the [standard asymmetric encryption used by OpenPGP](https://www.gnupg.org/faq/gnupg-faq.html#default_rsa2048), 2048-bit RSA. It ensures compatibility with other PGP clients.

For encrypting the configuration file, containing the email server credentials, SEEC uses Python [Fernet](https://cryptography.io/en/latest/fernet/) library, which uses AES-128 in CBC mode.[^1]

[^1]: https://github.com/pyca/cryptography/blob/main/src/cryptography/fernet.py

## Error handling

- Error messages do not disclose private information
- Error messages do not display stack trace information
- Error messages are non-specific
- After an unexpected error, the user is logged out and session object clears all contained data.

[EOF]
