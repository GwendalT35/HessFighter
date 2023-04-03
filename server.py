import socket
import threading
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class Server:
    def __init__(self, port):
        threading.Thread.__init__(self)
        host = socket.gethostname()
        local_ip = socket.gethostbyname(host)
        self.host = local_ip
        self.port = port
        self.key = b'ma_cle_de_chiffrement123'
        self.client_address = None
        # Créer un objet socket pour le serveur
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Lier le socket à une adresse et un port
        self.server_socket.bind((self.host, self.port))

        # Mettre le socket en mode écoute
        self.server_socket.listen(5)
        print("Serveur en attente de connexions...")

    def send(self, message=""):
        print("Envoie à :", self.client_address, ": ", message)
        # Chiffrement du message avec AES-256
        cipher = AES.new(self.key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))

        # Envoi du message chiffré au client
        try:
            self.client_socket.send(cipher.iv + ciphertext)
        except:
            pass

    def start(self):
        threading.Thread(target=self.run).start()

    def run(self):
        while True:
            # Accepter une nouvelle connexion client
            self.client_socket, self.client_address = self.server_socket.accept()
            # Créer un nouveau thread pour gérer la connexion client
            threading.Thread(target=self.send).start()
