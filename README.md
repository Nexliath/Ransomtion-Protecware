# Ransomtion Protecware
Application anti-virus spécialisée contre les ransomwares réalisée comme projet au sein d'Efrei Paris lors du Mastercamp L3 2021.

## Table des matières
1. [Informations générales](#informations-générales)
2. [Compatibilité](#compatibilité)
3. [Option de sauvegardes](#option-de-sauvegardes)
4. [Installation et lancement](#installation-et-lancement)
5. [Contributeurs](#contributeurs)

## Informations générales
Ransomtion Protecware est un programme développé en Python compatible Linux et pouvant être utilisé en parallèle d'un serveur de backup.\
Ce projet permet à une entreprise PME, ou même un particulier, de protéger son infrastructure IT contre les ransomwares.

Les différentes fonctionnalités présentes sont :
1. Actions pré-attaque :
    * Interface graphique de contrôle de l'application (lancement/désactivation)
    * Whitelist d'un programme de confiance pour autoriser son exécution
    * [Sauvegarde des données sensibles de l'utilisateur](#option-de-sauvegardes)
2. Actions au cours d'une attaque :
    * Détection de l'exécution d'un ransomware
        - Volumes d'écriture suspects (> 10 Go lus et > 20 Go écrits)
        - Création de fichiers reconnus comme utilisés par des ransomwares (extensions .WNNCRY etc.)
        - Utilisation abusive des ressources (> 80% du CPU)
    * Coupure des interfaces réseau
    * Arrêt du programme concerné
3. Actions post-attaque :
    * Tentative de déchiffrement automatique des fichiers chiffrés
    * Restauration d'une sauvegarde
    * Visibilité de l'historique des ransomwares bloqués

![startuml](http://www.plantuml.com/plantuml/png/fLDDJnin4BtxLupe0OZ4LkKOK4K2lRLIHJ_kZZr9NBns67i8KiL_wJNz6_l7Eju8Dg4BALIAacZcpNlFzfkpb3LbhhrALouiDEaQEA7H2U6d6cjpDQF8mPv77mb6tXaSUqOrZcIHrjLFpWOtc-UsCIAAotNzY_Pr3EfEAO_J33a25HXOHsYoavRYxBnBEYCJl7bWF_4ku72JjgrKa-ZjISRRF1nxSQQqhLrmATDh2JRbJwlMNGMFM8SWU0msgU9QXvb7sBlK8SMwd04-KynebffmJsuCOBX1EeIZ8pWudyiK4dZvOJmKpC77E7FX42fULE__0eYa2yQpnLwwxz49T7yk5YEvQqQmc81QHyL6WecFrzoiKe_K2uQVjT6PDf6z57kq7YDs45wYP9591ZZ0H9w75psaVQWjudx4QMNZCbHmC6uBCCU9ZRMssj7Z2-_Ul_CsahpU8BszmAJNVy4ZU75c7FeUcpi6_a7nH-GiKyqly1ec9QvU87rI_SXjZVkT_dR-3dII0AE4pI0zMBf_TmKYBr-3mOSI-rGYleWkv3GOI7bRR3bt6OkOTFQAioVQtVsBVhTHkyxIpR_qlhf9LKGkcbL6ax54lrdTDYl3xUxQVGuRuHSR7gUvpMxa1TDwEroGoQasPL5aCL3pxRQXL_2FY9hV6Ip3WkACT5qZc5XU93Ih_sR_YY7haZgmyf61kPjE2MiCJyRYk8t5vkuW9CqtEDDaSKSgdj6xJyQpbhfq77Vf649-c2duAEb4fTITEfCsr_uF)

## Compatibilité
Ransomtion Protecware doit être installé sur chaque machine à protéger.\
Il peut être installé sur un serveur en faisant appel uniquement au daemon.\
Sur les ordinateurs clients, il est fortement recommandé d'utiliser l'interface graphique fournie.

L'application est (pour le moment) exclusivement compatible avec les systèmes d'exploitation Linux. Une version Windows et macOS est prévue.\
Seule la version LTS la plus récente d'Ubuntu est supportée et testée.

## Option de sauvegardes
En faisant appel à nos services complémentaires, nous pouvons mettre en place un serveur sécurisé de sauvegardes au sein de votre réseau d'entreprise.\
Des sauvegardes incrémentales (fichiers modifiés uniquement) des données utilisateur sensibles (dossier au choix) sont alors réalisés chaque semaine.\
Un backup complet est réalisé chaque mois pour minimiser les risques de corruption des fichiers.

Pour le mettre en place manuellement, exécuter le fichier `backups/setup.py` en tant que super-utilisateur et répondre aux questions.\
La connexion SSH est faite par clé RSA. Il faut donc générer une paire de clés et installer la clé publique sur le serveur de stockage.\
Il est conseillé de choisir soit le répertoire `/home`, soit le répertoire de l'utilisateur `/home/YourLoginHere`, soit la racine `/` (par défaut).

### Obtenir l'adresse IP du NAS

Sur un Raspberry Pi, suivre les instructions suivantes :
1. Allumer et brancher le boitier à un écran
2. Se connecter avec l'utilisateur dont les identifiants par défaut sont nas:123
3. Ouvrir un terminal et taper la commande "ip show enp0s3"
4. Recopier l'adresse IP affichée

### Mettre en place la clé RSA sur le NAS

Sur la machine client, exécuter :
```bash
ssh-keygen -f ~/.ssh/id_rsa_ransomtion_protecware_backups -t rsa -b 4096
ssh-copy-id -i ~/.ssh/id_rsa_ransomtion_protecware_backups $USERNAME@$IP
```
En remplaçant `$USERNAME` et `$IP` par le nom d'utilisateur du compte (`nas` par défaut) et l'adresse IP du NAS obtenue à l'étape précédente.\
Entrer le mot de passe du compte lorsque demandé (`123` par défaut).

## Installation et lancement
Pour installer l'application depuis les sources, récupérez le répertoire de l'application :
```bash
git clone https://github.com/Nexliath/Ransomtion-Protecware.git 
cd Ransomtion-Protecware
```

Installez les dépendances :
```bash
pip3 install -r daemon/requirements.txt
pip3 install -r gui/requirements.txt
pip3 install pyinstaller
```

Puis exécutez le fichier `build.sh` en tant que super-utilisateur :
```bash
./build.sh
```

Deux exécutables binaires sont alors créés dans le dossier `dist`.\
Pour installer le programme et lancer l'interface graphique, utilisez l'exécutable `RansomtionProtecware` en tant que super-utilisateur :
```bash
sudo ./dist/RansomtionProtecware
```

Pour lancer le logiciel en head-less (daemon uniquement) sur un serveur par exemple, utilisez l'exécutable `RansomtionProtecware-daemon` en tant que super-utilisateur :
```bash
sudo ./dist/RansomtionProtecware-daemon &
```

## Contributeurs

* <img src="https://avatars.githubusercontent.com/u/66913204?s=64&v=4" width="48" alt="Loucye" /> [DUFOUR    Lucie](https://github.com/Loucye)
* <img src="https://avatars.githubusercontent.com/u/6292584?s=64&v=4" width="48" alt="au2001" /> [GARNIER   Aurélien](https://github.com/au2001)
* <img src="https://avatars.githubusercontent.com/u/49352273?s=64&v=4" width="48" alt="Nexliath" /> [GARNIER   Victor](https://github.com/Nexliath)
* <img src="https://avatars.githubusercontent.com/u/56166579?s=64&v=4" width="48" alt="Malpaga" /> [MANGEARD  Philippe](https://github.com/Malpaga)
* <img src="https://avatars.githubusercontent.com/u/58551445?s=64&v=4" width="48" alt="Scorr" /> [MÉLINE    Stan](https://github.com/Sccor)
* <img src="https://avatars.githubusercontent.com/u/21981282?s=64&v=4" width="48" alt="Irraky" /> [RECOURSÉ  Déborah](https://github.com/Irraky)
