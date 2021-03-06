import pickle
import random
import socket
import time
import threading
import errno
import os
import fcntl
import paramiko
import getpass


IP = ["94.106.244.227", "127.0.0.1"]
PORT = 7654

BUFFERSIZE = 100


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

def check_linux():

    platform = os.name
    if platform == "posix" or platform == "Linux" or platform == "Darwin":
        return True
    else:
        return False

def commandInput():
    global is_linux

    if is_linux == True:
        command = input(bcolors.OKGREEN+ "passGen >> " + bcolors.ENDC)
        return command

    else:
        command = input("passGen >> ")
        return command



def commandWorker():
    try:
        while True:
            global server, random_IP
            command = commandInput()
            args = command.split(' ')
            erreur_syntax = False

            if args[0] == "gen" or args[0] == "Gen":
                crashed = connexionStatus(server_status)

                if not crashed:
                    if len(args) == 1:
                        length = random.randint(1, 10)
                        password_counter = random.randint(1,20)
                        erreur_syntax = False
                        passData = [args[0], password_counter, length]
                        passData = pickle.dumps(passData)
                        server.send(passData)



                    else:
                        try:
                            password_counter = int(args[1])
                            length = int(args[2])

                            if password_counter >= 30:
                                if is_linux:
                                    print(bcolors.FAIL + "Nombre de mot de passe trop grand !(MAX 50)" + bcolors.ENDC)
                                else:
                                    print("Nombre de mot de passe trop grand !(MAX 50)")

                                erreur_syntax = True

                            elif length >= 30:
                                if is_linux:
                                    print(bcolors.FAIL + "Longueur du mot de passe trop grand !(MAX 50)" + bcolors.ENDC)
                                else:
                                    print("Longueur du mot de passe trop grand !(MAX 50)")
                                erreur_syntax = True

                            else:
                                erreur_syntax = False
                                passData = [args[0], password_counter, length]
                                passData = pickle.dumps(passData)
                                server.send(passData)


                        except :
                            if is_linux:
                                print(bcolors.WARNING + "Erreur dans la syntax. Utilisation :")
                                print("\t Gen : Génerer des mot de passe. Utilisation : Gen <Nombre de mot de passe> <Longueur du mot de passe>")

                            else:
                                print("Erreur dans la syntax. Utilisation :")
                                print(
                                    "\t Gen : Génerer des mot de passe. Utilisation : Gen <Nombre de mot de passe> <Longueur du mot de passe>")
                            erreur_syntax = True
                            pass

                    if not erreur_syntax :
                        try:
                            result = server.recv(99999999)
                            password_holder = pickle.loads(result)

                        except KeyboardInterrupt:
                            continue

                        validchoice = False

                        while not validchoice:

                            print("Voulez-vous affichés les mots de passe ? (O/N)")
                            choice = commandInput()

                            if choice == "O" or choice == "o":

                                validchoice = True
                                for index, decoded_password in enumerate(password_holder):
                                    if is_linux:
                                        print("MDP {} : ".format(index + 1), bcolors.OKBLUE + decoded_password + bcolors.ENDC)
                                    else:
                                        print("MDP {} : ".format(index + 1) + decoded_password)


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

                                if is_linux:
                                    print("Le fichier " + bcolors.WARNING + "\"Passwords\"" + bcolors.ENDC + " contient vos mot de passe")

                                else:
                                    print("Le fichier \"Passwords\" contient vos mot de passe")
                                validchoice = True

                            elif save == "N" or save == "n":
                                validchoice = True

                            else:
                                validchoice = False

                else:
                    if is_linux:
                        print(bcolors.FAIL + "Vous n'etes connecté à aucun serveur !" + bcolors.ENDC)
                    else:
                        print("Vous n'etes connecté à aucun serveur !")




            elif args[0] == "Info" or args[0] == "info" or args[0] == "i" or args[0] == "stat" or args[0] == "s" or args[0] == "I" or args[0] == "S":
                try:
                    if len(args) == 1:
                        crash = connexionStatus(server_status)

                        if crash == True:
                            if is_linux:
                                print(bcolors.FAIL + "Déconnecté !" + bcolors.ENDC)
                            else:
                                print("Déconnecté !")

                        elif crash == False:
                            if is_linux:
                                print(bcolors.OKGREEN + "Connecté au serveur : " + bcolors.ENDC+ bcolors.OKBLUE + random_IP + bcolors.ENDC)
                            else:
                                print("Connecté au serveur : {}".format(random_IP))

                    if len(args) == 2:
                        crash = connexionStatus(server_status)
                        if crash == False:

                            if args[1].rstrip() == "-a":
                                if is_linux:
                                    print(bcolors.OKGREEN + "Connecté au serveur : " + bcolors.ENDC + bcolors.OKBLUE + random_IP + bcolors.ENDC)

                                else:
                                    print("Connecté au serveur : {}".format(random_IP))

                                server.send(pickle.dumps([args[0]]))
                                sys_info = server.recv(99999999)
                                sys_info = pickle.loads(sys_info)
                                if is_linux:
                                    print(bcolors.WARNING + "Platform : {}".format(sys_info[0]) + bcolors.ENDC)
                                    print(bcolors.WARNING + "Platform-Release : {}".format(sys_info[1]) + bcolors.ENDC)
                                    print(bcolors.WARNING + "Platform-Version : {}".format(sys_info[2]) + bcolors.ENDC)
                                    print(bcolors.FAIL + "Architecture : {}".format(sys_info[3]) + bcolors.ENDC)
                                    print(bcolors.OKBLUE + "Hostname : {}".format(sys_info[4]) + bcolors.ENDC)
                                    print(bcolors.OKBLUE + "Ip Address : {}".format(sys_info[5]) + bcolors.ENDC)
                                    print(bcolors.FAIL + "Processor : {}".format(sys_info[6]) + bcolors.ENDC)
                                    print(bcolors.FAIL + "CPU Cores : {}".format(sys_info[7]) + bcolors.ENDC)
                                    print(bcolors.OKGREEN + "Ram : {}".format(sys_info[8]) + bcolors.ENDC)
                                    print(bcolors.OKGREEN + "Ram Usage : {}%".format(sys_info[9]) + bcolors.ENDC)
                                    print(bcolors.FAIL + "CPU Usage : {}%".format(sys_info[10]) + bcolors.ENDC)
                                    start_ms = time.time()
                                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                    s.connect((random_IP, PORT))
                                    s.close()
                                    print(bcolors.OKBLUE + "Latence : {} ms".format(round(time.time() - start_ms, 2)) + bcolors.ENDC)

                                else:
                                    print("Platform : {}".format(sys_info[0]))
                                    print("Platform-Release : {}".format(sys_info[1]))
                                    print("Platform-Version : {}".format(sys_info[2]))
                                    print("Architecture : {}".format(sys_info[3]))
                                    print("Hostname : {}".format(sys_info[4]))
                                    print("Ip Address : {}".format(sys_info[5]))
                                    print("Processor : {}".format(sys_info[6]))
                                    print("CPU Cores : {}".format(sys_info[7]))
                                    print("Ram : {}".format(sys_info[8]))
                                    print("Ram Usage : {}%".format(sys_info[9]))
                                    print("CPU Usage : {}%".format(sys_info[10]))
                                    start_ms = time.time()
                                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                    s.connect((random_IP, PORT))
                                    s.close()
                                    print("Latence : {} ms".format(round(time.time() - start_ms, 2)))

                        elif crash == True:
                            if is_linux:
                                print(bcolors.FAIL + "Déconnecté !" + bcolors.ENDC)

                            else:
                                print("Déconnecté !")

                except KeyboardInterrupt:
                    pass

            elif args[0] == "Serveur" or args[0] == "SERVEUR" or args[0] == "serveur" or args[0] == "serv":
                serveur_up = []
                if len(args) == 1:
                    for serveur in IP:
                        try:
                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            s.settimeout(1)
                            s.connect((serveur, PORT))
                            s.close()
                            serveur_up.append(serveur)

                        except:
                            pass

                    for index, serveur in enumerate(serveur_up):
                        if is_linux:
                            print(bcolors.OKGREEN + "Serveur {} [{}] : est fonctionnel !".format(index+1, serveur) + bcolors.ENDC)

                        else:
                            print("Serveur {} [{}] : est fonctionnel !".format(index + 1,serveur))


                    #faire une boucle et afficher les serveur disponibles

                elif args[1] == "-a":
                    serveur_up = []
                    serveur_down = []

                    for serveur in IP:
                        try:
                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            s.settimeout(1)
                            s.connect((serveur, PORT))
                            s.close()
                            serveur_up.append(serveur)

                        except:
                            serveur_down.append(serveur)
                            pass

                    for index, serveur in enumerate(serveur_up):
                        if is_linux:
                            print(bcolors.OKGREEN + "Serveur {} [{}] : est fonctionnel !".format(index+1, serveur) + bcolors.ENDC)

                        else:
                            print("Serveur {} [{}] : est fonctionnel !".format(index + 1,serveur))


                    for index, serveur in enumerate(serveur_down):
                        if is_linux:
                            print(bcolors.FAIL + "Serveur {} [{}] : est down !".format(index + 1, serveur) + bcolors.ENDC)

                        else:
                            print("Serveur {} [{}] : est down !".format(index + 1, serveur))



                    #Faire une boucle et afficher serveurs disponible et non disponibles



            elif args[0] == "exit" or args[0] == "Exit" or args[0] == "ex" or args[0] == "quit" or args[0] == "QUIT" or args[0] == "Quit":
                os._exit(0)

            elif args[0] == "Help" or args[0] == "help" or args[0] == "HELP" or args[0] == "aide" or args[0] == "Aide" or args[0] == "AIDE":
                if is_linux:
                    print(bcolors.WARNING)
                    print("Liste de commande disponible : ")
                    print("\t Gen : Génerer des mot de passe. Utilisation : Gen <Nombre de mot de passe> <Longueur du mot de passe>.")
                    print("\t Info ou stat : Afficher le status de connexion. Utilisation : -a Pour plus d'inforamtions sur le serveur.")
                    print("\t Serveur : Afficher les serveurs disponibles. Utilisation : -a pour afficher tout les serveurs.")
                    print("\t Changer : Changer de serveur.")
                    print("\t Remote : Controler un serveur à distance par ssh.")
                    print("\t Exit : Quitter le programme.")
                    print("\t Help ou Aide : afficher ce menu.")
                    print("Plus de fonctionne viendront quand les idées seront la.")
                    print(bcolors.ENDC)

                else:
                    print("Liste de commande disponible : ")
                    print("\t Gen : Génerer des mot de passe. Utilisation : Gen <Nombre de mot de passe> <Longueur du mot de passe>.")
                    print("\t Info ou stat : Afficher le status de connexion. Utilisation : -a Pour plus d'inforamtions sur le serveur.")
                    print("\t Serveur : Afficher les serveurs disponibles. Utilisation : -a pour afficher tout les serveurs.")
                    print("\t Changer : Changer de serveur.")
                    print("\t Remote : Controler un serveur à distance par ssh.")
                    print("\t Exit : Quitter le programme.")
                    print("\t Help ou Aide : afficher ce menu.")
                    print("Plus de fonctionne viendront quand les idées seront la.")


            elif args[0] == "changer" or args[0] == "Changer" or args[0] == "CHANGER":
                validchoice = False
                while not validchoice:
                    serveur_up = []

                    crashed = connexionStatus(server_status)

                    if not crashed:
                        if is_linux:
                            print(bcolors.WARNING + "Vous etes connecté au serveur " + bcolors.OKGREEN + random_IP + bcolors.ENDC)

                        else:
                            print("Vous etes connecté au serveur {}".format(random_IP))

                    for serveur in IP:
                        try:

                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            s.connect((serveur, PORT))
                            s.close()
                            serveur_up.append(serveur)

                        except:
                            pass

                    for index, serveur in enumerate(serveur_up):
                        try:
                            start_ms = time.time()
                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            s.connect((serveur, PORT))
                            s.close()
                            if is_linux:
                                print(bcolors.OKCYAN + "Serveur ({}) [{}] : {} ms".format(index+1, serveur, round(time.time() - start_ms, 3)) + bcolors.ENDC)

                            else:
                                print("Serveur ({}) [{}] : {} ms".format(index + 1, serveur,round(time.time() - start_ms,3)))
                        except:
                            pass

                    if len(serveur_up) == 0:
                        if is_linux:
                            print(bcolors.FAIL + "Aucun serveur disponible !" + bcolors.ENDC)

                        else:
                            print("Aucun serveur disponible !")
                        validchoice = True

                    else:
                        try:
                            serveur_choix = input("Choisissez un serveur dans la liste ci-dessus (Enter pour ne rien faire) : ")
                            if not serveur_choix:
                                validchoice = True

                            else:
                                serveur_choix = int(serveur_choix)

                                if serveur_up[serveur_choix -1] == random_IP:
                                    if is_linux:
                                        print(bcolors.WARNING + "Vous êtes deja connecté à ce serveur !. Serveur non changé !" + bcolors.ENDC)
                                    else:
                                        print("Vous êtes deja connecté à ce serveur !. Serveur non changé !")
                                    validchoice = True
                                else:

                                    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                    server.connect((IP[serveur_choix-1],PORT))

                                    random_IP = IP[serveur_choix - 1]
                                    if is_linux:
                                        print(bcolors.WARNING + "Connecté au serveur {}".format(IP[serveur_choix-1])+ bcolors.ENDC)
                                    else:
                                        print("Connecté au serveur {}".format(IP[serveur_choix - 1]))

                                    validchoice = True
                        except ValueError:
                            validchoice = False
                            pass

                        except IndexError:
                            if is_linux:
                                print( bcolors.WARNING + "Serveur non compris dans la liste..." + bcolors.ENDC)
                            else:
                                print("Serveur non compris dans la liste...")

                            validchoice = False

                        except ConnectionError:
                            if is_linux:
                                print(bcolors.FAIL + "Serveur Down" + bcolors.ENDC)
                            else:
                                print("Serveur Down")

                            validchoice = False

            elif args[0] == "remote" or args[0] == "Remote":

                attempt = 3
                while attempt != 0:
                    try:
                        if is_linux:
                            username = input(bcolors.OKBLUE + "Utilisateur >> {}".format(bcolors.ENDC))

                        else:
                            username = input("Utilisateur >> ")

                        if is_linux:
                            pasword = getpass.getpass(bcolors.WARNING + "Mot de passe >> {}".format(bcolors.ENDC))

                        else:
                            pasword = getpass.getpass("Mot de passe >> ")
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(random_IP, username=username, password=pasword)
                        attempt = 0
                        crashed = connexionStatus(server_status)
                        current_server = random_IP
                        while not crashed and current_server == random_IP:

                            crashed = connexionStatus(server_status)

                            command_ssh = input("{} >> ".format(random_IP))

                            if command_ssh == "Exit" or command_ssh == "exit":

                                break
                            stdin, stdout, stderr = ssh.exec_command(command_ssh)
                            print(stdout.read().decode())
                            err = stderr.read().decode()
                            if err:
                                print(err)

                    except paramiko.AuthenticationException:
                        if is_linux:
                            print(bcolors.FAIL + "Nom d'utilisateur ou mot de passe incorrect !" + bcolors.ENDC)

                        else:
                            print("Nom d'utilisateur ou mot de passe incorrect !")

                        attempt -=1

                    except paramiko.ssh_exception.NoValidConnectionsError:
                        print("Impossible de se connecter au serveur {}. Veuillez check le firewall !".format(random_IP))
                        attempt = 0

                    except getpass.GetPassWarning:
                        pass

            elif args[0] == "Hash" or args[0] == "hash":

                crashed = connexionStatus(server_status)
                erreur_syntax = False
                if crashed == False:
                    if len(args) == 1:
                        if is_linux:
                            print(bcolors.WARNING + "Utilisation : Hash <HashType> <hash>" + bcolors.ENDC)

                        else:
                            print("Utilisation : Hash <HashType> <hash>")

                        erreur_syntax = True

                    elif len(args) == 2:
                        erreur_syntax = False
                        hash = [args[0],"Default" ,args[1]]
                        hash = pickle.dumps(hash)
                        server.send(hash)

                    elif len(args) == 3:
                        erreur_syntax = False
                        hash = [args[0], args[1], args[2]]
                        hash = pickle.dumps(hash)
                        server.send(hash)
                    else:
                        if is_linux:
                            print(bcolors.WARNING + "Utilisation : Hash <HashType> <hash>" + bcolors.ENDC)
                        else:
                            print("Utilisation : Hash <HashType> <hash>")

                        erreur_syntax = True

                    if not erreur_syntax:
                        try:
                            hash = server.recv(99999999)
                            hash = pickle.loads(hash)
                            print(hash)

                        except KeyboardInterrupt:

                            pass


                else:
                    if is_linux:
                        print(bcolors.FAIL + "Vous n'etes connecté à aucun serveur !" + bcolors.ENDC)

                    else:
                        print("Vous n'etes connecté à aucun serveur !")


    except AttributeError:
        os._exit(0)

    except KeyboardInterrupt:
        os._exit(0)






def connexionStatus(server_status):
    try:
        server_status.recv(4)
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

            while len(serveur_up) == 0:
                for serveur in IP:
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((serveur, PORT))
                        s.close()
                        serveur_up.append(serveur)
                    except:

                        pass

            global random_IP
            random_IP = serveur_up[random.randint(0,len(serveur_up)-1)]
            server.connect((random_IP, PORT))
            server_status.connect((random_IP, PORT))
            server_status.setblocking(False)
            connected = True

            crashed = False
            while not crashed:

                crashed = connexionStatus(server_status)

                if crashed == True:

                    crashed = True
                    connected = False

                time.sleep(0.1)


        except ConnectionError:
            print("La connexion à échouer.. Connexion à un autre serveur en cours...")
            connected = False
            time.sleep(1)


        except socket.timeout:
            print("Le serveur est down ou alors le port n'est pas forwarded...")





is_linux = check_linux()
connexion_thread = threading.Thread(target=connexionHolder)
connexion_thread.start()
commandWorker()




