"""Module de tests unitaires pour le projet de graphes orientés pondérés."""

import time
import pytest
import subprocess

from modules.classes import Noeud, Arc, GrapheOrientePondere
from modules.fonctions import afficher_dijkstra, charger_csv, choisir_chemin, afficher_carte_terminal
from modules.static_methods import afficher_progression, reconstitution_chemin
from main import main
from demonstration import scenario

class TestNoeud:
    """Tests unitaires pour la classe Noeud."""
    n1 = Noeud('A', (1.0, 2.0))
    n2 = Noeud('A', (1.0, 2.0))
    n3 = Noeud('B', (3.0, 4.0))

    def test_init_et_representation(self):
        """Vérifie l'initialisation et les méthodes de représentation."""
        assert self.n1.etiquette == 'A'
        assert self.n1.coordonees == (1.0, 2.0)
        assert repr(self.n1) == "Noeud(A)"
        assert str(self.n1) == "A"

    def test_egalite_et_hachage(self):
        """Vérifie l'égalité et le hachage des nœuds."""
        assert self.n1 == self.n2
        assert self.n1 != self.n3
        assert hash(self.n1) == hash(self.n2)

class TestArc:
    """Tests unitaires pour la classe Arc."""
    n1 = Noeud('A', (0.0, 0.0))
    n2 = Noeud('B', (3.0, 4.0))
    arc1 = Arc(n1, n2)
    arc2 = Arc(n1, n2)

    def test_init_et_methodes(self):
        """Vérifie l'initialisation et les méthodes de l'arc."""
        assert repr(self.arc1) == f"Arc({self.n1}, {self.n2})"
        assert self.arc1.noeuds() == [self.n1, self.n2]
        assert self.arc1 == self.arc2
        assert hash(self.arc1) == hash(self.arc2)

class TestGrapheOrientePondere:
    """Tests unitaires pour les objets Noeud, Arc et la logique du Graphe."""

    # Données de test réutilisables
    na = Noeud('A', (0.0, 0.0))
    nb = Noeud('B', (0.0, 3.0))
    nc = Noeud('C', (4.0, 0.0))
    nd = Noeud('D', (10.0, 10.0)) # Noeud inatteignable

    arc_ab = Arc(na, nb) # Distance: 3.0
    arc_ac = Arc(na, nc) # Distance: 4.0
    arc_bc = Arc(nb, nc) # Distance: 5.0

    graphe = GrapheOrientePondere(
        [na, nb, nc, nd],
        [arc_ab, arc_ac, arc_bc]
    )

    def test_noeud_et_arc(self):
        """Vérifie l'initialisation, l'égalité et le hachage des entités de base."""
        # Test Noeud
        n_copie = Noeud('A', (0.0, 0.0))
        assert self.na.etiquette == 'A'
        assert self.na == n_copie
        assert hash(self.na) == hash(n_copie)
        assert str(self.na) == "A"

        # Test Arc
        arc_copie = Arc(self.na, self.nb)
        assert self.arc_ab == arc_copie
        assert hash(self.arc_ab) == hash(arc_copie)
        assert self.arc_ab.noeuds() == [self.na, self.nb]

    def test_initialisation_graphe(self):
        """Vérifie le calcul automatique des poids et la création de l'adjacence."""
        assert self.graphe.arcs[self.arc_ab] == 3.0
        assert self.graphe.arcs[self.arc_ac] == 4.0
        # Vérification du dictionnaire d'adjacence
        assert ('B', 3.0) in self.graphe.adjacence['A']
        assert ('C', 4.0) in self.graphe.adjacence['A']

    def test_erreur_poids_negatif(self):
        """Vérifie que Dijkstra lève une ValueError en présence de poids négatifs."""
        carte = GrapheOrientePondere([self.na, self.nb], [self.arc_ab])
        # Injection manuelle d'un poids négatif dans la liste d'adjacence
        carte.adjacence['A'] = [('B', -5.0)]

        with pytest.raises(ValueError, match="poids < 0"):
            carte.plus_court_chemin(self.na, self.nb)

    def test_plus_court_chemin_nominal(self):
        """Vérifie le calcul exact du chemin et de la distance optimale."""
        chemin, distance = self.graphe.plus_court_chemin(self.na, self.nc)
        assert chemin == ['A', 'C']
        assert distance == 4.0

    def test_plus_court_chemin_inatteignable(self):
        """Vérifie la gestion d'un sommet cible déconnecté du graphe."""
        chemin, distance = self.graphe.plus_court_chemin(self.na, self.nd)
        assert not chemin
        assert distance == float('inf')

    def test_plus_court_chemin_meme_noeud(self):
        """Vérifie le comportement si le départ et l'arrivée sont identiques."""
        chemin, distance = self.graphe.plus_court_chemin(self.na, self.na)
        assert chemin == ['A']
        assert distance == 0.0

