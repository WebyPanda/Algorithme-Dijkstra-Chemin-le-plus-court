"""Module contenant les classes utilisées par le programme."""

import time
import heapq
from math import sqrt
from modules.static_methods import afficher_progression, reconstitution_chemin

class Noeud:
    """Représente un nœud identifié par un label."""

    def __init__(self, etiquette, coordonees:tuple):
        self.etiquette = etiquette
        self.coordonees = coordonees

    def __repr__(self):
        return f"Noeud({self.etiquette})"

    def __str__(self):
        return str(self.etiquette)

    def __eq__(self, autre):
        return isinstance(autre, Noeud) and self.coordonees == autre.coordonees

    def __hash__(self):
        return hash(self.etiquette)


class Arc:
    """Représente un arc orientée entre deux nœuds."""

    def __init__(self, noeud1: Noeud, noeud2: Noeud):
        self.noeud1 = noeud1
        self.noeud2 = noeud2

    def __repr__(self):
        return f"Arc({self.noeud1}, {self.noeud2})"

    def __hash__(self):
        return hash((self.noeud1, self.noeud2))

    def __eq__(self, autre):
        egalite_noeuds = autre.noeud1 == self.noeud1 and autre.noeud2 == self.noeud2
        return isinstance(autre, Arc) and egalite_noeuds

    def noeuds(self):
        """Retourne les deux nœuds sous forme d'ensemble."""
        return [self.noeud1, self.noeud2]


class GrapheOrientePondere:
    """Classe correspondant à un graphe ici utilisé comme une carte"""

    @staticmethod
    def trouver_poid_arc(arc:Arc):
        """
        Calcule la distance euclidienne entre les deux nœuds d'une arc.
        
        Argument:
            arc (Arc): L'objet arc contenant les nœuds source et destination.
            
        Retour:
            distance (float): La distance (poids) entre les deux sommets.
        """
        #Crée la liste des coordonées des noeuds d'un arc : [(x1,y1),(x2,y2)]
        coordonees = [noeud.coordonees for noeud in arc.noeuds()]

        #Distance = racine ( (x1-x2)**2 + (y1-y2)**2 )
        distance = sqrt( (coordonees[0][0]-coordonees[1][0])**2
                        + (coordonees[0][1]-coordonees[1][1])**2 )

        return distance

    def __init__(self, noeuds:list, arcs:list):
        """
        Initialise un graphe pré-rempli avec une liste
        de noeuds et d'arcs. Les poids des arcs sont calculés automatiquement
        à l'initialisation.
        
        Arguments:
            noeuds (list): Liste des Noeuds du graphe.
            arcs (list): Liste des Aretes reliant les nœuds.
        """
        self.noeuds = noeuds
        #Dictionnaire rassemblant un arc et sa pondération
        self.arcs = {}
        #Dictionnaire d'adjacence pour faciliter la recherche des voisins
        self.adjacence = {noeud.etiquette: [] for noeud in self.noeuds}
        for arc in arcs:
            poids = self.trouver_poid_arc(arc)
            self.arcs[arc] = poids
            self.adjacence[arc.noeud1.etiquette].append((arc.noeud2.etiquette, poids))


    def plus_court_chemin(self, noeud_depart, noeud_arrive):
        """
        Calcule le plus court chemin entre un noeud de départ et un noeud d'arrivée.
        
        Implémente l'algorithme de Dijkstra pour les graphes pondérés à poids positifs.
        Le chemin est reconstruit à rebours à partir du dictionnaire des prédécesseurs.
        
        Args:
            noeud_depart (Noeud): Le sommet d'origine.
            noeud_arrive (Noeud): Le sommet de destination.
            
        Returns:
            list: La liste ordonnée des étiquettes de sommets 
                formant le chemin le plus court, ou [] si chemin inexistant.
            float: La valeur de la distance la plus courte entre le noeud de départ 
                et celui d'arrivée ou +inf si chemin inexistant.
        """
        if noeud_depart == noeud_arrive:
            return [noeud_depart.etiquette], 0.0

        #====================================================================
        #           Initialisation
        #====================================================================
        distances = {noeud.etiquette: float('inf') for noeud in self.noeuds}
        #Initialisation du sommet de depart a 0
        distances[noeud_depart.etiquette] = 0.0

        predecesseur = {noeud.etiquette: None for noeud in self.noeuds}

        file = []
        heapq.heappush(file, (0.0, noeud_depart.etiquette))

        noeuds_visites = set()

        print('Début Dijkstra :')
        #Total : [nombre de noeuds, temps de début, temps du dernier affichage,
        #           pourcentage_précédent, pourcentage_actuel]
        total = [len(self.noeuds), time.time(), time.time(), 0, 0]

        #====================================================================
        #           Corps
        #====================================================================
        # Tant que R != ∅ faire
        while file:
            # Affichage de la progression
            # Calcul du pourcentage d'avancement entier
            total[4] = int((len(noeuds_visites) / total[0]) * 100)

            # Rafraîchissement de l'affichage
            if total[4] > total[3]+5:  # Affiche tous les 5% d'avancement
                total[3], total[2] = afficher_progression(*total)

            # Choisir i tel que i = argmin C(j)
            # Déballage direct du tuple extrait par heapq (plus rapide que list())
            distance_actuelle, etiquette_actuelle = heapq.heappop(file)

            # Si le noeud a déjà été traité définitivement, on l'ignore
            if etiquette_actuelle in noeuds_visites:
                continue

            # Ajouter vi à S (noeuds terminés)
            noeuds_visites.add(etiquette_actuelle)

            # Arrêt anticipé : la cible a été trouvée de manière optimale
            if etiquette_actuelle == noeud_arrive.etiquette:
                break

            # Mise à jour de C
            # Pour tous les sommets vj voisins de vi faire
            for etiquette_adjacente, poids in self.adjacence[etiquette_actuelle]:

                # Sécurité pour rendre Dijkstra robuste
                if poids < 0:
                    raise ValueError(f"!! {etiquette_actuelle}->{etiquette_adjacente} poids < 0")

                # C(j) = min(C(j), C(i) + cij)
                nouvelle_distance = distance_actuelle + poids

                if nouvelle_distance < distances[etiquette_adjacente]:
                    distances[etiquette_adjacente] = nouvelle_distance
                    predecesseur[etiquette_adjacente] = etiquette_actuelle

                    # Mise à jour de la file de priorité
                    heapq.heappush(file, (nouvelle_distance, etiquette_adjacente))

        #====================================================================
        #            Reconstitution
        #====================================================================
        print(f"\nDijkstra finit en {time.time() - total[1]:.2f} secondes.")

        chemin = reconstitution_chemin(predecesseur, noeud_depart.etiquette, noeud_arrive.etiquette)

        return chemin, distances[noeud_arrive.etiquette]
