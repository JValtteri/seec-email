# SEEC

## What is SEEC

A command line email client using end-to-end encryption.
Created as a course project submission for Tampere University **Secure Programming** [(COMP.SEC.300-2023-2024-1-TAU)](https://moodle.tuni.fi/course/view.php?id=40916 "COMP.SEC.300-2023-2024-1 Secure Programming (Lectures and exercises)") course.

### Note on Security

#### Disclaimer!

```diff
- This project is very much a work in progress!
- All basic security features are not yet complete!
```

This software is made as an exercise and comes with NO WARENTY WHAT SO EVER. Though I've made every effort to follow secure programming best practices, the software has not been audited by a professional entity, so the real world security has not been verified. Also, this client is incredibly bare-bones. You'd likely not get much use of it anyways.

#### Technical documentation

[Threat analysis](security.md)

[AI use Disclosure](ai_use_disclosure.md)

## Features

- [x] Client log in
	- [x] Keys stored securely
	- [x] Encrypting/Decrypting email credintials
- [x] SSL connection to SMTP mail server
- [x] Send and Receive emails
- [ ] Browse messages without downloading
- [x] Generating PGP keys pairs
- [x] Asymmetric Encryption
	- [x] Encrypting messages
	- [x] Decrypting messages
- [ ] Input validation
- [ ] Finalize error handling

#### Future development ideas

- [ ] OAuth support (for logging in to gmail)
- [ ] Better support for use as a library or command line utility
- [ ] Ability to download messages to disk
- [ ] Ability to send and receive attachments


## Usage

### Setting up

1. **Download the SEEC project or clone from GitHub**

`https://github.com/JValtteri/seec-email.git`

2. **Requirements**

 Requirements | version
  ---- | :--:
Python | >= 3.7
pyyaml | >= 5.4
python-gnupg | >= 0.5.2
cryptography | ~

**Install requirements**

`pip install -r requirements.txt`

This program relies on [**GnuPG (gpg)**](https://www.gnupg.org/download/index.html). It is pre-installed on most Linux systems. It is also available for Windows.

3. **Configure config.yml**

Fill out according to your email providers instruuctions
SEEC does not support insecure connections. SSL encryption for
both incominng and outgoing mail must be set to `true`.

```yaml
address: email@address.com
password: p4ssp0rd

# Incoming
map: imap.address.com
map_port: 993
map_security: true

# Outgoing
smtp: smtp.address.com
smtp_port: 587
smtp_security: true
```

#### Note abot email providers support for standard email clients

Google has [discontinued support](https://support.google.com/mail/answer/7126229?hl=en) for the stabard email authentication method, and instead requires the use of [OAuth 2.0 "Sign in with Google" API](https://developers.google.com/identity/protocols/oauth2). Since this is a not yet a ubiquitous way of authenticating  with email servers, it is outside the main scope of this projec.

### Running the first time

4. **Run `main.py`**

5. **Create New User**

Select ´1´ from the menu. You will be shown a series of instructions and warnings. Continue by pressing enter.

You can abort at any time by pressing `Ctrl+C`.

**General Info**

You should have created your config.yml. It will be imported and encrypted with your password.

If you lose your password, you will lose access to
your configuration file and your private key, and
lose access to all your encrypted messages.

Keep your password safe.

**Security info**

The passphrase you enter will be used to unlock the
email client and the private PGP key.

This program uses an external GPG program to handle
PGP encryption. It may be configured by default to
remember your passphrase for a few minutes, even if
you logged out of SEEC.

By default, SEEC does not save any of your messages
to disk. This is to protect your privacy.

### Loggin in

If everything went well, you can now log in from the menu, by selecting `0`.

You will be prompted for your password. Password will be stored for the duration of your session.

The client will
- load and decrypt the config in to memory
- log in to your email server with the credintials defined in the config.yml.


### Inbox

While logged in, chose `0` to view the inbox.
To open a message, enter the corresponding number.
To go back, enter `Q`.

```
Subject                      Sender                        Date/Time   Secure
-------                      ------                        ---------   ------
[1] Re: About your health     dr.john@legitdoctors.com     14/02/2024*
[2] Re: About your health     dr.john@legitdoctors.com     03/12/2023
[3] How are you?              crazygoose69@yehaa.com       12/10/2023  [INSECURE]
[4] <No Subject>              maverick@topgun.gov          08/10/2023

<Number>=Open Message  N=New Message
```

### Read message

The encryption status is displayed in the top right hand corner. For an encrypted message, pressing `D` will attempt to decrypt the message with your public key.

```
<No Subject>              maverick@topgun.gov           08/10/2023  [secure]
----------------------------------------------------------------------------
Hi!

I seem to have misplaced my F-15. Have you seen it?

Br,
Maverick

-----------------------
Q = Close - R = Respond
```

3. On unsuccessful decrypt
```
How are you?              crazygoose69@yehaa.com        12/10/2023  [INSECURE]
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< INSECURE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Wanna go fishin'?

-Ya' mait Bob
-----------------------
Q = Close - R = Respond [INSECURE]
```

### Sending messages

There are two ways of sending a message.

1. Opening the address book and selecting the recipient.
2. Selecting `1` from the menu.
	- You can manually enter the address.

If a public key is available for the address, you are prompted to encrypt the message.

### Address book

Address book allows you to send messages and add new contacts.

#### Adding public key for a contact

From main menu, select import key.

1. Select the address the key is for
2. Copy the key in to the entry field

## Troubleshooting

#### Unable to generate new key

##### I deleted the old keyring and now key generation fails

- Reboot. After GPG agent restarts you should be able to create a new keyring.
- If the problem presists, delete remaining GPG related files. Be sure not to delete `gpg-agent.conf`.

##### I think I deleted `gpg-agent.conf`

- pull from repo to replace missing file(s)
- or copy manually from github
- or create a new `gpg-agent.conf` with the following line in it:
```allow-loopback-pinentry```

[EOF]
