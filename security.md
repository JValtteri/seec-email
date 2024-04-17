# Security Concerns and Mitigations

## Intercepted messages

#### Scenario

Adversary snoops on the network traffic, between client and server.

#### Mitigations

- Message body is always encrypted with PGP encryption
- Communication with the server uses SSL/TLS encryption

## Malicious access to local files

#### Scenario

Adversary gets access to files stored on the system and tries to find the keyfiles, or any files containing any exploitable information.

#### Mitigations

- PGP key is stored encrypted
- Server login information and credentials are stored encrypted
- No cleartext messages or keys are ever written to disk

## Memory inspection or memory dump

#### Scenario

Adversary plants malware on computer and analyzes the RAM memory during the use of SEEC. Any unencrypted data may leak as a result.

#### Notes

- `cryptography.fernet` is secure in its memory management. It claims not to leak any unencrypted bits.

- Searching for a suitable PGP encryption library with mitigation for data leakage and compatibility with Windows and Linux platforms

#### Mitigations

- Most of the sensitive processing will happen in imported libraries. Choosing ones with good implementation.
- Using `ctypes` to sanitize memory on the main programs Python side.
- Store actual in memory key hashed. Invalidate the hashed key, by re-salting the key file after session.

## Leak from email provider

#### Scenario 1

A data breach at the email provider leaks the login information for the service.

#### Mitigations

- Use a different key for logging in to the email server and encrypting the private key
- Login info and settings are encrypted with the same key as the private key

#### Scenario 2

A data breach at the email provider leaks all messages.

#### Mitigations

- All message bodies are encrypted with PGP.

## Mistake/misconfiguration

#### Scenario

User misconfigures the program or forgets to enable security features

#### Mitigations

- The email client enforces the use of PGP encryption.
	- Emails can't be sent without a valid PGP key.

## Secure Source Libraries

#### Risk: Python

~

#### Mitigations

Requiring `Python >= 3.7`. Many security and stability issues were fixed by 3.7.

#### Risk: YAML

Loading unsafe yaml files.

#### Mitigations

Using `yaml.safe_load()` to strip unsafe input
Requiring `pyyaml` >= 5.4 to mitigate `CVE-2020-14343`

#### Risk PGP impplementation

~

#### Mitigations

~

[EOF]
