## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## Module for handling cryptographic features
## 17. Apr. 2024

import gnupg, os


class RSAConfigurationError(Exception):
    """Exception raised for errors in the configuration."""

class GPG():
    """
    Object for interfacing with gnupg.GPG() object and
    methods thereby managing the GPG configurations used
    and access to PGP features and keyfile.
    """

    def __init__(self, home=None, keyring='seec.pkr'):
        if home == None:
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
            gnupghome=self.home,      # path/to/home
            keyring=self.keyring
            )
        gpg.encoding = self.encoding
        return gpg

    def __generate_rsa_key_pair(self, name, email, password, length=1024):
        """
        Generates an RSA key pair and stores it int the keychain
        """
        key_settings = self.gpg.gen_key_input(
            key_type="RSA",
            key_length=1024,
            passphrase=password,
            name_real="Autogenerated Key",
            name_comment="Generated by gnupg.py",
            name_email=email
            )
        key_obj = self.gpg.gen_key(key_settings)
        return key_obj

    def __generate_elliptic_curve_key_pair(self, name, email, password):
        """
        Generates an elliptic curve cypher key pair and stores it int the keychain
        """
        key_settings = self.gpg.gen_key_input(
            key_type="EDDSA",
            key_curve="ed25519",    #"cv25519",
            passphrase=password,
            name_real="Autogenerated Key",
            name_comment="Generated by gnupg.py",
            name_email=email
            )
        key_obj = self.gpg.gen_key(key_settings)
        return key_obj

    def generate_key_pair(self, name, email, password='', length=1024, type='rsa'):
        """
        Public interface to generate a cryptographically strong key pair
        The key is stored in a key chain
        """
        if length not in [1024, 2048]:
            raise RSAConfigurationError(f"Unsupported key length: {length}")
        if type == 'rsa':
            key_obj = self.__generate_rsa_key_pair(name, email, password, length)
        if type == 'elliptic':
            key_obj = self.__generate_elliptic_curve_key_pair(name, email, password)
        status_message = "Key generation successful"
        if key_obj.status != 'ok':
            status_message = f"Key generation failed: {key_obj.status}"
        return status_message

    def encrypt_with_key(self, data, recipient):
        """
        Encrypts the [data] with a public key corresponding with [recipient]
        [recipient] is any identifiable information corresponding with a key
        e.g. an email address.
        """
        pgp_obj = self.gpg.encrypt(data, recipient, always_trust=True)
        status_message = "Message encrypted"
        if pgp_obj.ok == False:
            status_message = f"Encryption failed: {pgp_obj.status}"
        data = pgp_obj.data
        return data, status_message

    def decrypt_with_key(self, message, password):
        """
        Decrypts the [message] with the private key
        """
        return self.gpg.decrypt(message)

    def import_public_key(self, key_data):
        """
        Imports a public key and adds it to keyfile
        """
        self.gpg.import_keys(key_data)

    def export_public_key(self, uid):
        """
        Exports a public key matching a uid, such as an email address
        """
        # False: Explicitly export only public keys
        key = self.gpg.export_keys(uid, False)


###