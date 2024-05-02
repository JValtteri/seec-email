#!/usr/bin/python
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Module for handling cryptographic features
## 17. Apr. 2024

import gnupg, os, base64
from cryptography.fernet import InvalidToken
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


SALT_SIZE = 16

class RSAConfigurationError(Exception):
    """Exception raised for errors in the configuration."""

class WrongKeyError(Exception):
    """Exception raised for wrong password."""

class GPG():
    """
    Object for interfacing with gnupg.GPG() object and
    methods thereby managing the GPG configurations used
    and access to PGP features and keyfile.
    """

    def __init__(self, home=None, keyring='seec.pkr'):
        if home is None:
            home = os.path.dirname(os.path.realpath(__file__))
        self.home = home
        self.keyring = keyring
        self.encoding = 'utf-8'
        self.gpg = self.__get_gpg()

    def __get_gpg(self):
        """
        Gets a gnupg.GPG() object.
        Sets parameters to be used, such as
        - path and name of keychain
        - used encoding
        """
        gpg = gnupg.GPG(
            gnupghome=self.home,    # path/to/home
            keyring=self.keyring    # keyfile
            )
        gpg.encoding = self.encoding
        return gpg

    def __generate_rsa_key_pair(self, name: str, email: str, comment: str, password: bytes, length=2048):
        """
        Generates an RSA key pair and stores it int the keychain
        """
        key_settings = self.gpg.gen_key_input(
            key_type="RSA",
            key_length=length,
            passphrase=password,
            name_real=name,
            name_comment=comment,
            name_email=email
            )
        key_obj = self.gpg.gen_key(key_settings)
        return key_obj

    def __generate_elliptic_curve_key_pair(self, name: str, email: str, comment: str, password: bytes):
        """
        Generates an elliptic curve cypher key pair and stores it int the keychain
        """
        key_settings = self.gpg.gen_key_input(
            key_type="EDDSA",
            key_curve="ed25519",    #"cv25519",
            passphrase=password,
            name_real=name,
            name_comment=comment,
            name_email=email
            )
        key_obj = self.gpg.gen_key(key_settings)
        return key_obj

    def __generate_gpg_default_key_pair(self, name: str, email: str, comment: str, password: bytes):
        """
        Generates a key pair with GPG default settings and stores it int the keychain
        """
        key_settings = self.gpg.gen_key_input(
            passphrase=password,
            name_real=name,
            name_comment=comment,
            name_email=email
            )
        key_obj = self.gpg.gen_key(key_settings)
        return key_obj

    def generate_key_pair(self, name: str, email: str, password='', length=2048, mode='rsa') -> str:
        """
        Public interface to generate a cryptographically strong key pair
        The key is stored in a key chain
        """
        comment="Generated with seecrypto.py"
        if length not in [1024, 2048, 4096]:
            raise RSAConfigurationError(f"Unsupported key length: {length}")
        if mode == 'rsa':
            key_obj = self.__generate_rsa_key_pair(name, email, comment, password, length)
        elif mode == 'elliptic':
            key_obj = self.__generate_elliptic_curve_key_pair(name, email, comment, password)
        elif mode == 'gpg_default':
            key_obj = self.__generate_gpg_default_key_pair(name, email, comment, password)
        status_message = "Key generation successful"
        if key_obj.status != 'ok':
            status_message = f"Key generation failed: {key_obj.status}"
        return status_message

    def encrypt_with_key(self, data: bytes, recipient: str) -> (bytes, str):
        """
        Encrypts the [data] with a public key corresponding with [recipient]
        [recipient] is any identifiable information corresponding with a key
        e.g. an email address, name or fingerprint.
        """
        pgp_obj = self.gpg.encrypt(data, recipient, always_trust=True)
        status_message = "Message encrypted"
        if pgp_obj.status != 'encryption ok':
            status_message = f"Encryption failed: {pgp_obj.status}"
        data = pgp_obj.data.decode(self.encoding)
        return data, status_message

    def decrypt_with_key(self, message, password) -> (str, str):
        """
        Decrypts the [message] with the private key
        """
        pgp_obj = self.gpg.decrypt(message, passphrase=password, always_trust=True)
        return pgp_obj.data, pgp_obj.status

    def import_public_key(self, key_data):
        """
        Imports a public key and adds it to keyfile
        """
        return self.gpg.import_keys(key_data)

    def export_key(self, uid, secret=False, passwd=''):
        """
        Exports a public key matching a uid, such as an email address
        """
        # False = Explicitly export only public keys
        return self.gpg.export_keys(uid, secret=secret, passphrase=passwd)

    def list_keys(self, secret=False):
        """
        Returns a list of key dicts
        """
        return self.gpg.list_keys(secret=secret)

    def delete_key(self, uid, private=False, passwd='') -> None:
        """
        Deletes a key [uid]
        if [private] flag is True, deletes the private key
        Returns the response object
        """
        return self.gpg.delete_keys(uid, private, passphrase=passwd)

    def public_key_available(self, uid) -> bool:
        """
        Returns True if a public key matching [uid] is found.
        [uid] can be any identifying data:
        - Name
        - Email
        - Fingerprint
        - Description
        """
        key = self.gpg.export_keys(uid)
        if key:
            return True
        return False

def __init_fernet(passphrase: bytes, salt: bytes) -> Fernet:
    """
    Creates a Fernet object for encrypting and decrypting
    """
    password = passphrase
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return Fernet(key)

def encrypt_bytes(data: bytes, passphrase: bytes) -> bytes:
    """
    Encrypts [bytes]. Uses a random salt and adds it to the end of the data.
    The length of the salt is [size]. Default is seecrypto.SALT_SIZE
    """
    salt = os.urandom(SALT_SIZE)
    f = __init_fernet(passphrase, salt)
    return f.encrypt(data)+salt

def decrypt_bytes(data: bytes, passphrase: bytes) -> bytes:
    """
    Decrypts [bytes]
    Handles extracting the salt
    """
    salt       = data[-SALT_SIZE:]      # Extract the salt from the end
    crypt_data = data[:-SALT_SIZE]      # Extract the cryptext
    f = __init_fernet(passphrase, salt)
    try:
        data = f.decrypt(crypt_data)
    except InvalidToken as e:
        raise WrongKeyError("Wrong password or corrupt data") from e
    return data

def encrypt_file_in_place(filename: str, passphrase: str) -> None:
    """
    Encrypts the file [filename] in place, using [passphrase].
    Overwrites the original file with the encrypted data.
    """
    passphrase = passphrase.encode('utf-8')
    with open(filename, 'rb') as f:
        clear_data = f.read()
        crypt_data = encrypt_bytes(clear_data, passphrase)
    with open(filename, 'wb') as f:
        f.write(crypt_data)

def decrypt_file_in_place(filename: str, passphrase: str) -> None:
    """
    Decrypts the file [filename] in place, using [passphrase].
    Overwrites the original file with the decrypted data.
    """
    passphrase = passphrase.encode('utf-8')
    with open(filename, 'rb') as f:
        crypt_blob = f.read()
        clear_data = decrypt_bytes(crypt_blob, passphrase)
    with open(filename, 'wb') as f:
        f.write(clear_data)

def decrypt_file_in_memory(filename: str, passphrase: str) -> bytes:
    """
    Reads the file [filename] and returns the decrypted version.
    Does not modify the file.
    """
    passphrase = passphrase.encode('utf-8')
    with open(filename, 'rb') as f:
        crypt_blob = f.read()
        clear_data = decrypt_bytes(crypt_blob, passphrase)
    return clear_data
