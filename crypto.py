from Crypto.Cipher import AES
from Crypto.Hash import SHA256

class MyCrypto(object):
    @staticmethod
    def password_to_key(password):
        """
        Use SHA-256 over our password to get a proper-sized AES key.
        This hashes our password into a 256 bit string.
        """
        return SHA256.new(password.encode('utf-8')).digest()

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
            try:
                key = MyCrypto.password_to_key(password)
                cipher = AES.new(key, AES.MODE_EAX)
                ciphertext, tag = cipher.encrypt_and_digest(content.encode('utf-8'))
                [ output.write(x) for x in (cipher.nonce, tag, ciphertext) ]

            except ValueError as e:
                print(e);


    @staticmethod
    def read_from_file(file_name, password, is_string=True):
        with open(file_name, 'rb') as file_object:
          nonce, tag, ciphertext = [ file_object.read(x) for x in (16, 16, -1) ]
          key = MyCrypto.password_to_key(password)
          cipher = AES.new(key, AES.MODE_EAX, nonce)
          plaintext = cipher.decrypt_and_verify(ciphertext, tag)
          print(plaintext)
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

