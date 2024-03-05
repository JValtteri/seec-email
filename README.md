# SEEC

## What is SEEC

A command line email client using end-to-end encryption. 
Created as a course project submission for Tampere University **Secure Programming** [(COMP.SEC.300-2023-2024-1-TAU)](https://moodle.tuni.fi/course/view.php?id=40916 "COMP.SEC.300-2023-2024-1 Secure Programming (Lectures and exercises)") course.
## Features

- Client log in 
	- Asymmetric Encryption
	- Keys stored securely
- SSL connection to SMTP mail server
- Send and Receive emails
- Browse messages without downloading

## Usage

### Inbox

1. To unlock the client, the user must log in
2. Once unlocked, the private key is loaded in to memory
3. Default view is new message titles, senders and encryption status

```
Subject                      Sender                        Date/Time   Secure
-------                      ------                        ---------   ------
[1] Re: About your health     dr.john@legitdoctors.com     14/02/2024*
[2] Re: About your health     dr.john@legitdoctors.com     03/12/2023
[3] How are you?              crazygoose69@yahoo.com       12/10/2023  [INSECURE]
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
How are you?              crazygoose69@yahoo.com        12/10/2023  [INSECURE]
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< INSECURE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Wanna go fishin'?

-Ya' mait Bob
-----------------------
Q = Close - R = Respond [INSECURE]
```

## Asymmetric Key Encryption

[EOF]