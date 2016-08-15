'''Génère des ufo et otf d'après les informations contenues dans le fichier de configuration.
'''

import fontforge
import json

# fichier de configuration
fichier_de_configuration = '/chemin/du/fichier/de/configuration'

class Configuration:
    '''Objet permettant de lire et écrire un fichier de configuration au format JSON'''
    def __init__(self,chemin_fichier_config):
        '''Transfère le contenu d'un fichier vers l'objet Configuration
        Chemin -> Void'''
        try:
            # ouverture du fichier
            donnees_json = open(chemin_fichier_config).read()
            # parsing des données
            configuration = json.loads(donnees_json)
            # récupération des paramètres
            # dont localisation du fichier pour sauvegarder plus tard
            self.chemin_fichier_config = chemin_fichier_config
            self.repertoire_sortie = configuration['repertoire_sortie']
            self.resolutions = configuration['resolutions']
            self.commentaire = configuration['commentaire']
            self.fichiers_sources = configuration['fichiers_sources']
            self.fichiers_json_pour_interpolation = configuration['fichiers_json_pour_interpolation']
            self.fichiers_json_interpoles = configuration["fichiers_json_interpoles"]
            self.fichiers_ufo = configuration["fichiers_ufo"]
        except Exception as e:
            print(e)

    def sauvegarder(self):
        '''Sauve l'objet configuration dans le fichier source
        Void -> Void'''
        print('sauvegarde du fichier de configuration...')
        # ouverture du fichier
        f = open(self.chemin_fichier_config,'w')
        # écriture au format JSON
        f.write(str(self))
        # fermeture du fichier
        f.close()
        print('fichier de configuration sauvegardé !')

    def __str__(self):
        '''Retourne l'objet Configuration au format JSON
        Void -> String'''
        return "{\"repertoire_sortie\":\"%s\",\"resolutions\":%s,\"commentaire\":\"%s\",\"fichiers_sources\":%s,\"fichiers_json_pour_interpolation\":%s,\"fichiers_json_interpoles\":%s,\"fichiers_ufo\":%s}" % (self.repertoire_sortie, self.resolutions, self.commentaire, json.dumps(self.fichiers_sources), json.dumps(self.fichiers_json_pour_interpolation), json.dumps(self.fichiers_json_interpoles),json.dumps(self.fichiers_ufo))

def go():
    '''programme principal, génère les otf
    Void -> Void'''
    # pour chaque police en entrée
    for chemins_ufo_resolution in config.fichiers_ufo:
        # pour chaque ufo précédement généré par police
        for chemin_ufo in chemins_ufo_resolution:
            # on ouvre le ufo
            police = fontforge.open(chemin_ufo)
            # on construit le chemin
            chemin_otf = config.repertoire_sortie + '/otf/' + chemin_ufo.split('/')[-1][:-3] + 'otf'
            # on génère le .otf
            police.generate(chemin_otf)
            # message
            print('→ ' + chemin_otf)

# import de la configuration
config = Configuration(fichier_de_configuration)

# lancement du programme principal
go()

print('fin du programme')
