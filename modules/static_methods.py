'''Ce module contient des méthodes statiques pour afficher la progression du traitement.'''

import time

def afficher_progression(_, temps_debut, temps_precedent,
                            __, pourcentage_actuel):
    """Affiche la progression du traitement avec le pourcentage et le temps écoulé."""

    temps_ecoule = time.time() - temps_debut
    ecart_temps = time.time() - temps_precedent
    # Sécurité contre la division par zéro lors de la première milliseconde
    vitesse = (60 / ecart_temps) if ecart_temps > 0 else 0.0

    print(f"\rProgression dans le graphe : {pourcentage_actuel}% | "
        f"Temps écoulé : {temps_ecoule:.2f} s | "
        f"Vitesse : {vitesse :.2f} %/min", end="", flush=True)
    return pourcentage_actuel, time.time()


def reconstitution_chemin(predecesseur, etiquette_depart, etiquette_arrive):
    """Reconstitue le chemin le plus court à partir du dictionnaire des prédecesseurs."""
    chemin = []

    # L'algorithme est-il arrivé au bout ?
    if predecesseur[etiquette_arrive] is not None:

        # On part de l'arrivée
        noeud = etiquette_arrive
        chemin.append(etiquette_arrive)

        # On ajoute les prédecesseurs jusqu'au départ
        while noeud != etiquette_depart:
            chemin.append(predecesseur[noeud])
            noeud = predecesseur[noeud]

    # On retourne la liste pour avoir le bon ordre (Début -> Fin)
    chemin.reverse()

    return chemin
