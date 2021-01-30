import random
import pickle

ALPHANUM = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz", "1234567890", "+=%£$*&@#§-_"]


def passwordGen(password_length, password_counter):

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

            if password_length<= 4:

                password_holder.append(password)
                acceptable = True
                password = ""

            else:
                password = ""

    return password_holder


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


password_counter = input("Nombres de mot de passe à générer : ")
password_counter = int(password_counter)
password_length = input("Longueur de chaque mot de passe : ")
password_length = int(password_length)

password_holder = passwordGen(password_length, password_counter)


validchoice = False

while not validchoice:

    save = input("Voulez vous sauvegarder les mots de passe dans un fichier ?(O/N)")
    if save == "O" or save == "o":

        print("Sauvegarde en cours...")
        encoded_password_holder = passwordEncoder(password_holder)

        with open('Passwords', 'wb') as file:
            pickle.dump(encoded_password_holder, file)

        print("Le fichier \"Passwords\" contient vos mot de passe. Pour les lires, veuillez utilisez le programme \"passDec.py\".")
        validchoice = True

    elif save == "N" or save == "n":
        for index, password in enumerate(password_holder):
            print("MDP {} : ".format(index +1 ), password)
            validchoice = True

    else:
        validchoice = False
