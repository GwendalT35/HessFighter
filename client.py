import socket
import threading
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class Client:
    def __init__(self, server_address, port):
        self.server_address = server_address
        self.port = port
        self.key = b'ma_cle_de_chiffrement123'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_address, self.port))
        self.decrypted_message = ''

    def receive_messages(self):
        # Fonction pour déchiffrer un message avec AES-256
        def decrypt_message(message):
            iv = message[:AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
            decrypted = unpad(cipher.decrypt(message[AES.block_size:]), AES.block_size)
            return decrypted.decode("iso-8859-1")

        while True:
            encrypted_message = self.socket.recv(1024)
            if encrypted_message:
                self.decrypted_message = decrypt_message(encrypted_message)
                print(self.decrypted_message)

    def get_decrypted_message(self):
        return self.decrypted_message

    def set_decrypted_message(self, data):
        self.decrypted_message = data
