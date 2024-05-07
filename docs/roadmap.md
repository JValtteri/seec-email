# Roadmap

## MVP Features

- [x] Client log in
	- [x] Keys stored securely
	- [x] Encrypting/Decrypting email credentials
- [x] SSL connection to SMTP mail server
- [x] Send and Receive emails
- [x] Limit Memory use on large inboxes
	- [ ] Browse messages without loading the message bodies
	- [x] Set a limit on number of messages that can be loaded at once (Limit is 100)
- [x] Generating PGP keys pairs
- [x] Asymmetric Encryption
	- [x] Encrypting messages
	- [x] Decrypting messages
- [x] Input validation
- [x] Finalize error handling

### Further development ideas (possibly)

- [ ] OAuth support (for logging in to gmail)
- [ ] Better support for use as a library or command line utility
- [ ] Ability to download messages to disk
- [x] Ability scroll the inbox
- [ ] Ability to search messages*
- [ ] Support multiple users
- [ ] Ability to Decrypt config
- [ ] Enable support for CC and BCC

### Advanced development (utopian)

- [ ] Folders support
- [ ] Remove inbox size limit
    - [ ] Decouple interface from back end (threading)
    - [ ] Smart loading
- [ ] Inbox filters
- [ ] Ability to send and receive attachments
- [ ] Improved TUI text editor with full eritor capabilities
    - [ ] Arrow navigation
    - [ ] Multi line edit text.
    - [ ] Ctrl for jumping words and paragraphs
    - [ ] Page Up and Page Down support
    - [ ] Home and End support
    - [ ] Copy Paste and Cut support
