# police-interpol

Note for english-speaking readers : there is no english version of this repository to date, but feel free to send me a message if you wish to see it translated.

Cette collection de scripts Python pour FontForge et Blender vise à automatiser l’exportation, à partir de polices de caractères existantes, d’une ou plusieurs versions sans courbe de celles-ci.

![exemple](images/exemple.png)

> Ci-dessus, un exemple d'un même caractère interpolé avec différentes résolutions (respectivement 1, 2 et 3 de gauche à droite).

## fichier de configuration

Vous devez préparer avant usage un fichier de configuration en y renseignant 3 propriétés :

  * repertoire_sortie : chaîne de caractère, indique le répertoire de sortie.
  * resolutions : tableau d’entiers, indique les différentes résolutions de police à générer.
  * commentaire : chaîne de caractère, sera utilisé comme métadonnée de commentaire pour les fichiers en sortie
  * fichiers_sources : tableau de chaînes de caractères, indique les chemins des fichiers à traiter.

Le chemin du fichier de configuration doit ensuite être renseigné avant usage dans chacun des fichiers. py.

Concernant l’usage de Python dans FontForge, vous pouvez vous référer à mon autre dépôt fontforge-documentation.

## Usage

Les fichiers 0, 2 & 3 sont à utiliser avec FontForge, le fichier 1 avec Blender.

## notes

Le programme ne modifie pas l'identifiant unique de chaque police, vous devrez effectuer manuellement cette opération vous-même.

## Licence

GNU GPL 3
