# Notes on Security

**This document expands on some of the security issues and rationale for the chosen solutions.**

## Attacks where an attacker has either remote or physical write access to the users hard drive.

### Memory sanitation

Sanitizing the password from the memory is not a straight forward task with a high level language like Python. Python manages its own memory and there is no simple way of removing anything from memory. Python itself doesn't offer features to do this.

I concluded that worrying about this issue is a waste of time. As a *"wise man"* of the internet put it: *"if your memory is constantly being compromised, I would re-think your security setup."* In any case, if an adversary can plant malware on my computer, memory inspection is the least of my worries.

### Not Compiled

Since Python isn't compiled, the code is easily read or modified by anyone. Even if set as read_only, an attacker with access to the system can write their own code to access any part of the program.

### Private members not enforced by Python

Since Python doesn't enforce private functions or variables, nothing prevents a piece of code probing in to those parts.

### Attacks against program integrity

If an attacker can modify files on the system, it is difficult to detect and warn if SEEC has been modified. Any automatic check can be nullified, by replacing the code doing the checking. Only by manually checking the files, their integrity can be confirmed.

One way to do this would be to calculate a checksum for all the files, and digitally signing them. The key to read the signature would be posted publicly with the repository. It's however unnecessary. The integrity of the files is easily checked by running command `git fetch && git status`. This will check if the local files have diverged from the source repository.

### Why it doesn't matter

1. If an attacker has full access to the system, there are more direct ways of attacking. An obvious and easy example would be a keylogger. There is no reasonable defense against a keyloggers, if the security of the system cannot be guaranteed.

2. The core part of the program is the PGP encryption and decryption. The cryptographically sensitive parts are handled by an OpenPGP compliant program, the GNU Privacy Guard.

%%
### What security this program provides?

This program gives an easy, integrated way of using PGP encryption and email. Nothing significantly sensitive is written to the disk. Mail is handled in memory.
%%

## Attacks with read access to disk

### Nothing saved to disc

You can't attack what doesn't exist. This is why this program doesn't save any data to disk. All messages are handled in memory. Only sensitive data on disk is the email credentials and the private key. The credentials are encrypted with AES-128 on the first run of SEEC. The private key is encrypted according to OpenPGP standard, by GPG.

### AES-128 CBC

While not the primary recommended symmetric encryption algorythm, it is thill on OWASP list as good enough. The library used for config file encryption is `cryptography.fernet`. It is a reputable library, therefore, risk for supply line attack is low.

Fernet supports AES-128 CBC encryption with high level functions that are easy to use securely. If upgrade to AES-256 would be sought, the encryption would need to be implemented manually with cryptography primitives from `cryptography.hazmat` library. This is inharently more risky, because doing this incorrecly can break security completely.

As risk for the config being stolen is low, and AES-128 is still considered *good enough*, an upgrade was not deemed worth the risk.