class TestStaticMethods:
    """Tests unitaires pour les outils de calcul et d'affichage isolés."""

    def test_reconstitution_logique(self):
        """Vérifie que la remontée des parents fonctionne sans erreur de type."""
        # Dictionnaire de test : A -> C -> B
        preds = {'A': None, 'C': 'A', 'B': 'C'}
        chemin = reconstitution_chemin(preds, 'A', 'B')
        assert chemin == ['A', 'C', 'B']

    def test_reconstitution_chemin(self):
        """Vérifie la capacité à remonter le dictionnaire des prédécesseurs."""
        predecesseurs = {'A': None, 'B': 'C', 'C': 'A', 'D': 'B'}

        # Cas nominal
        chemin = reconstitution_chemin(predecesseurs, 'A', 'D')
        assert chemin == ['A', 'C', 'B', 'D']

        # Cas chemin inatteignable (pas de prédécesseur pour l'arrivée)
        predecesseurs_vide = {'A': None, 'B': None}
        chemin_vide = reconstitution_chemin(predecesseurs_vide, 'A', 'B')
        assert not chemin_vide

    def test_afficher_progression(self, capsys):
        """Vérifie le formatage de la ligne de progression dynamique."""
        temps_debut = time.time() - 2.0
        temps_precedent = time.time() - 0.5

        pourcentage, _ = afficher_progression(None, temps_debut, temps_precedent, None, 50)
        sortie = capsys.readouterr().out

        assert pourcentage == 50
        assert "Progression dans le graphe : 50%" in sortie
        assert "Temps écoulé : 2.0" in sortie
        assert "Vitesse :" in sortie

class TestFonctions:
    """Tests unitaires pour les fonctions d'entrée/sortie, de parsing et d'affichage."""

    def test_charger_csv_valide(self, tmp_path):
        """Vérifie que la construction du graphe réussit avec un CSV conforme."""
        fichier_valide = tmp_path / "valide.csv"
        # Utilisation de nombres entiers pour passer le test isdigit() du code source
        fichier_valide.write_text("A,1,3,B,4,5\nC,2,9,B,4,5\n", encoding="utf-8")

        graphe = charger_csv(str(fichier_valide))
        assert graphe is not None
        assert len(graphe.noeuds) == 3
        assert len(graphe.arcs) == 2

    def test_charger_csv_invalide(self, tmp_path, capsys):
        """Vérifie le signalement des erreurs de format (ex: données manquantes)."""
        fichier_invalide = tmp_path / "invalide.csv"
        fichier_invalide.write_text("A,1.2,B,4.1,5.9\nX,erreur,0,Y,1,1\n", encoding="utf-8")

        charger_csv(str(fichier_invalide))
        sortie = capsys.readouterr().out
        assert "Erreur de format sur la ligne" in sortie


    def test_charger_csv_introuvable(self, capsys):
        """Vérifie la robustesse face à un fichier inexistant."""
        resultat = charger_csv("fichier_fantome.csv")
        sortie = capsys.readouterr().out
        assert resultat is None
        assert "est introuvable" in sortie

    def test_afficher_dijkstra(self, capsys):
        """Vérifie le formatage de la sortie console pour le chemin."""
        n1, n2 = Noeud('A', (0, 0)), Noeud('B', (1, 1))

        # Test chemin existant
        afficher_dijkstra(n1, n2, 5.5, ['A', 'C', 'B'])
        sortie = capsys.readouterr().out
        assert "Distance(A->B) = 5.5" in sortie
        assert "Chemin : A -> C -> B" in sortie

        # Test chemin inexistant
        afficher_dijkstra(n1, n2, float('inf'), [])
        sortie_vide = capsys.readouterr().out
        assert "Chemin inexistant" in sortie_vide

    def test_choisir_chemin(self, monkeypatch):
        """Vérifie la boucle de validation de la saisie utilisateur.
        C'est le seul endroit où la fixture native monkeypatch est utilisée 
        pour simuler un utilisateur qui tape sur son clavier."""
        graphe = GrapheOrientePondere([Noeud('A', (0, 0)), Noeud('B', (1, 1))], [])
        entrees_simulees = iter(['X', 'A', 'Y', 'B', 'oui'])
        monkeypatch.setattr('builtins.input', lambda _: next(entrees_simulees))

        depart, arrivee = choisir_chemin(graphe)
        assert depart.etiquette == 'A'
        assert arrivee.etiquette == 'B'

    def test_afficher_carte_terminal(self, capsys):
        """Vérifie que la génération de la grille ASCII 
        fonctionne avec le fichier test_ouvrir.csv."""
        # On charge le fichier CSV que vous avez défini à la racine
        graphe = charger_csv("donnees/test_ouvrir.csv")

        afficher_carte_terminal(graphe)
        sortie = capsys.readouterr().out

        # Vérification de l'interface visuelle textuelle
        assert "CARTE DU GRAPHE" in sortie
        assert "===" in sortie
        assert "|" in sortie 

