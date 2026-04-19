"""Module contenant les fonctions simplifiants la lisibilité du programme."""

import os
import zipfile
from modules.classes import GrapheOrientePondere, Noeud, Arc

def afficher_dijkstra(depart : Noeud, arrive : Noeud, distance : float, chemin : list):
    """
    Affiche le résultat de l'algorithme selon le format exigé par l'énoncé.
    
    Formate la sortie pour afficher la distance totale et le chemin détaillé 
    sous la forme "A -> B -> C". Gère également le cas des 
    chemins inexistants.
    
    Args:
        depart (Noeud): Le sommet d'origine.
        arrive (Noeud): Le sommet de destination.
        distance (float): La distance totale calculé.
        chemin (list): La liste des étiquettes des sommets composant le chemin.
    """

    print(f'Distance({depart.etiquette}->{arrive.etiquette}) = {distance}')

    if chemin != []:
        print(f'Chemin : {depart.etiquette}', end='')

        for noeud in chemin[1:]:
            print(f' -> {noeud}',end='')

        print()

    else:
        print('Chemin inexistant.')

def est_float(valeur):
    """Vérifie si une chaîne peut être convertie en float."""
    try:
        float(valeur)
        return True
    except ValueError:
        return False

def charger_csv(chemin_fichier: str):
    """
    Charge un graphe orienté pondéré à partir d'un fichier CSV.
    
    Argument:
        chemin_fichier (str): Le chemin vers le fichier CSV.
        
    Returns:
        Graphe_oriente_pondere: L'instance du graphe construite à partir des données,
                                ou un graphe vide si une erreur survient.
    
    Raises:
        FileNotFoundError: Si le fichier spécifié est introuvable (géré en interne).
        ValueError: Si une ligne du CSV ne respecte pas le format numérique attendu.
    """
    arcs = []
    noeuds = set()

    try:
        # Ouverture du fichier
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            lignes = f.readlines()

        # Nettoyage des sauts de ligne et séparation des éléments
        # On ignore les lignes vides potentielles avec la condition if ligne.strip()
        arcs_bruts = [ligne.strip().split(',') for ligne in lignes if ligne.strip()]

        for arc in arcs_bruts:
            # Vérification d'éléments dans la ligne
            if len(arc) != 6 or not all(est_float(item) for item in [arc[1], arc[2], arc[4], arc[5]]):
                print(f"Erreur de format sur la ligne : {arc}")

            else:
                # Initialisation des noeuds et de l'arête
                noeud1 = Noeud(arc[0].upper(), (float(arc[1]), float(arc[2])))
                noeud2 = Noeud(arc[3].upper(), (float(arc[4]), float(arc[5])))
                arete = Arc(noeud1, noeud2)

                # Ajout aux données
                arcs.append(arete)
                noeuds.add(noeud1)
                noeuds.add(noeud2)

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{chemin_fichier}' est introuvable.")

    if arcs and list(noeuds):
        return GrapheOrientePondere(list(noeuds), arcs)
    else:
        return None

def choisir_chemin(carte:GrapheOrientePondere):
    """
    Fait selectionner les points de départ et d'arrivée en vérifiant que les sommets 
    existent dans le graphe et demande une confirmation avant de valider.
    
    Args:
        carte (Graphe_orienté_pondéré): Le graphe chargée.
        
    Returns:
        tuple: Le pt_depart (Noeud) et le pt_arrive (Noeud).
    """
    etiquettes = {noeud.etiquette : noeud for noeud in carte.noeuds}
    affichage_etiquettes = ' '.join(etiquettes.keys())
    print('Noeuds disponibles :', affichage_etiquettes)

    while True:
        pt_depart = input('Point de départ : ')
        while pt_depart.upper() not in etiquettes.keys():
            print('Saisie invalide choisir dans :', affichage_etiquettes)
            pt_depart = input('Point de départ : ')

        pt_arrive = input('Point d\'arrivé : ')
        while pt_arrive.upper() not in etiquettes.keys():
            print('Saisie invalide choisir dans :', affichage_etiquettes)
            pt_arrive = input('Point d\'arrivé : ')

        invite = f'Chemin le plus court entre {pt_depart} et {pt_arrive} ? (o|oui|true|0)'
        if input(invite).lower() in ('o', 'oui', 'true', '0'):
            break

    return etiquettes[pt_depart.upper()], etiquettes[pt_arrive.upper()]

def afficher_carte_terminal(graphe, largeur=80, hauteur=20):
    """
    Génère une représentation visuelle du graphe dans le terminal.
    
    Cette fonction projette les coordonnées réelles des noeuds sur une grille 
    de caractères pour simuler une carte.
    """
    # On récupère toutes les coordonnées pour définir les limites de la carte
    x = min(n.coordonees[0] for n in graphe.noeuds) ,max(n.coordonees[0] for n in graphe.noeuds)
    y = min(n.coordonees[1] for n in graphe.noeuds), max(n.coordonees[1] for n in graphe.noeuds)

    # Protection si tous les points sont sur la même ligne
    ecarts = (x[1] - x[0]) if x[1] != x[0] else 1 ,(y[1] - y[0]) if y[1] != y[0] else 1

    # On crée une grille vide (une liste de listes de caractères)
    grille = [[" " for _ in range(largeur + 1)] for _ in range(hauteur + 1)]

    # On place les noeuds sur la grille
    for noeud in graphe.noeuds:
        # Calcul de la position relative (produit en croix)
        x_relatif = int(((noeud.coordonees[0] - x[0]) / ecarts[0]) * largeur)
        # On inverse Y car dans un terminal, la ligne 0 est en haut
        y_relatif = hauteur - int(((noeud.coordonees[1] - y[0]) / ecarts[1]) * hauteur)

        # On place l'étiquette du noeud
        label = noeud.etiquette[:2]  # Limite à 2 caractères pour éviter les chevauchements
        for i, char in enumerate(label):
            if x_relatif + i <= largeur:
                grille[y_relatif][x_relatif + i] = char

    # Affichage de la carte avec une bordure
    print("\n" + "=" * (largeur + 5))
    print(" CARTE DU GRAPHE ".center(largeur + 5, "#"))
    print("=" * (largeur + 5))

    for ligne in grille:
        print("| " + "".join(ligne) + " |")

    print("=" * (largeur + 4) + "=\n")

def preparer_donnees(dossier="donnees", nom_archive="donnees.zip", fichier_temoin="toulouse.csv"):
    """
    Vérifie si les données lourdes sont décompressées. 
    Si ce n'est pas le cas, extrait silencieusement l'archive correspondante.
    """
    chemin_archive = os.path.join(nom_archive)
    chemin_temoin = os.path.join(dossier, fichier_temoin)

    # Si le fichier CSV manque mais que l'archive ZIP est présente, on lance l'extraction
    if not os.path.exists(chemin_temoin) and os.path.exists(chemin_archive):
        print(f"\n[Information] Première exécution : Extraction de l'archive {nom_archive}...")
        try:
            with zipfile.ZipFile(chemin_archive, 'r') as archive:
                # Extrait tout le contenu du ZIP directement dans le dossier "donnees"
                archive.extractall(dossier)
            print("[Information] Extraction terminée avec succès.\n")
        except zipfile.BadZipFile:
            print(f"\n[Erreur] L'archive {nom_archive} est corrompue ou illisible.")
