# Tester Ransomtion Protecware

Les tests doivent être réalisé sur une **machine virtuelle Linux**.\
La dernière version LTS d'Ubuntu est fortement recommandée.

Pour tester Ransomtion Protecware, [téléchargez-le sur GitHub](https://github.com/Nexliath/Ransomtion-Protecware/releases/download/v0.1-alpha.1/RansomtionProtecware).

Ensuite, lancez le programme **en super-utilisateur** avec `sudo ./RansomtionProtecware`.\
Cliquez sur le bouton `Allumer` en bas de l'interface graphique. Vous pouvez ensuite fermer la fenêtre.

Enfin, démarrez un ransomware de test, tel que [GonnaCry](https://github.com/Nexliath/Ransomtion-Protecware/releases/download/v0.1-alpha.1/gonnacry) livré avec notre solution.

## Script complet head-less

```bash
wget https://github.com/Nexliath/Ransomtion-Protecware/releases/download/v0.1-alpha.1/RansomtionProtecware
sudo ./RansomtionProtecware &
sleep 10
sudo /var/lib/ransomtion-protecware/daemon

wget https://github.com/Nexliath/Ransomtion-Protecware/releases/download/v0.1-alpha.1/gonnacry
./gonnacry
```
