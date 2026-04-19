"""Module tracer_toulouse.py"""
import random
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt


def tracer_route_toulouse(fichier_graphml: str, route: list):
    """
    Trace une route sur le réseau piétonnier de Toulouse.

    Paramètres
    ----------
    fichier_graphml : str
        Chemin vers le fichier GraphML contenant le graphe OSMnx de Toulouse
        (ex. "toulouse_walk.graphml"). Si la chaîne est vide ou None, le graphe
        sera téléchargé depuis OpenStreetMap via ox.graph_from_place.
    route : list
        Liste ordonnée d'identifiants de nœuds (node IDs) représentant la
        trajectoire à tracer sur le graphe. Les identifiants doivent exister
        dans le graphe chargé.

    Comportement
    ----------
    - Charge (ou télécharge) le graphe piétonnier de Toulouse.
    - Si la route fournie contient des nœuds absents du graphe, lève une
        exception ValueError.
    - Affiche le graphe (matplotlib) et superpose la route en rouge.
    - Retourne le graphe utilisé (sous-graphe de la plus grande composante)
        et la route (liste de nœuds) pour usage ultérieur.
    """
    # 1) charger ou télécharger le graphe
    if fichier_graphml:
        graphe = ox.load_graphml(fichier_graphml)
    else:
        graphe = ox.graph_from_place("Toulouse, France", network_type="walk")

    # 2) réduire le graphe à la plus grande composante connexe (pour garantir qu'une route existe)
    if graphe.is_directed():
        composantes_connexes = nx.strongly_connected_components(graphe)
    else:
        composantes_connexes = nx.connected_components(graphe)
    composante_maximum = max(composantes_connexes, key=len) # plus grande composante connexe du graphe
    sous_graphe_connexe = graphe.subgraph(composante_maximum).copy()

    # 3) si route est vide alors choisir aléatoirement une O/D et calculer la route
    if not route:
        noeuds = list(sous_graphe_connexe.nodes)
        depart = random.choice(noeuds)
        arrivee = random.choice(noeuds)
        while arrivee == depart:
            arrivee = random.choice(noeuds)
        route = nx.shortest_path(sous_graphe_connexe, depart, arrivee, weight="length")

    # 4) vérifier que tous les nœuds de la route sont dans le graphe
    noeuds_absents = [n for n in route if n not in sous_graphe_connexe.nodes]
    if noeuds_absents:
        raise ValueError(f"Les nœuds suivants sont absents du graphe : {noeuds_absents}")

    # 5) tracer le graphe et superposer la route
    # paramètres par défaut pour les marqueurs
    marqueur_depart = {"marker": "o", "c": "green", "s": 100, "label": "Départ"}
    marqueur_arrivee = {"marker": "^", "c": "blue", "s": 100, "label": "Arrivée"}

    # utiliser ox.plot_graph pour le fond, puis dessiner la route en rouge.
    _, axes = ox.plot_graph(sous_graphe_connexe, show=False, close=False,
                                    node_size=0, edge_color="#999999", edge_linewidth=0.5)
    # utilitaire pour obtenir les géométries d'arêtes correspondant à la route
    try:
        route_arcs_gdfs = ox.routing.route_to_gdf(sous_graphe_connexe, route)
        route_arcs_gdfs.plot(ax=axes, linewidth=3, edgecolor="red")
    except Exception:
        # tracer la polyline des nœuds si route_to_gdfs non disponible
        coordonnees = [(sous_graphe_connexe.nodes[n]["y"],
                        sous_graphe_connexe.nodes[n]["x"]) for n in route]
        axes.plot([c[1] for c in coordonnees], [c[0] for c in coordonnees],
                    color="red", linewidth=3, transform=axes.transData)

    # obtenir les coordonnées lon/lat des extrémités (depart, arrivee)
    depart = route[0]
    arrivee = route[-1]
    depart_longitude = sous_graphe_connexe.nodes[depart]["x"]
    depart_latitude = sous_graphe_connexe.nodes[depart]["y"]
    arrive_longitude = sous_graphe_connexe.nodes[arrivee]["x"]
    arrive_latitude = sous_graphe_connexe.nodes[arrivee]["y"]

    # afficher les extrémités de la route sur la figure différemment 
    # (ex. vert pour départ, bleu pour arrivée)
    axes.scatter([depart_longitude], [depart_latitude], **marqueur_depart)
    axes.scatter([arrive_longitude], [arrive_latitude], **marqueur_arrivee)

    # afficher la figure et sa légende
    axes.legend()
    plt.show()
