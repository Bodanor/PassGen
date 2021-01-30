import pickle
import random
import socket
import time
import threading
import errno
import os
import fcntl
import sys

IP = ["94.106.244.227", "127.0.0.1"]
PORT = 7654

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def passwordEncoder(password_holder):

    encoded_password_holder = []
    password_encoded = ""

    for password in password_holder:
        for caracter in password:
            caractere_holder = ord(caracter) + 47
            password_encoded += chr(caractere_holder)

        encoded_password_holder.append(password_encoded)
        password_encoded = ""

    return encoded_password_holder



def commandInput():
    command = input(bcolors.OKGREEN+ "passGen >> " + bcolors.ENDC)
    return command


def commandWorker():
    while True:
        command = commandInput()
        args = command.split(' ')
        if args[0] == "gen" or args[0] == "Gen":
            if len(args) == 1:
                length = random.randint(0, 10)
                password_counter = random.randint(0,20)

                passData = [args[0], length, password_counter]
                passData = pickle.dumps(passData)
                server.send(passData)

            else:
                length = int(args[1])
                password_counter = int(args[2])

                passData = [args[0],length, password_counter]
                passData = pickle.dumps(passData)
                server.send(passData)

            result = server.recv(8096)
            password_holder = pickle.loads(result)


            validchoice = False

            while not validchoice:

                print("Voulez-vous affichés les mots de passe ? (O/N)")
                choice = commandInput()

                if choice == "O" or choice == "o":

                    validchoice = True
                    for index, decoded_password in enumerate(password_holder):
                        print("MDP {} : ".format(index + 1), bcolors.OKBLUE + decoded_password + bcolors.ENDC)


                elif choice == "N" or choice == "n":
                    validchoice = True


                else:
                    validchoice = False


            validchoice = False
            while not validchoice:

                print("Voulez vous sauvegarder les mots de passe dans un fichier ?(O/N)")
                save = commandInput()

                if save == "O" or save == "o":

                    print("Sauvegarde en cours...")
                    encoded_password_holder = passwordEncoder(password_holder)

                    with open('Passwords', 'wb') as file:
                        pickle.dump(encoded_password_holder, file)

                    print("Le fichier " + bcolors.WARNING + "\"Passwords\"" + bcolors.ENDC + " contient vos mot de passe")
                    validchoice = True

                elif save == "N" or save == "n":
                        validchoice = True

                else:
                    validchoice = False



        if args[0] == "Status" or args[0] == "status" or args[0] == "stat":
            if len(args) == 1:
                crash = connexionStatus(server_status)

                if crash == True:
                    print(bcolors.FAIL + "Disconnected !" + bcolors.ENDC)

                elif crash == False:
                    print(bcolors.OKGREEN + "Connected !" + bcolors.ENDC)


        if args[0] == "Serveur" or args[0] == "SERVEUR" or args[0] == "serveur" or args[0] == "serv":
            serveur_up = []
            if len(args) == 1:
                for serveur in IP:
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((serveur, PORT))
                        s.close()
                        serveur_up.append(serveur)

                    except:
                        pass

                for index, serveur in enumerate(serveur_up):
                    print(bcolors.OKGREEN + "Serveur {} [{}] : est fonctionnel !".format(index+1, serveur) + bcolors.ENDC)


                #faire une boucle et afficher les serveur disponibles

            elif args[1] == "-a":
                serveur_up = []
                serveur_down = []

                for serveur in IP:
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((serveur, PORT))
                        s.close()
                        serveur_up.append(serveur)

                    except:
                        serveur_down.append(serveur)
                        pass

                for index, serveur in enumerate(serveur_up):
                    print(bcolors.OKGREEN + "Serveur {} [{}] : est fonctionnel !".format(index+1, serveur) + bcolors.ENDC)

                for index, serveur in enumerate(serveur_down):
                    print(bcolors.FAIL + "Serveur {} [{}] : est down !".format(index + 1, serveur) + bcolors.ENDC)



                #Faire une boucle et afficher serveurs disponible et non disponibles



        if args[0] == "exit" or args[0] == "Exit" or args[0] == "ex":
            os._exit(0)

        if args[0] == "Help" or args[0] == "help" or args[0] == "HELP":
            print(bcolors.WARNING)
            print("Liste de commande disponible : ")
            print("\t Gen : Génerer des mot de passe. Utilisation : Gen <Nombre de mot de passe> <Longueur du mot de passe>")
            print("\t Status : Afficher le status de connexion")
            print("\t Server : Afficher les serveurs disponibles. Utilisation : -a pour afficher tout les serveurs")
            print("\t Exit : Quitter le programme.")
            print("\t Help : afficher ce menu.")
            print("Plus de fonctionne viendront quand les idées seront la.")
            print(bcolors.ENDC)




def connexionStatus(server_status):
    try:
        connexion = server_status.recv(4)
    except socket.error as e:
        err = e.args[0]
        if err == errno.EAGAIN or err == errno.EWOULDBLOCK:

            return False
        else:

            return True

    else:

        return True





def connexionHolder():

    connected = False
    while not connected:
        try:
            global server, server_status

            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_status = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serveur_up = []
            try:
                for serveur in IP:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((serveur, PORT))
                    s.close()
                    serveur_up.append(serveur)

            except:
                pass

            random_IP = serveur_up[random.randint(0,len(serveur_up)-1)]
            server.connect((random_IP, PORT))
            server_status.connect((random_IP, PORT))
            print(bcolors.WARNING + "Connecté au serveur {}".format(random_IP) + bcolors.ENDC)
            fcntl.fcntl(server_status, fcntl.F_SETFL, os.O_NONBLOCK)
            connected = True
            command_threader = threading.Thread(target=commandWorker)
            command_threader.start()

            crashed = False
            while not crashed:

                crashed = connexionStatus(server_status)

                if crashed == True:
                    print("Le serveur a crash !")
                    crashed = True
                    connected = False

                time.sleep(0.1)


        except ConnectionError:
            print("La connexion à échouer.. Connexion à un autre serveur en cours...")
            connected = False
            time.sleep(1)


        except socket.timeout:
            print("Le serveur est down ou alors le port n'est pas forwarded...")




while True:
    connexionHolder()




