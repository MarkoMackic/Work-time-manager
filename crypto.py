from simplecrypt import encrypt, decrypt


class Crypto(object):
    @staticmethod
    def write_to_file(content, file_name, password):
        """Write password encrypted content to the file.

        Params:
            * content -> string -> content to be encrypted
            * file_name -> string -> file name to save
            encrypted content to
            * password -> string -> password for encryption

        """
        with open(file_name, 'wb+') as output:
            encrypted = encrypt(password, content)
            output.write(encrypted)

    @staticmethod
    def read_from_file(file_name, password, is_string=True):
        with open(file_name, 'rb') as file_object:
            encrypted = file_object.read()
            plaintext = decrypt(password, encrypted)
            if is_string:
                return plaintext.decode('utf8')
            else:
                return plaintext

    @staticmethod
    def encrypt_text(text, password):
        pass

    @staticmethod
    def decrypt_text(text, password):
        pass

