# Tester Ransomtion Protecware

Les tests doivent être réalisé sur une **machine virtuelle Linux**.\
La dernière version LTS d'Ubuntu est fortement recommandée.

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
Ransomtion Protectware protège maintenant votre ordinateur des ransomwares !

## Créer des fichiers de test

Pour permettre au ransomware de chiffrer des données, nous recommandons de créer des fichiers aléatoires :
```bash
cd ~
mkdir test
for i in {1..10}; do
	dd if=/dev/urandom of=test/$i.txt bs=1024 count=10240
done
```

## Lancer un ransomware

Pour tester la détection et autres étapes, démarrez un ransomware de test.\
Pour cela, nous avons mit à disposition une version améliorée de [GonnaCry](https://github.com/au2001/GonnaCry).

Téléchargez le projet depuis GitHub :
```bash
git clone https://github.com/au2001/GonnaCry.git
cd "GonnaCry/src"
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

## Utilisation de l'interface graphique

Une fois le ransomware exécuté, vous pouvez ré-ouvrir l'interface graphique pour voir le résultat :
```bash
sudo ./dist/RansomtionProtecware
```

Pour se connecter, utilisez les identifiants suivants :\
**Nom d'utilisateur :** admin\
**Mot de passe :** admin
