import rco.file_crypto as fcrypt

fcrypt.encrypt_file('myfile.txt', 'myfile.encrypted.txt', 'public.pem')
fcrypt.decrypt_file('myfile.encrypted.txt', 'myfile.decrypted.txt', 'private.pem', '123123')