class TestDemonstration:
    """Tests unitaires pour le fichier de démonstration interactif."""

    def test_scenario_nominal(self, monkeypatch, capsys):
        """Vérifie le fonctionnement normal avec le vrai fichier test_ouvrir.csv."""
        # L'unique monkeypatch indispensable pour éviter que le test ne fige en 
        # attendant qu'un humain tape sur le clavier.
        entrees = iter(['A', 'D', 'oui'])
        monkeypatch.setattr('builtins.input', lambda _: next(entrees))

        # On utilise directement votre fichier de données réel
        scenario("test_ouvrir.csv")
        sortie = capsys.readouterr().out

        # Vérifie que l'algorithme de Dijkstra s'est bien exécuté jusqu'au bout
        assert "Distance(" in sortie
        assert "Chemin :" in sortie

    def test_scenario_carte_vide(self, capsys):
        """Vérifie l'arrêt propre du scénario si le fichier CSV est introuvable."""
        # On passe volontairement un nom de fichier qui n'existe pas
        scenario("fichier_fantome.csv")
        sortie = capsys.readouterr().out

        assert "La carte est vide" in sortie

    def test_graphml_scenario(self, monkeypatch, capsys):
        """Vérifie que le scénario de tracé de la route sur la carte de Toulouse se déclenche."""
        entrees = iter(['A', 'D', 'oui'])
        monkeypatch.setattr('builtins.input', lambda _: next(entrees))

        scenario("test_ouvrir.csv", "toulouse.graphml")
        sortie = capsys.readouterr().out

        assert "Chargement du tracé de la route sur la carte de Toulouse" in sortie

class TestMain:
    """Tests unitaires pour le point d'entrée en ligne de commande (CLI)."""

    def test_main_nominal(self, monkeypatch, capsys):
        """Vérifie l'exécution réussie de bout en bout avec test_ouvrir.csv."""
        # L'astuce pour ne pas importer sys : on donne le chemin sous forme de string ("sys.argv")
        arguments = ["main.py", "--fichier", "test_ouvrir.csv", "--source", "A", "--cible", "D"]
        monkeypatch.setattr("sys.argv", arguments)

        main()
        sortie = capsys.readouterr().out

        assert "Distance(" in sortie
        assert "Chemin :" in sortie

    def test_graphml_nominal(self, monkeypatch, capsys):
        """
        Vérifie que le scénario de tracé de la route sur 
        la carte de Toulouse se déclenche puis erreur sur A et D.
        """
        arguments = ["main.py", "--fichier", "test_ouvrir.csv", "--source", "A",
                        "--cible", "D", "--graphml", "toulouse.graphml"]
        monkeypatch.setattr("sys.argv", arguments)

        main()
        sortie = capsys.readouterr().out

        assert "Chargement du tracé de la route sur la carte de Toulouse" in sortie

    def test_main_sommet_inconnu(self, monkeypatch, capsys):
        """Vérifie le rejet d'une source n'existant pas dans le graphe."""
        arguments = ["main.py", "--fichier", "test_ouvrir.csv",
                        "--source", "INCONNU", "--cible", "D"]
        monkeypatch.setattr("sys.argv", arguments)

        # Le programme est censé s'arrêter brutalement (sys.exit) si le noeud n'existe pas.
        # pytest.raises s'assure que cette interruption se produit bien.
        with pytest.raises(SystemExit):
            main()

        sortie = capsys.readouterr().out
        assert "n'existe pas dans le graphe" in sortie

        #Vérifie le rejet d'une cible n'existant pas dans le graphe.
        arguments = ["main.py", "--fichier", "test_ouvrir.csv",
                        "--source", "A", "--cible", "INCONNU"]
        monkeypatch.setattr("sys.argv", arguments)

        # Le programme est censé s'arrêter brutalement (sys.exit) si le noeud n'existe pas.
        # pytest.raises s'assure que cette interruption se produit bien.
        with pytest.raises(SystemExit):
            main()

        sortie = capsys.readouterr().out
        assert "n'existe pas dans le graphe" in sortie

    def test_main_graphe_vide(self, monkeypatch, capsys):
        """Vérifie l'arrêt du programme si le fichier est introuvable (graphe vide/None)."""
        arguments = ["main.py", "--fichier", "inexistant.csv", "--source", "A", "--cible", "B"]
        monkeypatch.setattr("sys.argv", arguments)

        with pytest.raises(SystemExit):
            main()

        sortie = capsys.readouterr().out
        assert "Le graphe est vide" in sortie
