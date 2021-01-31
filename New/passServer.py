import socket
import pickle
import random
import time
import multiprocessing
import hashlib
import threading
import platform
import psutil
import logging


def SystemInfoUpdated():
    while True:
        global info_status
        info_status = getSystemInfo()

def getSystemInfo():
    try:
        info=[]
        info.append(platform.system())
        info.append(platform.release())
        info.append(platform.version())
        info.append(platform.machine())
        info.append(socket.gethostname())
        info.append(socket.gethostbyname(socket.gethostname()))
        info.append(platform.processor())
        info.append(multiprocessing.cpu_count())
        info.append(str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB")
        info.append(psutil.virtual_memory().percent)
        info.append(psutil.cpu_percent(interval=1))
        return info
    except Exception as e:
        logging.exception(e)


sys_info_thread = threading.Thread(target=SystemInfoUpdated)
sys_info_thread.start()

start_timer = time.time()

IP = "127.0.0.1"
PORT = 7654

ALPHANUM = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz", "1234567890", "+=%£$*&@#§-_"]

def client_handler(connexion, addr):
    try:
        while True:
            command = connexion.recv(1024)
            if not command:
                print("[{}] Deconnexion de {}!".format(round(time.time() - start_timer, 4), addr[0]))
                break

            command = pickle.loads(command)

            data = clientCommandWorker(command)
            data = pickle.dumps(data)
            connexion.send(data)

    except pickle.UnpicklingError:
        connexion.close()
        print("[{}] Deconnexion de {}!".format(round(time.time() - start_timer, 4), addr[0]))
    except ValueError:
        connexion.close()
        print("[{}] Deconnexion de {}!".format(round(time.time() - start_timer, 4), addr[0]))


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

    elif command[0] == "Info" or command[0] == "info" or command[0] == "i" or command[0] == "stat" or command[0] == "s" or command[0] == "I" or command[0] == "S":
        global info_status
        return info_status

    elif command[0] == "Hash" or command[0] == "hash":
        if command[1] == "Default":
            hashed = hash(command[2])
            return hashed

        elif command[1] == "md5" or command[1] == "MD5":
            hashed = hashlib.md5(bytes(command[2], "UTF8")).hexdigest()
            print(hashed)
            return hashed

        elif command[1] == "sha1" or command[1] == "SHA1" or command[1] == "sha-1" or command[1] == "SHA-1":
            hashed = hashlib.sha1(bytes(command[2], "UTF8")).hexdigest()
            return hashed

        elif command[1] == "sha224" or command[1] == "SHA224" or command[1] == "sha-224" or command[1] == "SHA-224":
            hashed = hashlib.sha224(bytes(command[2], "UTF8")).hexdigest()
            return hashed

        elif command[1] == "sha256" or command[1] == "SHA256" or command[1] == "sha-256" or command[1] == "SHA-256":
            hashed = hashlib.sha256(bytes(command[2], "UTF8")).hexdigest()
            return hashed

        elif command[1] == "sha384" or command[1] == "SHA384" or command[1] == "sha-384" or command[1] == "SHA-384":
            hashed = hashlib.sha384(bytes(command[2], "UTF8")).hexdigest()
            return hashed

        elif command[1] == "sha512" or command[1] == "SHA512" or command[1] == "sha-512" or command[1] == "SHA-512":
            hashed = hashlib.sha512(bytes(command[2], "UTF8")).hexdigest()
            return hashed




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
