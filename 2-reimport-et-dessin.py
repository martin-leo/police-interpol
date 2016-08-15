'''
# Import JSON

Importe la police interpolée, redessine les glyphes, met à jour les métadonnées et génère les UFO.
'''

import fontforge
import json

# paramétrage

# fichier de configuration
fichier_de_configuration = '/chemin/du/fichier/de/configuration'

# fermeture de la police après traitement (risque de bug)
fermer_police = False

# traitement des métadonnées : veillez à adapter la fonction traitement_metadonnees !
traiter_metadonnees = False

def dessiner_glyphe(police, glyphe):
  '''
  Dessine le glyphe donné d'une police
  Police, Glyph -> String
  '''
  selecteur = glyphe['glyphname'].encode('utf8')
  try:
    # on créé un "pen"
    pen = police[selecteur].glyphPen()
    # on récupère les données de l'approche droite qui va sauter lors du dessiner
    approche_droite = police[selecteur].right_side_bearing
    # pour chaque contour du glyphe
    for contour in glyphe['contours']:
      # on le place sur le premier point
      pen.moveTo( ( round( float(contour['points'][0]['x']) ), round( float(contour['points'][0]['y']) ) ) )
      # pour chaque point du contour à l'exception du premier
      for point in contour['points'][1:]:
        # on trace une ligne jusqu'au prochain point
        pen.lineTo( ( round( float(point['x']) ), round( float(point['y']) ) ) )
      # puis on clot le chemin dessiné
      pen.closePath();
    # on rerègle l'approche droite qui a sauté
    police[selecteur].right_side_bearing = approche_droite
    # on efface le 'pen' ce qui force le raffraîchissement de l'interface
    pen = None
  except Exception as e:
    print(e)

def traitement_metadonnees(police, resolution, font_name_original, family_name_original, full_name_original, commentaire):
    '''Procède au traitement des métadonnées.
    Attention, ce traitement dépend des métadonnées de la typo, ce passage est à adapter !
    Font, Int, String, String, String, String -> Void'''
    # font name
    font_name = font_name_original.split('-')
    font_name = font_name[0] + 'Interpol' + str(resolution) + '-' + font_name[1]
    police.fontname = font_name
    # family name
    family_name = family_name_original + ' Interpol ' + str(resolution)
    police.familyname = family_name
    # full name
    full_name = full_name_original.split('-')
    full_name = full_name[0] + 'Interpol' + str(resolution) + '-' + full_name[1]
    police.fullname = full_name
    # commentaire
    if commentaire == 'reset':
      police.comment = ''
    elif commentaire != '':
      police.comment = commentaire

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
        return "{\"repertoire_sortie\":\"%s\",\"resolutions\":%s,\"commentaire\":\"%s\",\"fichiers_sources\":%s,\"fichiers_json_pour_interpolation\":%s,\"fichiers_json_interpoles\":%s,\"fichiers_ufo\":%s}" % (self.repertoire_sortie, self.resolutions, self.commentaire, json.dumps(self.fichiers_sources), json.dumps(self.fichiers_json_pour_interpolation), json.dumps(self.fichiers_json_interpoles), json.dumps(self.fichiers_ufo))

def go():
    '''Procède au réimport des police, à leur dessin et au traitement des métadonnées.
    Void -> Void'''
    # on va garder traces des fichiers ufo généré
    chemins_ufo = []
    # pour chaque police
    for index_source in range(0,len(config.fichiers_sources)):
        chemin_source = config.fichiers_sources[index_source]
        print('traitement de ' + chemin_source)
        police = fontforge.open(chemin_source)
        # metadonnées de base
        font_name_original = police.fontname
        family_name_original = police.familyname
        full_name_original = police.fullname
        # pour chaque police on va garder en mémoire les .ufo exportés
        chemins_ufo_police = []
        # pour chaque résolution
        for index_resolution in range(0,len(config.resolutions)):
            resolution = config.resolutions[index_resolution]
            # formation du chemin
            chemin_json_interpole = config.fichiers_json_interpoles[index_source][index_resolution]
            # import des données
            json_data = open(chemin_json_interpole).read()
            data = json.loads(json_data)
            # dessin des glyphes
            for glyphe in data['glyphs']:
              dessiner_glyphe(police, glyphe)
            # modification de metadonnées de la police
            # (partielle et à compléter manuellement)
            if (traiter_metadonnees):
                traitement_metadonnees(police, resolution, font_name_original, family_name_original, full_name_original, config.commentaire)
            # chemin pour export
            chemin_export_ufo = chemin_source.split('/')[-1][:-4].split('-')
            chemin_export_ufo = config.repertoire_sortie + '/ufo/' + chemin_export_ufo[0] + 'Interpol' + str(resolution) + '-' + chemin_export_ufo[1] + '.ufo'
            # chemin_export_ufo = config.repertoire_sortie + '/ufo/' + chemin_source.split('/')[-1][:-4].split(-) + '.ufo'
            # export ufo
            police.generate(chemin_export_ufo)
            chemins_ufo_police.append(chemin_export_ufo)
        # on ajoute les chemins vers les ufo de la police à la liste globale
        chemins_ufo.append(chemins_ufo_police)
        # fermeture
        if fermer_police:
            police.close()
    config.fichiers_ufo = chemins_ufo
    config.sauvegarder()

# import de la configuration
config = Configuration(fichier_de_configuration)

# lancement du programme principal
go()

print('fin du programme')
