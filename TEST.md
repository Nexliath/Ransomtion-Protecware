# Tester Ransomtion Protecware

Les tests doivent être réalisé sur une **machine virtuelle Linux**.\
La dernière version LTS d'Ubuntu est fortement recommandée.

Assurez-vous d'avoir les logiciels utilisés :
```bash
sudo apt-get install git python3-pip python#-tk
```

Pour tester Ransomtion Protecware, téléchargez le projet depuis GitHub :
```bash
git clone https://github.com/Nexliath/Ransomtion-Protecware.git
cd "Ransomtion-Protecware"
```

Ensuite, installez les dépendences nécessaires :
```bash
pip3 install -r gui/requirements.txt
pip3 install -r daemon/requirements.txt
pip3 install pyinstaller
export PATH="$PATH:$HOME/.local/bin"
```

Compilez désormais le programme depuis les sources :
```bash
./build.sh
```

Enfin, lancez le programme **en tant que super-utilisateur** :
```bash
sudo ./dist/RansomtionProtecware
```
Cliquez sur le bouton `Allumer` en bas de l'interface graphique et fermez la fenêtre.\
Ransomtion Protectware protège maintenant votre ordinateur des ransomwares !\
Il se lance automatiquement dès lors que la machine s'allume.

![Ransomtion Protecware](https://user-images.githubusercontent.com/6292584/124626195-be9ae580-de7e-11eb-8319-9d07a3ee80d4.png)

## Créer des fichiers de test

Pour permettre au ransomware de chiffrer des données, nous recommandons de créer des fichiers aléatoires :
```bash
cd ~
mkdir test
for i in {1..10}; do
	dd if=/dev/urandom of=test/$i.txt bs=1024 count=10240
	md5sum test/$i.txt >> test/md5sums
done
```

## Lancer un ransomware

Pour tester la détection et autres étapes, démarrez un ransomware de test.\
Pour cela, nous avons mit à disposition une version améliorée de [GonnaCry](https://github.com/au2001/GonnaCry).

Téléchargez le projet depuis GitHub :
```bash
git clone https://github.com/au2001/GonnaCry.git
cd GonnaCry/src
```

Installez les dépendances :
```bash
pip3 install -r requeriments.txt
```

Compilez depuis les sources :
```bash
python3 build.py
```

Exécutez le ransomware (pensez à prendre un snapshot de la VM avant) :
```bash
./dist/gonnacry
```

![GonnaCry](https://user-images.githubusercontent.com/6292584/124626504-06217180-de7f-11eb-8c65-9dd33341b021.png)

## Vérification de l'efficacité

Peu après que le ransomware dépasse les 100 Mo écrits, il sera bloqué par Ransomtion Protecware.\
L'inscription `Killed` apparaîtra dans la fenêtre d'exécution du ransomware.

![GonnaCry Killed](https://user-images.githubusercontent.com/6292584/124632532-ba71c680-de84-11eb-83ff-a748a9d279ee.png)

Le déchiffrement automatique commence aussitôt et se termine rapidement.\
Après quelques secondes, les fichiers .GNNCRY devraient donc tous avoir été déchiffrés :
```bash
find ~ -name "*.GNNCRY"
```
La commande ci-dessus ne devrait afficher aucun résultat, ou au plus un fichier qui a été partielement chiffré.\
Dans ce cas, puisque l'original existe toujours sur le disque, il suffit de supprimer ce fichier.

La connexion Internet ayant été interrompue, il est possible de la rétablir avec un reboot ou par ligne de commande :
```bash
sudo ip link set enp0s3 up
```

## Utilisation de l'interface graphique

Une fois le ransomware exécuté, vous pouvez ré-ouvrir l'interface graphique pour voir le résultat :
```bash
sudo ./dist/RansomtionProtecware
```

Une entrée `gonnacry` sera rajoutée dans la liste des logiciels bloqués.

Les options disponibles à tester sont : changement de thème et de langue, ajout/suppression de logiciels de la whitelist, allumage/extinction du logiciel.\
Pour se connecter lors de l'ajout de logiciels à la whitelist, utilisez les identifiants suivants :\
**Nom d'utilisateur :** admin\
**Mot de passe :** admin
