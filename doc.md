
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
 - [presentation](<https://docs.google.com/presentation/d/133-CHRmHWjJb9L3z88HlBSB_0j9DTEWmJkn-5gD1Zp8/edit?usp=sharing>)

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

[source](<https://medium.com/@acpanjan/download-google-drive-files-using-wget-3c2c025a8b99>)

1. Extraire l'ID du document depuis l'address de partage
1. Telecharger le document avec la commande:

```
wget --no-check-certificate -O FILENAME 'https://docs.google.com/uc?export=download&id=FILEID'
```
Donc pour notre example:
```
wget --no-check-certificate -O FILENAME 'https://docs.google.com/uc?export=download&id=133-CHRmHWjJb9L3z88HlBSB_0j9DTEWmJkn-5gD1Zp8'
```

## Affichage d'une presentation

## Verification reguliere pour nouvelle version de la presentation

## Stockage de l'activite de la raspberry sur drive

