Titre
-----
Projet : tracé de routes sur le réseau piétonnier de Toulouse (OSMnx)

Prérequis
--------
- Python 3.9 ou 3.10 recommandé.
- pip installé.
- (Optionnel) Conda si vous préférez gérer l'environnement avec conda.

Installation (avec requirements.txt)
------------------------------------
1) Cloner ou placer le projet dans un dossier local.

2) Créer et activer un environnement virtuel (recommandé)
- Sous Linux / macOS:
  python -m venv venv
  source venv/bin/activate
- Sous Windows (PowerShell):
  python -m venv venv
  .\venv\Scripts\Activate.ps1

3) Mettre pip à jour
  pip install --upgrade pip

4) Installer les dépendances depuis requirements.txt
  pip install -r requirements.txt

Remarques importantes
--------------------
- Pour les bibliothèques géospatiales (geopandas, rtree, shapely, pyproj) l'installation via pip fonctionne généralement, mais sur certaines plateformes il peut être plus fiable d'utiliser conda (conda-forge).
- Exemple conda (si pip échoue) :
  conda create -n monenv -c conda-forge python=3.10 osmnx networkx matplotlib geopandas rtree
  conda activate monenv

Fichiers utiles
---------------
- tracer_toulouse.py  : contient la fonction tracer_route_toulouse(...)
- exemple_route.py        : exemple d'appel de la fonction
- requirements.txt    : liste des dépendances à installer
- toulouse.graphml : (optionnel) fichier GraphML pré-téléchargé du graphe dans le dossier "donnees"

Exécution
---------
1) Assurez-vous que l'environnement est activé et que les dépendances sont installées.
2) Lancer le script d'exemple :
  python exemple_route.py
3) Le script chargera (ou téléchargera) le graphe et affichera la carte avec la route.

Dépannage rapide
----------------
- Erreur d'installation liée à GEOS/PROJ/OGR: essayez conda avec conda-forge.
- Si le tracé n'apparaît pas correctement, vérifiez la version d'OSMnx et adaptez les appels de plotting (certaines fonctions ont changé entre versions).

