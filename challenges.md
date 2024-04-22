# Notes on Security

### Memory sanitization

Sanitizing the password from the memory is not a straight forward task with a high level language like Python. Python manages its own memory and there is no simple way of removing anything from memory.

### Not Compiled

Since Python isn't compiled, the code is easily read or modified by anyone. Even if set as read_only, an attacker with access to the system can write their own code to access any part of the program.

### Private members not enforced by Python

Since Python doesn't enforce private functions or variables, nothing prevents a piece of code probing in to those parts.

### Why it doesn't matter

1. If an attacker has full access to the system, there are more direct ways of attacking. An obvious and easy example would be a keylogger. There is no reasonable defence against a keyloggers, if the security of the system cannot be guaranteed.

2. The core part of the program is the PGP encryption and decryption. The cryptographically sensitive parts are handled by an OpenPGP compliant program, the GNU Privacy Guard.

### What security this program provides?

This program gives an easy, integrated way of using PGP encryption and email. Nothing significantly sensitive is written to the disk. Mail is handled in memory.

