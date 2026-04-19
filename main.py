"""Point d'entrée principal du programme en ligne de commande."""

import argparse
import sys
from modules.fonctions import charger_csv, afficher_dijkstra, preparer_donnees

def main():
    """Analyse les arguments de la ligne de commande et exécute Dijkstra."""
    # Configuration de l'interface en ligne de commande
    parser = argparse.ArgumentParser(
        description="Calcul du plus court chemin dans un graphe orienté pondéré.")

    parser.add_argument('--fichier', type=str, required=True,
                        help="Chemin vers le fichier CSV contenant les arcs.")
    parser.add_argument('--source', type=str, required=True,
                        help="Étiquette du sommet de départ.")
    parser.add_argument('--cible', type=str, required=True,
                        help="Étiquette du sommet d'arrivée.")
    parser.add_argument('--graphml', type=str, default='',
                        help="Chemin fichier GraphML pour tracer la route sur la carte de Toulouse.")

    arguments = parser.parse_args()
    preparer_donnees()

    # Chargement du graphe
    carte = charger_csv(f'donnees/{arguments.fichier}')

    # Arrêt si le graphe est vide (fichier introuvable ou mal formaté)
    if carte is None:
        print('Le graphe est vide, veuillez fournir un fichier CSV valide.')
        sys.exit(1)

    # Création d'un dictionnaire pour indexer les objets Noeud par leur étiquette
    etiquettes = {noeud.etiquette: noeud for noeud in carte.noeuds}

    # Vérification de l'existence des sommets spécifiés en arguments
    if arguments.source not in etiquettes:
        print(f"Erreur : Le sommet source '{arguments.source}' n'existe pas dans le graphe.")
        sys.exit(1)

    if arguments.cible not in etiquettes:
        print(f"Erreur : Le sommet cible '{arguments.cible}' n'existe pas dans le graphe.")
        sys.exit(1)

    # Récupération des noeuds correspondants
    noeud_depart = etiquettes[arguments.source]
    noeud_arrive = etiquettes[arguments.cible]

    # Calcul et affichage (pas de risque de poids négatif car norme euclidéenne)
    chemin, distance = carte.plus_court_chemin(noeud_depart, noeud_arrive)
    afficher_dijkstra(noeud_depart, noeud_arrive, distance, chemin)

    if chemin and arguments.graphml != '':
        try:
            print('Chargement du tracé de la route sur la carte de Toulouse...')

            from tracer.tracer_toulouse import tracer_route_toulouse

            chemin = [int(noeud) if str(noeud).isdigit() else noeud for noeud in chemin]

            tracer_route_toulouse(f'donnees/{arguments.graphml}', chemin)
        except ImportError:
            print("Un des modules nécessaires pour tracer la route n'est pas installé. Veuillez",
                    "installer osmnx et networkx pour visualiser la route sur la carte de Toulouse")
        except Exception as e:
            print(f"Une erreur est survenue lors du tracé de la route : {e}")

if __name__ == "__main__":
    main()
