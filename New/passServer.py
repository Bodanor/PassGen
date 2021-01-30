import socket
import threading
import pickle
import random
import time

start_timer = time.time()

IP = "127.0.0.1"
PORT = 7654

ALPHANUM = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz", "1234567890", "+=%£$*&@#§-_"]

def client_handler(connexion, addr):
    while True:
        command = connexion.recv(1024)
        if not command:
            print("[{}] Deconnexion de {}!".format(round(time.time() - start_timer, 4), addr[0]))
            break

        command = pickle.loads(command)

        data = clientCommandWorker(command)
        data = pickle.dumps(data)
        connexion.send(data)

def clientCommandWorker(command):

    if command[0] == "gen" or command[0] == "Gen":
        password_length = command[2]
        password_counter = command[1]

        password_holder = []
        password = ""

        for y in range(0, password_counter):
            acceptable = False

            while not acceptable:
                symbols_counter = 0
                uppercase_counter = 0
                lowercase_counter = 0
                numeric_counter = 0

                for x in range(0, password_length):

                    random_cat = random.randint(0, len(ALPHANUM) - 1)
                    random_caractere = random.randint(0, len(ALPHANUM[random_cat]) - 1)

                    password += ALPHANUM[random_cat][random_caractere]

                    if random_cat == 0:
                        uppercase_counter += 1

                    elif random_cat == 1:
                        lowercase_counter += 1

                    elif random_cat == 2:
                        numeric_counter += 1

                    elif random_cat == 3:
                        symbols_counter += 1

                if (password_length > 4) and (symbols_counter > 2 or numeric_counter > 2):
                    password_holder.append(password)
                    acceptable = True
                    password = ""

                if password_length <= 4:

                    password_holder.append(password)
                    acceptable = True
                    password = ""

                else:
                    password = ""

        return password_holder




server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((IP, PORT))

print("[{}] Démarrage du serveur !".format(round(time.time() - start_timer, 4)))

while True:
    server.listen()
    connexion, addresse = server.accept()
    print("[{}]Nouvelle connexion de {} sur le port {}".format(round(time.time() - start_timer, 4),addresse[0], addresse[1]))
    client_thread = threading.Thread(target=client_handler, args=(connexion,addresse,))
    client_thread.start()
