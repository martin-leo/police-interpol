'''
# Exportation JSON d'une police

La police est exportée sous la forme d'un fichier <fontname>.json ou data.json
'''

import fontforge
import json

# Paramètres

# option pour fermer chaque police en fin de traitement
# peut faire buguer fontForge
fermer_police = False

# fichier de configuration
fichier_de_configuration = '/chemin/du/fichier/de/configuration'

def exporter_police(police):
  '''Exporte un objet police au format JSON et retourne son chemin
  Police -> Chemin'''
  # nom par défaut
  filename = 'data.json'
  # mais si la police à un fontname on l'utilise
  if police.fontname:
    filename = str(police.fontname) + '.json'
  # on génère le chemin de sortie
  filepath = config.repertoire_sortie + "/json/originaux/" + filename
  # on génère le fichier JSON
  f = open(filepath,'w')
  f.write(police_vers_json(police))
  f.close()
  # on retourne le chemin du fichier créé
  return filepath

def lister_glyphes(police):
  '''Retourne la liste des glyphes présents dans une police
  Police -> Liste de glyphes'''
  liste_des_glyphes = []
  # pour chaque index de glyphe
  for glyphe_index in police:
    # on récupère le glyphe
    glyphe = police[glyphe_index]
    # s'il contient quelque chose
    if glyphe.activeLayer > 0:
      # on l'ajoute à la liste
      liste_des_glyphes.append(glyphe)
  # on retourne la liste
  return liste_des_glyphes

def lister_contours(glyphe):
  '''Retourne une liste de contours pour un glyphe donné.
  Glyphe -> Liste d'objets Contours'''
  # liste des contours
  liste_des_contours = []
  # si pas de layer actif
  if not glyphe.activeLayer:
    return
  # sinon on prend la référence
  layer = glyphe.layers[glyphe.activeLayer]
  # pour chaque contour dans le layer
  for contour in layer:
    # on ajoute à la liste
    liste_des_contours.append(contour)
  # que l'on retourne
  return liste_des_contours

def police_vers_json(police):
  '''Retourne une version JSON d'une police donné
  Police -> JSON'''
  # ouverture du JSON
  json = '{'
  # propriété familyname
  json += '"familyname":"' + str(police.familyname) + '",'
  # propriété fontname
  if police.fontname:
    json += '"fontname":"' + str(police.fontname) + '",'
  # propriété cidfullname
  if police.fullname:
    json += '"fullname":"' + str(police.fullname) + '",'
  # propriété glyphs (liste)
  json += '"glyphs":['
  # on peuple avec les glyphes en json
  for glyphe in lister_glyphes(police):
    json += glyphe_vers_json(glyphe) + ","
  # on enlève la dernière virgule inutile !
  json = json[:-1]
  # on ferme la liste
  json += ']'
  # et le JSON
  json += '}'
  # que l'on retourne
  return json

def glyphe_vers_json(glyphe):
  '''Retourne une version JSON d'un glyphe donné
  Glyphe -> JSON'''
  # ouverture du JSON
  json = '{'
  # propriété glyphname
  if glyphe.glyphname:
    json += '"glyphname":"' + glyphe.glyphname + '",'
  # propriété contours (liste)
  json += '"contours":['
  # on peuple avec les contours en json
  contours = lister_contours(glyphe)
  if len(contours) > 0:
    for contour in contours:
      json += contour_vers_json(contour) + ","
    # on enlève la dernière virgule inutile !
    json = json[:-1]
  # on ferme la liste
  json += ']'
  # et le JSON
  json += '}'
  # que l'on retourne
  return json

def contour_vers_json(contour):
  '''Retourne une version JSON d'un contour donné
  Contour -> JSON'''
  # ouverture du JSON
  json = '{'
  # propriété points (liste)
  json += '"points":['
  for point in contour:
    json += point_vers_json(point) + ","
  # on enlève la dernière virgule inutile !
  json = json[:-1]
  # on clôt la liste
  json += ']'
  # et le JSON
  json += '}'
  # que l'on retourne
  return json

def point_vers_json(point):
  '''Retourne une version JSON d'un point donné
  Contour -> JSON'''
  # ouverture du JSON
  json = '{'
  # propriété x
  json += '"x":"' + str(point.x) + '",'
  # propriété y
  json += '"y":"' + str(point.y) + '",'
  # propriété on_curve
  json += '"on_curve":' + str(point.on_curve)
  # on ferme le JSON
  json += '}'
  # que l'on retourne
  return json

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
    '''Procède à l'exportation des polices.
    Void -> Void'''
    # pour chaque chemin spécifié
    for chemin_police in config.fichiers_sources:
        # on imprime le chemin
        print('export : ' + chemin_police)
        # on ouvre la police
        police = fontforge.open(chemin_police)
        # on l'exporte en JSON
        config.fichiers_json_pour_interpolation.append( exporter_police(police) )
        # si option pour fermer la typo après usage
        if fermer_police:
            police.close()
    # on sauvegarde le fichier de configuration
    config.sauvegarder()
    # on signale la fin des opérations
    print('export terminé.\n')

# import de la configuration
config = Configuration(fichier_de_configuration)

# lancement du programme principal
go()
