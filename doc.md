
# Verification basic

Nous allons commencer par verifier que la carte raspberry est bien installer, et que
le systeme officiel fonctionne

## Materiel

Afin de pouvoir la raspberry, il faut:

- une carte raspberry
- une carte SD de 8 Go
- adaptateur carte SD pour connexion a l'oridnateur
- une alimentation secteur vers USB A
- un cable HDMI pour connecter la raspberry a un ecran
- un ordinateur

## Systeme officiel

La raspberry met a disposition un utilitaire pour facilement installer le systeme: [rpi-imager](<https://www.raspberrypi.com/software/>)

### Lancement de l'utilitaire

L'utilitaire rpi-imager permet une installation basic de la carte.

Il faut d'abord connecter la carte SD a l'ordinateur avant de lancer l'utilitaire.

Il consiste de 4 boutons:

- Selection de l'OS (le systeme)
- Selection de la carte SD
- Configuration de l'image (bouton avec logo de roue crantee/molette) (qui apparaitra une fois le system selectionne)
- Ecriture de l'OS sur la carte SD

### Configuration du systeme

Dans l'utilitaire, nous allons configurer:

- Le mot de passe pour se connecter au raspberry
- Le mot de passe du wifi
- Et autre

En suivant les instructions suivantes (ou utiliser la configuration attachee):

1. Selection de l'OS (le systeme)
   1. Cliquer le bouton et selectionner: "Raspberry PI OS (32 bit)"
1. Selection de la carte SD
   1. Cliquer sur la premiere proposition afficher qui doit etre votre carte SD
1. Configuration de l'image (bouton avec logo de roue crantee/molette)
   1. Cliquer sur la case "Activer SSH"
   1. Cliquer sur la case "Configure le nom d'utilisateur et mot de passe"
      1. Utilisateur: "pi"
      1. Mot de passe: "pi"
   1. Cliquer sur la case "Configurer le reseau WiFI"
      1. SSID: mettre le nom du reseau wifi
      1. Password: mettre le mot de passe du reseau wifi

### Installation du systeme

Suiver les instructions suivantes:

1. Ecriture de l'OS sur la carte SD
   1. Appuyer sur le bonton et laisser l'utilisateur
   1. Attendre que l'utilitaire ait fini

### Test de la raspberry

Faire:

1. Inserer la carte SD dans la raspberry
1. Connecter la raspberry a une ecran
1. Connecter l'alimentation USB

La raspberry va demarrer

1. Des leds s'allume sur la carte indiquant que le systeme est sous tension et demarre
1. L'ecran auquel est connect la reapsberry va afficher differentes choses (cela peut prendre 1/2 minutes):
   1. Un ecran avec un degrade de couleur (2 seconds)
   1. ecran noir (30 secondes)
   1. ecran avec le logo et du texte dessous
   1. ecran noir (45 secondes)



# Configuration de la presentation a afficher

1. Creer un dossier ou placer les fichiers liee a la presentation
1. Partager ce fichier en LECTURE avec n'importe qui sur internet
1. Deplacer la presentation dans le dossier
   1. Partager ce fichier en LECTURE avec n'importe qui sur internet
   1. Recuperer le lien du document
1. Creer un fichier "log" dans le dossier
   1. Partager ce fichier en EDITION avec n'importe qui sur internet
   1. Recuperer le lien du document

Exemmple:
 - [log](<https://docs.google.com/document/d/1BNW0uXCjVyg87TGipDLzPzvVrpjbDQw9J5DBHsRWNfY/edit?usp=sharing>)
 - [presentation](<https://docs.google.com/presentation/d/1awmTttnjZcQe5-KutgFCA4hrhCaiEiTH/edit?usp=sharing&ouid=104476098094281710249&rtpof=true&sd=true>)

# Modification pour afficher une presentation

## Desactiver la veille de l'ecran

[source](<https://pimylifeup.com/raspberry-pi-disable-screen-blanking/>)
Etapes:

En ligne de commande:

1. sudo raspi-config
1. Display options
1. Screen blanking
1. Select "NO"
1. Reboot the pi when asked

## Telechargement d'une presentation depuis google drive

WARNING: Si le fichier a ete cree dans drive, il ne sera pas possible de le telecharger, dans ce cas, telecharger manuellement et uploader le fichier.

[source](<https://github.com/wkentaro/gdown)

1. Installer le package python

```
pip install gdown
```

1. Telecharger le document avec gdown:

```
gdown <LINK> <OUTPUT>
```
Donc pour notre example:
```
python3 cb_kiosk/dl_from_drive.py "https://docs.google.com/presentation/d/1awmTttnjZcQe5-KutgFCA4hrhCaiEiTH/edit?usp=sharing&ouid=104476098094281710249&rtpof=true&sd=true" flprez.ppt
```

## Affichage d'une presentation

## Verification reguliere pour nouvelle version de la presentation

## Stockage de l'activite de la raspberry sur drive


https://docs.google.com/presentation/d/e/2PACX-1vSIhmvpmyYEpqDX-lNgvpaEJWoNNKnnmSC14NuucIkadE2bIb_a4D9ThcITqACFVw/pub?start=true&loop=true&delayms=15000


=> It seems there is no OS solution to display a ppt as a slideshow
+ google slides do not integrate delays....bbuiltin delay between slides is 4 seconds !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

ppt -> info timing -> slideshow is just rendering + timing
odp -> 
gsslides -> a mess...

# Installation sur board pour mode kiosk

## Impress

Sur la board:

```
sudo apt update
sudo apt install -y default-jre
sudo apt install -y libreoffice-java-common
sudo apt install -y libreoffice-writer
```

## Script pour telecharger la presentation

```
scp dl_from_drive.py pi@<pi network address>/home/pi/prez
```

## Lancement de la presentation

```
python3 dl_from_drive.py <lien de partage de la presentation>
impress --show presentation.ppt
```

## Tunnel SSH pour controler la board a distance

[source](<https://doc.ubuntu-fr.org/tutoriel/reverse_ssh>)
-> La board est le systeme "distant" et la machine d'un utilisateur est "local".

Ce systeme permettra de faire que la board se connecte a une machine particuliere d'un utilisateur,
et donc l'utilisateur pourra se connecter sur la board sans avoir ses informations.

### Parametres

Voici les differents parametres:

- PI_USERNAME = pi
- PI_SSH_PORT = 22
- USERNAME = eramox
- USER_IP_ADDR = 88.170.53.149
- USER_SSH_PORT = 22222
- EXCHANGE_PORT = 26000

### Configuration

La cle de la board doit etre ajoute a la machine a laquelle la board va se connecter

```
ssh-copy-id -p <USER_SSH_PORT> <USERNAME>@<USER_IP_ADDR> 
ssh-copy-id -p 22222 eramox@88.170.53.149
```

### Installation

Sur la board:
```
sudo apt update
sudo apt install -y autossh
sudo nano /etc/systemd/system/autossh.service
```

avec le contenu:

```
[Unit]
Description=Keep a tunnel open on port 22
After=network.target
 
[Service]
# User=<PI_USERNAME>
User=pi
# ExecStart=/usr/bin/autossh -o ServerAliveInterval=60 -NR <EXCHANGE_PORT>:localhost:<PI_SSH_PORT> -p <USER_SSH_PORT> <USERNAME>@<USER_IP_ADDR>
ExecStart=/usr/bin/autossh -o ServerAliveInterval=60 -NR 26000:localhost:22 -p 22222 eramox@88.170.53.149
Restart=on-failure
 
[Install]
WantedBy=multi-user.target
```

Et finalement:

```
sudo systemctl --now enable autossh.service
sudo systemctl status autossh
```

Il sera possible de se connecter a la board depuis la machine utilisateur avec la commande:

```
ssh -p <EXCHANGE_PORT> <PI_USERNAME>@localhost
ssh -p 26000 pi@localhost
```

## Programs

### Display when calling from ssh

```
export DISPLAY=:0.0
```

### convert ppt to pdf

```
soffice --headless --convert-to pdf <name>.ppt
```
The resulting file will be <name>.pdf

### display

```
impressive --auto 15 --fullscreen --page-progress --wrap --nocursor --nologo --noclicks --nooverview --clock <name>.pdf
```












