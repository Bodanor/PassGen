import pickle


def passwordDecoder(encoded_password_holder):

    decoded_password_holder = []
    decoded_password = ""

    for encoded_password in encoded_password_holder:

        for encoded_caracter in encoded_password:
            decoded_caracter_holder = ord(encoded_caracter) - 47
            decoded_password += chr(decoded_caracter_holder)

        decoded_password_holder.append(decoded_password)
        decoded_password = ""

    return decoded_password_holder


with open('Passwords', 'rb') as file:
    encoded_password_holder = pickle.load(file)


decoded_password_holder = passwordDecoder(encoded_password_holder)

print("Mot de passe Chargé !")


validChoice = False

while not validChoice:

    choice = input("Voulez-vous affichés les mots de passe ? (O/N)")


    if choice == "O" or choice == "o":

        for index,decoded_password in enumerate(decoded_password_holder):
            print("MDP {} : ".format(index + 1), decoded_password)

        validChoice = True

    elif choice == "N" or choice == "n":
        print("Les mot de passe sont garder crypté dans le fichier !")
        validChoice = True

    else:
        validChoice = False





