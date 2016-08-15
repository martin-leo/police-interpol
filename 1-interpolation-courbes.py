'''
# Interpolation d'une police au format JSON

La police est importée dans Blender et interpolée grâce à la librairie mathutils, puis réexportée.
'''

import json
import mathutils

# paramétrage

# fichier de configuration
fichier_de_configuration = '/chemin/du/fichier/de/configuration'

class Police:
  '''Classe permettant le représentatation simple
  d'un objet Font calqué sur FontForge'''
  def __init__(self, chemin_fichier_json, resolution):
    '''Constructeur, permet l'import des données
    depuis un fichier JSON.
    String -> Void'''
    try:
      # chargement des données
      file_path = chemin_fichier_json
      json_data = open(file_path).read()
      data = json.loads(json_data)
      # données général
      self.familyname = data['familyname']
      self.fontname = data['fontname']
      self.fullname = data['fullname']
      self.glyphs = []
      self.resolution = resolution
      # pour chaque glyphe dans le JSON
      for donnees_glyphe in data['glyphs']:
        # on créé un objet Glyph
        glyphe = Glyph()
        # où l'on charge mes données
        glyphe.charger(donnees_glyphe)
        # et l'on l'ajoute aux glyphes de l'objet Police
        self.glyphs.append(glyphe)
    # En cas d'erreur :
    except Exception as e:
      print(e)

  def traiter(self):
    '''Procède à l'interpolation des glyphes
    [Int] -> Void'''
    for glyphe in self.glyphs:
      glyphe.traiter(self.resolution)

  def exporter_liste_glyphes(self):
    '''Retourne la liste des glyphes interpolés
    sous forme de JSON
    Void -> String'''
    # début de la liste au format JSON
    json = '['
    # pour chaque glyphe de la police
    for glyphe in self.glyphs:
      # on ajoute au JSON la version interpolée
      json += str(glyphe.export()) + ','
    # on enlève la dernière virgule inutile
    json = json[:-1]
    # on ferme
    json += ']'
    # on retourne le JSON
    return json

  def exporter(self, chemin_du_fichier):
    '''Procède à l'export de la police interpolée
    dans un fichier JSON à l'emplacement donné.
    String -> Void'''
    # on créé le JSON
    export_json = "{\"familyname\":\"%s\",\"fontname\":\"%s\",\"fullname\":\"%s\",\"resolution\":%d,\"glyphs\":%s}" % (self.familyname, self.fontname, self.fullname, self.resolution, self.exporter_liste_glyphes())
    # on ouvre le fichier
    f = open(chemin_du_fichier,'w')
    # on écrit le JSON
    f.write(export_json)
    # on ferme
    f.close()

class Glyph:
  '''Classe permettant le représentatation simple
  d'un objet Glyphe calqué sur FontForge'''
  def __init__(self,glyphname = '',contours = []):
    '''Constructeur
    [String[,Contour List]] -> Void'''
    # Nom du glyphe
    self.glyphname = glyphname
    # liste des contours
    self.contours = contours

  def charger(self,data):
    '''charge des données exportées depuis FontForge au format JSON
    String -> Void'''
    # opt. conversion du string JSON vers un objet
    # data = json.loads(data)
    # récupération du nom du glyphe
    self.glyphname = data['glyphname']
    # mise à zéro de la liste des contours
    self.contours = []
    # itérations sur les données de contour en entrée
    for donnees_contour in data['contours']:
      # pour chaque contour en entrée :
      # création d'un objet contour
      '''
      self.charger_contour(donnees_contour)
      '''
      contour = None
      contour = Contour()
      # Mystère : sauf pour le premier évidemment
      # le Contour nouvellement créé a la propriété
      # points déjà peuplée des points du contour précédent ??? WTF ???
      contour.points = []
      # chargement des données
      contour.charger(donnees_contour)
      # ajout à la liste des contours
      self.contours.append(contour)

  def traiter(self,resolution):
    '''traite les données chargées
    Int -> Void'''
    # on ajoute deux pour tenir compte
    # des deux points d'origine
    # résolution = points ajoutés
    resolution = resolution + 2
    # on peuple self.copie avec un glyphe vide
    self.copie = Glyph(self.glyphname)
    # Mystère : sauf pour le premier évidemment
    # la copie de Contour nouvellement créé a la propriété
    # points déjà peuplée des points du contour précédent ??? WTF ???
    self.copie.contours = []
    # pour chaque contour en copie la version interpolée
    for contour in self.contours:
      self.copie.contours.append(contour.traiter(resolution))

  def export(self):
    '''Retourne la version interpolée
    Void -> Glyph'''
    try:
      return self.copie
    except Exception as e:
      print(e)
      return self.glyphname

  def __str__(self):
    '''Imprime une version lisible de l'objet
    Void -> String'''
    return "{\"glyphname\":\"%s\",\"contours\":%s}" % (self.glyphname, str(self.contours))


