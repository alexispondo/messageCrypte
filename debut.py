from os import system as sys

# genere le couple de cle privée/publique
def Prive(nom):
    txt = "openssl genrsa -out "+nom+"_cle_prive.pem 1024"
    return sys(txt)

# Extraire de la paire de clées la clée publique
def Public(nom):
    txt = "openssl rsa -in "+nom+"_cle_prive.pem -pubout -out "+nom+"_cle_publique.pem"
    return sys(txt)

# Créer la clé secrete (elle sera enregistré dans un fichier texte)
def MdpTxt(nom):
    fichier = nom+"_mdp.txt"
    with open(fichier, "w") as f:
        cle = input("Entrez votre clé secrete: ")
        f.write(cle)

# Crypter le fichier à envoyé
def CrypterFichier(nom, fichier, extension, mdp):
    txt = "openssl enc -e -aes-256-cbc -in "+fichier+"."+extension+" -out "+nom+"_video."+extension+" -pass pass:"+mdp
    return sys(txt)

# Chiffré la clé secrete (celle utilisée pour crypter le fichier)
def ChiffrerCle(nom, mdp_claire, pub_cle):
    txt = "openssl rsautl -encrypt -in "+mdp_claire+" -inkey "+pub_cle+" -pubin -out "+nom+"_mdp_chiffrer.txt"
    return sys(txt)

# Générer une empreinte pour le fichier
def GenererEmpreinte(nom, fichier):
    txt ="openssl dgst -sha1 -out "+nom+"_empreinte.txt "+fichier
    return sys(txt)

# Faire la signature de l'empreinte
def SignerEmpreinte(nom, empreinte, cleprive):
    txt ="openssl rsautl -sign -in "+empreinte+" -inkey "+cleprive+" -out "+nom+"_signature.txt"
    return sys(txt)



# Déchiffrer la clé secrete de l'emeteur'
def DechiffrerCle(nom, mdpcrypte, cleprive):
    txt = "openssl rsautl -decrypt -in "+mdpcrypte+" -inkey "+cleprive+" -out mdpdechiffre_par_"+nom+".txt"
    return sys(txt)

# Decrypter le fichier reçu
def DecrypterFichier(nom, fichierchiffre, extension, mdp):
    txt = "openssl enc -d -aes-256-cbc -in "+fichierchiffre+"."+extension+" -out video_dechiffrer_par_"+nom+"."+extension+" -pass pass:"+mdp+""
    #txt = "openssl enc -d -aes-256-cbc -in "+fichierchiffre+"."+extension+" -out video_dechiffrer_par_"+nom+"."+extension
    return sys(txt)

# Verifier la signature (authentification)
def VerifierAuth(signature, cle_publique):
    txt = "openssl rsautl -verify -in "+signature+" -pubin -inkey "+cle_publique+" -out empreinte2_pour_verification.txt"
    return sys(txt)

# Comparaison du contenu des fichiers d'empreintes
def comparaison(f1, f2):
    with open(f1, "r") as f_1:
        v1 = f_1.read()
    with open(f2, "r") as f_2:
        v2 = f_2.read()

    v1 = v1.split(" ")[-1][:-1]
    v2 = v2.split(" ")[-1][:-1]
    if v1 == v2:
        return True
    else:
        return False


