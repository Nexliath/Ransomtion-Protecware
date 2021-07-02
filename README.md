# Ransomtion Protecware
Application anti-virus spécialisée contre les ransomwares réalisée comme projet au sein d'Efrei Paris lors du Mastercamp L3 2021.

## Table des matières
1. [Informations générales](#informations-générales)
2. [Compatibilité](#compatibilité)
3. [Option de sauvegardes](#option-de-sauvegardes)
4. [Installation et lancement](#installation-et-lancement)
5. [Tests](#tests)
6. [Contributeurs](#contributeurs)

## Informations générales
Ransomtion Protecware est un programme développé en Python compatible Linux et pouvant être utilisé en parallèle d'un serveur de backup.\
Ce projet permet à une entreprise PME, ou même un particulier, de protéger son infrastructure IT contre les ransomwares.

Les différentes fonctionnalités présentes sont :
1. Actions pré-attaque :
    * Interface graphique de contrôle de l'application (lancement/désactivation)
    * Whitelist d'un programme de confiance pour autoriser son exécution
    * [Sauvegarde des données sensibles de l'utilisateur](#option-de-sauvegardes)
2. Actions au cours d'une attaque :
    * Détection de l'exécution d'un ransomware
        - Volumes d'écriture suspects (> 10 Go lus et > 20 Go écrits)
        - Création de fichiers reconnus comme utilisés par des ransomwares (extensions .WNNCRY etc.)
        - Utilisation abusive des ressources (> 80% du CPU)
    * Coupure des interfaces réseau
    * Arrêt du programme concerné
3. Actions post-attaque :
    * Tentative de déchiffrement automatique des fichiers chiffrés
    * Restauration d'une sauvegarde
    * Visibilité de l'historique des ransomwares bloqués

![startuml](http://www.plantuml.com/plantuml/png/TP91pjCm48NtFiLJsV17-YEnpOzGcmfM825G3-3QGsewiOizLYeXxiAMS_HYs7-hgfNIxNiltvjnPfb4HyaZgxHt_g2Z7f4J6Pq8lrMlpNw88Nkx3XmYLkmCzPn9zI5QYcVrYxFU3JjvDTGgnZ2TZU-Qn-2L-gCKqm-11CGQX7MHZBZgQICbcSMnIreeHxovjhomyzJTuCzAkmriNuIEqlLS9bIgqhGVcB3ufdqAOsNZQmn2PjAH5cKNeBjfwV3yZBUVm-3yqworkGWLP0dRqfCFDNhv26rTgVtmA8aEpXlEbcRngvyX2qv_mHhJpWaLM-xmzQKgVpvwnx_-iStw7NGgZq2ilQ48BZ3ZYB7by2kV_YcKTWKqpSUZa4zrvaDmNbBJ57csgkWBXOTpl6zjc7oBsjs1AjQcsPq_4TbwKI21TfQUwcKiIpoF_1y0)

## Compatibilité
Ransomtion Protecware doit être installé sur chaque machine à protéger.\
Il peut être installé sur un serveur en faisant appel uniquement au daemon.\
Sur les ordinateurs clients, il est fortement recommandé d'utiliser le script d'installation et l'interface graphique fournie.

L'application est (pour le moment) exclusivement compatible avec les systèmes d'exploitation Linux. Une version Windows et macOS est prévue.\
Seule la version LTS la plus récente d'Ubuntu est supportée et testée.

## Option de sauvegardes
En faisant appel à nos services complémentaires, nous pouvons mettre en place un serveur sécurisé de sauvegardes au sein de votre réseau d'entreprise.\
Des sauvegardes incrémentales (fichiers modifiés uniquement) des données utilisateur sensibles (dossier au choix) sont alors réalisés chaque semaine.\
Un backup complet est réalisé chaque mois pour minimiser les risques de corruption des fichiers.

## Installation et lancement
Pour installer l'application depuis les sources, récupérez le répertoire de l'application :
```bash
git clone https://github.com/Nexliath/Ransomtion-Protecware.git 
cd Ransomtion-Protecware
```

Puis exécutez le fichier `build.sh` en tant que super-utilisateur :
```bash
sudo ./build.sh
```

Une adresse ip est demandée:
### Si le boitier de backup est installé
ll faut entrer l'adresse ip du boitier.  
Pour la connaitre, il faut suivre les étapes suivantes :
1. Brancher le boitier à un écran
2. Se connecter avec l'utilisateur dont le couple login:password est nas:123
3. Ouvrir un terminal
4. Entrer la commande "ip -c show enp0s3"
5. Récupérer l'adresse ip affichée  
Il n'y a plus qu'à recopier cette adresse.  
Une confirmation du choix est proposée.  
Il faut vérifier que l'adresse ip a bien été remplie et valider.  
Il faut ensuite choisir le répertoire à sauvegarder.  
*Il est conseillé de choisir soit le répertoire "/home", soit le répertoire de l'utilisateur "/home/YourLoginHere", soit la racine "/".*  
Une nouvelle confirmation permet de corriger les potentielles erreurs.  
### Sans présence de boitier
Il suffit de ne rien entrer.  
Une confirmation du choix est proposée.  
Il faut alors appuyer à nouveau sur entrer.
### Ajouter le système de backup après une première installation
Si le programme a déjà été configuré mais qu'un boitier de backup a été acquis, il est toujours possible de mettre en place le système de sauvegardes.  
Pour cela, il faut se placer dans le dossier Ransomtion-Protecware puis lancer les commandes suivantes :
``` bash
sudo rm ~/.backup.sh
sudo ./build.sh
```
Puis suivre l'installation à partir de l'étape [d'installation du boitier].(#Si-le-boitier-de-backup-est-installé)  
 <br>
 <br> 

Le reste de l'installation est fait automatiquement.  
Deux exécutables binaires sont créés dans le dossier `dist`.\
Pour lancer l'interface graphique, utilisez l'exécutable `RansomtionProtecware` :
```bash
sudo ./dist/RansomtionProtecware
```
Pour lancer le logiciel en head-less (daemon uniquement) sur un serveur par exemple, utilisez l'exécutable `RansomtionProtecware-daemon` :
```bash
sudo ./dist/RansomtionProtecware-daemon &
```

## Tests

*Rédaction des tests en cours. Cette section sera mise à jour avec le contenu nécessaire pour exécuter les tests.*

## Contributeurs

* <img src="https://avatars.githubusercontent.com/u/66913204?s=64&v=4" width="48" alt="Loucye" /> [DUFOUR    Lucie](https://github.com/Loucye)
* <img src="https://avatars.githubusercontent.com/u/6292584?s=64&v=4" width="48" alt="au2001" /> [GARNIER   Aurélien](https://github.com/au2001)
* <img src="https://avatars.githubusercontent.com/u/49352273?s=64&v=4" width="48" alt="Nexliath" /> [GARNIER   Victor](https://github.com/Nexliath)
* <img src="https://avatars.githubusercontent.com/u/56166579?s=64&v=4" width="48" alt="Malpaga" /> [MANGEARD  Philippe](https://github.com/Malpaga)
* <img src="https://avatars.githubusercontent.com/u/58551445?s=64&v=4" width="48" alt="Scorr" /> [MÉLINE    Stan](https://github.com/Sccor)
* <img src="https://avatars.githubusercontent.com/u/21981282?s=64&v=4" width="48" alt="Irraky" /> [RECOURSÉ  Déborah](https://github.com/Irraky)
