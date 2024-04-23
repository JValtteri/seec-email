# SEEC

## What is SEEC

A command line email client using end-to-end encryption.
Created as a course project submission for Tampere University **Secure Programming** [(COMP.SEC.300-2023-2024-1-TAU)](https://moodle.tuni.fi/course/view.php?id=40916 "COMP.SEC.300-2023-2024-1 Secure Programming (Lectures and exercises)") course.

### Note on Security

##### Disclaimer!

**This project is very much a incomplete.**

This software is made as an exercise and comes with NO WARENTY WHAT SO EVER. Though I've made every effort to follow secure programming best practices, the software has not been audited by a professional entity, so the real world security has not been verified. Also, this client is incredibly bare-bones. You'd likely not get much use of it anyways.

#### Technical documentation

[Threat analysis](security.md)

[AI use Disclosure](ai_use_disclosure.md)

## Features

- Client log in
	- Asymmetric Encryption
	- Keys stored securely
- SSL connection to SMTP mail server
- Send and Receive emails
- Browse messages without downloading

## Usage

### Setting up

1. **Download the SEEC project or clone from GitHub**

`https://github.com/JValtteri/seec-email.git`

2. **Requirements**

 Requirements | version
  ---- | :--:
Python | >= 3.7
pyyaml | >= 5.4

**Install requirements**

`pip install -r requirements.txt`

3. **Configure connfig.yml**

Fill out according to your email providers instruuctions
SEEC does not suupport insecuure connections. SSL encryption for
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

### Inbox

1. To unlock the client, the user must log in
2. Once unlocked, the private key is loaded in to memory
3. Default view is new message titles, senders and encryption status

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

1. Attempts to decrypt with private key
2. On success, displays the decrypted content

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

## Asymmetric Key Encryption

[EOF]