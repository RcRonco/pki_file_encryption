# Author: Ron Cohen (RcRonco)
# Date: 04/02/2018

import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA


def encrypt_file(input_path, output_path, pub_key_path='public.pem'):
    """
    Encrypt file with public key.
    :param pub_key_path: the location of the public key.
    :param input_path: the location of the file will be encrypted.
    :param output_path: the encrypted file location.
    :return: None.
    """
    # Import private key
    with open(pub_key_path, 'rb') as pub_fd:
        rsa = RSA.importKey(pub_fd.read())

    # Generate secret key
    secret_key = os.urandom(16)

    # Encrypt the secret key with Public key
    encrypted_secret_key = rsa.encrypt(secret_key, None)

    with open(input_path, 'rb') as in_fd:
        data = in_fd.read()

    # Generate Initialization vector for AES encryption
    iv = os.urandom(16)
    aes = AES.new(secret_key, AES.MODE_CBC, iv)

    # Pad the data to fit block multiplier
    padding_len = aes.block_size - (len(data) % aes.block_size)
    data += ('\x00' * padding_len).encode()
    enc_data = aes.encrypt(data)

    with open(output_path, 'wb') as out_fb:
        # Write out the encrypted secret key, preceded by a length indication
        out_fb.write((str(len(encrypted_secret_key[0])) + '\n').encode())
        out_fb.write(encrypted_secret_key[0])

        # Write out the initialization vector and then the encrypted data
        out_fb.write(iv)
        out_fb.write(enc_data)


def decrypt_file(input_path, output_path, priv_key_path='private.pem',  pwd=None):
    """
    Decrypt file with private key.
    :param input_path: the location of the file will be decrypted.
    :param output_path: the decrypted file location.
    :param priv_key_path: the location of the private key.
    :param pwd: passphrase that decrypt private key.
        (AES variations are not supported by PyCrypto due to 04/02/2018)
    :return: None.
    """
    # Import private key
    with open(priv_key_path, 'rb') as priv_fd:
        rsa = RSA.importKey(priv_fd.read(), passphrase=pwd)

    # Read the encrypted file
    with open(input_path, 'rb') as in_fd:
        key_size = int(in_fd.readline())
        encrypted_key = in_fd.read(key_size)
        iv = in_fd.read(16)
        # decrypt symmetric encryption key with the private key
        secret_key = rsa.decrypt(encrypted_key)
        enc_data = in_fd.read()

    aes = AES.new(secret_key, AES.MODE_CBC, iv)
    # decrypt data
    data = aes.decrypt(enc_data)

    # remove padding
    data = data.decode('utf8').replace('\x00', '').encode()

    with open(output_path, 'wb') as out_fd:
        out_fd.write(data)