def main():
    print("Bienvenue les gars:")
    nom = input("Entrer votre nom: ")
    print("\n\n========================================= Faites un choix ============================================")
    print("| 1- Générer la paire de clé")
    print("| 2- Extraire la clé publique")
    print("| 3- creation de la clé secrete")
    print("| 4- crypter le fichier à transferer en utilisant une clé secrete")
    print("| 5- chiffrer la clé secrete")
    print("| 6- Generer une empreinte")
    print("| 7- Signer l'empreinte")
    print("\n| 8- dechiffrer la clé secrete")
    print("| 9- decrypter le fichier reçu")
    print("| 10- Verifier l'authentification")
    print("| 11- Comparer les fichier d'empreints")
    print("| q- pour quitter")
    choix = input("Choix: ")
    while choix != "q":
        if choix == "1":
            print("\nGénérer la paire de clé")
            Prive(nom)
            print("\n")
            print("clé privé => {}_cle_prive.pem".format(nom))

        elif choix == "2":
            print("\nExtraire la clé publique")
            Public(nom)
            print("\n")
            print("clé publique => {}_cle_publique.pem".format(nom))

        elif choix == "3":
            print("\nCréation de la clé secrete")
            MdpTxt(nom)

        elif choix == "4":
            print("\nCryptage du fichier à transferer")
            extension = str(input("Entrer l'extension du fichier à crypter "))
            fichier = str(input("Entrez le nom de fichier à crypter "))
            mdp = str(input("Entrez la clé secrete "))
            CrypterFichier(nom, fichier, extension, mdp)

        elif choix == "5":
            print("\nChiffrage de la clé sécrete")
            print("Pour ce cryptage veuillez utiliser la clé public de votre recepteur !!!")
            mdp_claire = input("Entrez le nom du fichier de mot de passe sans oublier les extensions ")
            pub_cle = input("Entrez le nom de la clé publique de votre recepteur sans oublier les extensions ")
            ChiffrerCle(nom, mdp_claire, pub_cle)

        elif choix == "6":
            print("\nGenerer une empreinte")
            fichier = input("Entrez le nom du fichier dont vous voulez generer l'empreinte sans oublier les extensions ")
            GenererEmpreinte(nom, fichier)

        elif choix == "7":
            print("\nSigner l'empreinte")
            empreinte = input("Entrez le nom de l'empreinte sans oublier les extensions ")
            cleprive = input("Entrez la clé privée sans oublier les extensions ")
            SignerEmpreinte(nom,empreinte, cleprive)

        elif choix == "8":
            print("\nDechiffrer la clé secrete")
            mdpcrypte = input("Entrez le fichier de mot de passe crypté sans oublier les extensions ")
            cleprive = input("Entrez votre cle privée sans oublier les extensions ")
            DechiffrerCle(nom, mdpcrypte, cleprive)

        elif choix == "9":
            print("\nDecrypter le fichier reçu")

            extension = str(input("Entrer l'extension du fichier crypté "))
            fichierchiffre = str(input("Entrez le nom de fichier à crypter "))
            mdp = str(input("Entrez la clé secrete de l'emeteur "))
            DecrypterFichier(nom, fichierchiffre, extension, mdp)

        elif choix == "10":
            print("\nVerifier l'authentification")
            signature = input("Entrez le nom de la signature reçu sans oublier l'extensions ")
            cle_publique = input("Entrez la clé publique de l'emeteur sans oublier les extensions ")
            VerifierAuth(signature, cle_publique)

        elif choix == "11":
            print("\nComparer les fichier d'empreints")
            f1 = input("Entrez le nom du fichier d'empreinte initial sans oublier l'extension")
            f2 = input("Entrez le nom du fichier d'empreinte de veriificattion sans oublier l'extension")
            if comparaison(f1,f2):
                print("Les deux fichiers ont la même empreinte, le fichier n'a donc pas été altéré")
            else:
                print("Désolé l'empreint n'est pas la même !!!")

        print("\n\n========================================= Faites un choix ============================================")
        print("| 1- Générer la paire de clé")
        print("| 2- Extraire la clé publique")
        print("| 3- creation de la clé secrete")
        print("| 4- crypter le fichier à transferer en utilisant une clé secrete")
        print("| 5- chiffrer la clé secrete")
        print("| 6- Generer une empreinte")
        print("| 7- Signer l'empreinte")
        print("\n| 8- dechiffrer la clé secrete")
        print("| 9- decrypter le fichier reçu")
        print("| 10- Verifier l'authentification")
        print("| 11- Comparer les fichier d'empreints")
        print("| q- pour quitter")
        choix = input("Choix: ")

main()