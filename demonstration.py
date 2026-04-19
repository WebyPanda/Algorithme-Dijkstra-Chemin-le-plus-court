"""Module principal de l'algorithme de Dijkstra"""

from modules.fonctions import afficher_carte_terminal, charger_csv
from modules.fonctions import choisir_chemin, afficher_dijkstra, preparer_donnees

def scenario(csv:str, graphml:str=''):
    """
    Affiche le résultat de l'algorithme de Dijkstra pour une liste d'arcs donné.
    
    Args:
        csv (str): Le chemin vers le fichier de données CSV.
        graphml (str): Le chemin vers le fichier GraphML.
    """

    preparer_donnees()

    carte = charger_csv(f'donnees/{csv}')
    if carte is None:
        print("La carte est vide. Veuillez fournir un fichier CSV valide.")
        return

    if len(carte.noeuds) < 10:
        afficher_carte_terminal(carte)

    pt_depart, pt_arrive = choisir_chemin(carte)

    chemin_plus_court, distance = carte.plus_court_chemin(pt_depart, pt_arrive)

    afficher_dijkstra(pt_depart, pt_arrive, distance, chemin_plus_court)

    if chemin_plus_court and graphml != '':
        try:
            print('Chargement du tracé de la route sur la carte de Toulouse...')

            from tracer.tracer_toulouse import tracer_route_toulouse

            chemin = [int(noeud) if str(noeud).isdigit() else noeud for noeud in chemin_plus_court]

            tracer_route_toulouse(f'donnees/{graphml}', chemin)
        except ImportError:
            print("Un des modules nécessaires pour tracer la route n'est pas installé. Veuillez",
                    "installer osmnx et networkx pour visualiser la route sur la carte de Toulouse")
        except Exception as e:
            print(f"Une erreur est survenue lors du tracé de la route : {e}")


if __name__ == "__main__":
    NOM_CSV = input("Nom du fichier CSV dans /donnees (ex: 'toulouse.csv') : ")
    NOM_GRAPHML = input("Fichier graphml dans /donnees (ex: 'toulouse.graphml')"+
                        "(laisser vide pour ne pas tracer) : ")
    scenario(NOM_CSV, NOM_GRAPHML)
