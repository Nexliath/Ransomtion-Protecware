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

![startuml](http://www.plantuml.com/plantuml/png/fPFFRXCn4CRlVefHERIDr21wJ15gqd832PK_TyUUP4szzdRiQIgXlWlNy1hxOemtObcL3K55Yf9e_Cqtttf-UvcofiorL-dMXKQJhe4J6fqGlgc5DhThYXpiLVIHOEwTmOLdL8j85cbNVUziSEigTmTpehZPrJzgNyUW7fNokCgG8r2HWNM49ZivKfoTTqbdP88NlVk5Tm5dGzkkCbr6RoyoFkJPmaiofMtjWakPdcim7FzwsgMRmXFN6OWUWqsgfDPXxH6ERdH8iIxF01yePZGRJNWaDmOm6vZEuEmCJgugwK82Bp-Cfw8vUHVNBfp2b9lfcpy4Cj85uzdYgDsNw4HwN4d4IEwE4Imce2vHYP5WwUCTjziqCkhVcm_4w4ERo5wA8xEUA0uPtc3AcaaQEC1IriFDYEcOQcWyhf3jshW9KpXPT0MeS6bZhQrszFJ2-_qFiis5rtkabzUOzEulU0GloOn3FnBpGCDmOl--VRvw1Je9NEXrC4Yz_DTE54WO-PfCtXOaKy6lYIxaD9b8UVurSfQszZju3PlAPVGkPJavAW7t7FTtqytlQHzvfF7-WxUtlrEL8TVjDgF9MB1ijm_jrd3tNjbZ3WCm9OR7LUwuYjmmxSXrGJfNsXI81LhK_308z3p_EL7x8uDbQ2YkITSrWebb8w7T_hVx9mnP5oB0oaSQAhTQ4TPIteV5UOV5a6k4fFaUrvei7g1Y_xoUZBz8XdIS_wPZ1hdlAVeeTA9Iwb5ToZ7N_YS0)

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
