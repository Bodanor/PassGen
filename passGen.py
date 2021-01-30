import random
import pickle

alphanum = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz", "1234567890", "+=%£$*&@#§-_"]

password_holder = []
password = ""
password_couter = input("Nombres de mot de passe : ")
password_couter = int(password_couter)
lenght = input("Longueur du mot de passe : ")
lenght = int(lenght)


for y in range(0,password_couter):
    acceptable = False

    while not acceptable:
        symbols_counter = 0
        uppercase_counter = 0
        lowercase_counter = 0
        numeric_counter = 0

        for x in range(0,lenght):

            random_cat = random.randint(0,len(alphanum)-1)
            random_caractere = random.randint(0,len(alphanum[random_cat])-1)

            password += alphanum[random_cat][random_caractere]

            if random_cat == 0:
                uppercase_counter += 1

            elif random_cat == 1:
                lowercase_counter += 1

            elif random_cat == 2:
                numeric_counter += 1

            elif random_cat == 3:
                symbols_counter += 1


        if (lenght > 4) and (symbols_counter > 2 or numeric_counter > 2):
            symbols_counter = 0
            uppercase_counter = 0
            lowercase_counter = 0
            numeric_counter = 0
            password_holder.append(password)
            acceptable = True
            password = ""

        if lenght <= 4:
            symbols_counter = 0
            uppercase_counter = 0
            lowercase_counter = 0
            numeric_counter = 0
            password_holder.append(password)
            acceptable = True
            password = ""

        else:
            password = ""

validchoice = False

while not validchoice:

    save = input("Voulez vous sauvegarder les mots de passe dans un fichier ?(O/N)")
    if save == "O" or save == "o":

        encoded_password_holder = []
        password_encoded = ""

        for password in password_holder:
            for caracter in password:

                caractere_holder = ord(caracter) + 47
                password_encoded += chr(caractere_holder)

            encoded_password_holder.append(password_encoded)
            password_encoded = ""


        with open('Passwords', 'wb') as file:
            pickle.dump(encoded_password_holder, file)

        print("Le fichier \"Passwords\" contient vos mot de passe. Pour les lires, veuillez utilisez le programme \"passDec.py\".")
        validchoice = True

    elif save == "N" or save == "n":
        for index, password in enumerate(password_holder):
            print("MDP {} : ".format(index), password)
            validchoice = True

    else:
        validchoice = False
