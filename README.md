# Ransomtion-Protecware (Version 1)
Projet pour contrer les ransomwares

## Table des matières
1. [Informations générales](#informations-generale)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Test](#test)
5. [FAQs](#faqs)

## Informations générales
***
Ransomtion Protecware est un programme python qui peut être couplé à un boitier. Ce projet permet à une petite entreprise de protéger ses ordinateurs contre les ransomwares.
Les différentes fonctions présentes sur le projet sont:
1. Actions pré-attaque :
    * Blacklist de programmes via leur nom
    * Ajout d'un programme à la whitelist
    * Sauvegarde automatique toutes les semaines <sup>[1](#myfootnote1)</sup>
2. Actions pendant une attaque :
    * Détection de plus de 20Go réécrits dans les fichiers <sup>[2](#myfootnote2)</sup>
    * Arrêt du programme concerné <sup>[3](#myfootnote3)</sup>
    * Coupure des interfaces réseaux
3. Actions post-attaque :
    * Récupération d'une sauvegarde

![startuml](http://www.plantuml.com/plantuml/png/TP91pjCm48NtFiLJsV17-YEnpOzGcmfM825G3-3QGsewiOizLYeXxiAMS_HYs7-hgfNIxNiltvjnPfb4HyaZgxHt_g2Z7f4J6Pq8lrMlpNw88Nkx3XmYLkmCzPn9zI5QYcVrYxFU3JjvDTGgnZ2TZU-Qn-2L-gCKqm-11CGQX7MHZBZgQICbcSMnIreeHxovjhomyzJTuCzAkmriNuIEqlLS9bIgqhGVcB3ufdqAOsNZQmn2PjAH5cKNeBjfwV3yZBUVm-3yqworkGWLP0dRqfCFDNhv26rTgVtmA8aEpXlEbcRngvyX2qv_mHhJpWaLM-xmzQKgVpvwnx_-iStw7NGgZq2ilQ48BZ3ZYB7by2kV_YcKTWKqpSUZa4zrvaDmNbBJ57csgkWBXOTpl6zjc7oBsjs1AjQcsPq_4TbwKI21TfQUwcKiIpoF_1y0)

## Prérequis
***
Les machines pouvant faire tourner ce programme sont les machines Ubuntu.
Le programme est installé sur chaque machine client.
### Backup
Pour le backup, un boîtier dois être fourni. Il est composé d'une raspberry paramétrée avec samba et un disque dur de la taille souhaitée

Vérifiez que les éléments suivants sont bien présents sur votre machine Ubuntu pour utiliser ce programme :

## Installation
***
Pour installer l'application, il est possible de cliquer sur le bouton Download ZIP sur Github ou d'écrire la ligne de commande suivante dans un terminal :
```bash
git clone https://github.com/Nexliath/Ransomtion-Protecware.git 
```

## Test
***


## Contributeurs
***

* DUFOUR    Lucie
* GARNIER   Aurélien
* GARNIER   Victor
* MANGEARD  Philippe
* MELINE    Stan
* RECOURSE  Déborah

## FAQs
***


<a name="myfootnote1">1</a>:: La sauvegarde autommatique n'est pas obligatoire et nécessite un boitier (ici un disque dur branché sur une raspberry) ou un serveur en ligne.
<a name="myfootnote2">2</a>:: Dans ce projet, nous ne nous occupons pas des ransomware couplés à des DOS sur la RAM.
<a name="myfootnote3">3</a>:: Si le programme n'est pas une menace, il peut être ajouté à la whitelist par l'utilisateur pour permettre son action.