class Contour:
  '''Classe permettant le représentation simple
  d'un objet Contour calqué sur FontForge'''
  def __init__(self, points = []):
    '''Constructeur.
    [Point List] -> Void'''
    self.points = points

  def charger(self, data):
    '''Charge des données sous forme d'objet
    dans self.points sous forme d'une liste d'objets Points
    Objet -> Void'''
    # Pour chaque point de la liste en entrée
    for point in data['points']:
      # on créé un nouveau point
      p = Point()
      # On charge les données en entrée
      p.charger(point)
      # On l'ajoute à la liste des points de l'objet Contour
      self.points.append(p)

  def next_point(self, index, decalage = 1):
    '''Retourne index + décalage
    En reprenant au début de la liste un fois arrivé au bout.
    Int, Int -> Int'''
    # si on est PAS au dernier point
    if index + decalage < (len(self.points)):
      return index + decalage
    else:
      return (index + decalage) - len(self.points)

  def traiter(self, resolution):
    '''Retourne un nouveau Contour avec les nouveaux points
    générés par interpolation.
    Int -> Contour'''
    # nouvel objet contour à retourner
    nouveau_contour = Contour()
    # liste des points du nouveau contour
    nouveau_contour.points = []
    # pour chacun point
    for i in range(0,len(self.points)):
      # on créé une référence de travail au point
      point = self.points[i]
      # si le point de travail n'est pas un point de controle
      # on s'intéresse à ce qui le suit
      if not point.is_control_point():
        # on l'ajoute à nos nouveaux points
        nouveau_contour.points.append(point)
        # on créé une référence de travail au point suivant
        prochain_point = self.points[self.next_point(i)]
        # si celui-ci n'est pas un point de contrôle
        # on est sur une droite, pas d'action nécéssaire
        if not prochain_point.is_control_point():
          pass
        # si le point est au contraire un point de contrôle
        # cela signifie que l'on est sur une courbe
        # qu'il faut donc interpoler
        else:
          # on va travailler avec différents points
          # point a
          a = point.to_vector()
          # point de controle pca
          pca = prochain_point.to_vector()
          # point de controle pcb
          pcb = self.points[self.next_point(i,2)].to_vector()
          # point b
          b = self.points[self.next_point(i,3)].to_vector()
          # on procède à l'interpolation qui retourne une liste d'objets Vector
          # dont on ne garde pas les premier et dernier points
          vectors = mathutils.geometry.interpolate_bezier(a,pca,pcb,b,resolution)[1:-1]
          # pour chaque
          for vector in vectors:
            # on créé un nouvel objet Point paramétré
            point = Point(vector.x, vector.y, 1)
            # on l'ajoute à la liste des nouveaux points
            nouveau_contour.points.append(point)
      # si c'est un point de contrôle on passe
      else:
        pass
    # on retourne le nouveau contour
    return nouveau_contour

  def __str__(self):
    '''Imprime une version lisible de l'objet
    Void -> String'''
    return "{\"points\":%s}" % (str(self.points))

  def __repr__(self):
    '''Imprime une version lisible de l'objet
    Void -> String'''
    return "{\"points\":%s}" % (str(self.points))

class Point:
  '''Classe permettant le représentatation simple
  d'un objet Point calqué sur FontForge
  [Int[,Int[,Boolean]]] -> Void'''
  def __init__(self, x = None, y = None, on_curve = None):
    '''Constructeur'''
    self.x = x
    self.y = y
    self.on_curve = on_curve

  def charger(self,data):
    '''charge des données dans l'objet Point
    Object -> Void'''
    self.x = data['x'];
    self.y = data['y'];
    self.on_curve = data['on_curve']

  def is_control_point(self):
    '''Renvoie un booléen selon la nature du point
    (Point de contrôle ou non)
    Void -> Booléen'''
    return self.on_curve != 1

  def to_vector(self):
    '''Renvoie le point sous forme d'objet Vector'''
    return mathutils.Vector((float(self.x),float(self.y),0))

  def __str__(self):
    '''Retourne l'objet sous forme de chaîne de caractère
    Void -> String'''
    return "{\"x\":\"%s\",\"y\":\"%s\",\"on_curve\":%s}" % (self.x, self.y, self.on_curve)

  def __repr__(self):
    '''Retourne l'objet sous forme de chaîne de caractère
    Void -> String'''
    return "{\"x\":\"%s\",\"y\":\"%s\",\"on_curve\":%s}" % (self.x, self.y, self.on_curve)

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
    '''Programme principal
    Void -> Void'''
    # on traite police après police
    for chemin_json in config.fichiers_json_pour_interpolation:
        print('traitement de ' + chemin_json)
        # on va garder une trace pour chaque résolution
        # de tous les fichiers générés
        # pour enregistrement dans le fichier de configuration
        polices_exportees = []
        # pour chaque résolution
        for resolution in config.resolutions:
            print('→ résolution ' + str(resolution))
            # on génère le chemin de fichier en sortie
            chemin_json_sortie = config.repertoire_sortie + '/json/interpoles/' + chemin_json.split('/')[-1][:-5] + '.interpol.' + str(resolution) + '.json'
            # on charge la police
            police = Police(chemin_json, resolution)
            # on interpole
            police.traiter()
            # on exporte
            police.exporter(chemin_json_sortie)
            # on ajoute à la liste des polices exportées
            polices_exportees.append(chemin_json_sortie)
        # on ajoute la liste des json avec interpolation à la conf
        config.fichiers_json_interpoles.append(polices_exportees)
        print('fin du traitement')
    # on sauvegarde la configuration
    config.sauvegarder()

# import de la configuration
config = Configuration(fichier_de_configuration)

# lancement du programme principal
go()

# signal de fin de programme
print('fin du programme')
