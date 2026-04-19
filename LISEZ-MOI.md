============================================================================================================================================
            Projet de Théorie des Graphes (Algorithme de Dijkstra)
============================================================================================================================================
Ce projet est le fruit de notre travail sur les graphes orientés et pondérés.
L'idée était de coder un module capable de calculer le chemin le plus court entre deux points géographiques 
en utilisant le célèbre algorithme de Dijkstra.
(La mise en forme de certaines lignes peut paraître originale, 
    cela est dû au respect des conventions de pylint pour créer un code plus beau)

============================================================================================================================================
            COMMENT LANCER LE PROGRAMME ?
============================================================================================================================================
On a prévu deux façons de l'utiliser, selon si vous préférez la ligne de commande pure ou un module plus interactif.

=======     ATTENTION !!!     ======
#                                  #
#    Dans les deux cas suivant,    #
#   stocker les fichier CSV et     #
# graphml dans le dossier donnees. #
====================================

*Option A : Le mode "commande" (demandé par le sujet) 
Utilisez le fichier main.py. Il prend des arguments précis et vous donne le résultat direct.
Commande : python main.py --fichier toulouse.csv --source 625236 --cible 2493904512 (optionnel : --graphml toulouse.graphml)

*Option B : Le mode "démo" (plus convivial)
Lancez le fichier demonstration.py. Le script vous guidera et vous demandera, après les fichiers CSV et graphml,
de taper le départ et l'arrivée directement dans la console à l'aide d'une carte représentant
les coordonnées des différentes destinations (si le fichier CSV est petit).

============================================================================================================================================
            LE FORMAT DES DONNEES
============================================================================================================================================

Le programme lit des fichiers CSV (en UTF-8). Chaque ligne représente un trajet (un arc) entre deux villes avec leurs coordonnées.
Format : depart, x_depart, y_depart, arrivee, x_arrivee, y_arrivee
Note : Comme le fichier ne donne pas directement le poids des trajets, 
on le calcule nous-mêmes en utilisant la distance euclidienne entre les deux points.
En ce sens, il n'y aura jamais de poids négatifs sur les arcs, 
donc des except ou des test serait superflus voir irréalisables.

Un fichier graphml peut aussi être ajouté pour un affichage plus détaillé du chemin.

============================================================================================================================================
            COMMENT ON A ORGANISE LE CODE
============================================================================================================================================
On a découpé le projet en plusieurs fichiers pour que ce soit plus propre:

*classes.py : C'est le moteur. On y trouve les définitions des Noeuds, des Arcs et toute la logique de Dijkstra.
*fonctions.py : Ce fichier s'occupe de la "paperasse" (charger le CSV et afficher les résultats proprement).
*main.py : L'outil pour lancer le programme en ligne de commande.
*demonstration.py : Notre script pour la présentation interactive.
*static_methods.py : Un fichier contenant les @static_methods qui auraient pris trop de place dans classes.py
*test_projet.py : Tous nos tests pour vérifier que rien ne casse (on utilise pytest)

============================================================================================================================================
            NOS CHOIX TECHNIQUES
============================================================================================================================================

Pour le Graphe : On stocke les sommets dans une liste et les arcs dans un dictionnaire. 
Pourquoi un dictionnaire ? 
Parce que ça permet de retrouver le poids d'un trajet hyper rapidement, en O(1).

Pour Dijkstra : On utilise aussi des dictionnaires pour garder une trace des distances et des parents de chaque point,
ce qui rend les mises à jour très efficaces.
Important : Un trajet de A vers B n'est pas forcément le même que de B vers A (c'est un graphe orienté). 
On s'assure aussi que tous les poids sont positifs, car c'est une règle d'or pour Dijkstra.

============================================================================================================================================
            POURQUOI PAS DE POIDS NEGATIFS ?
============================================================================================================================================
C'est une question de logique : Dijkstra est un algorithme "glouton". 
Il part du principe que dès qu'il a trouvé un chemin vers un point, c'est forcément le meilleur. 
S'il y avait des poids négatifs, on pourrait continuer de réduire la distance indéfiniment 
en repassant par certains chemins, et l'algorithme se tromperait ou ne s'arrêterait jamais.

        CONTRE-EXEMPLE MINIMAL :

Soit un graphe composé de trois nœuds A, B, C et de trois arcs :

*A -> B (poids 10)
*A -> C (poids 5)
*B -> C (poids -7)

Si l'on cherche le plus court chemin de A vers C :
À l'initialisation, A est à 0. 
Les voisins sont B (10) et C (5).
ERREUR : Comme C est le plus petit, Dijkstra le "verrouille" et considère que la distance la plus courte pour aller à C est 5.
Il passe ensuite à B (distance 10). Il voit l'arc B -> C avec un poids de -7.Le calcul serait 10 + (-7) = 3.
Mais comme C est déjà marqué comme "visité/terminé", l'algorithme standard ne revient pas en arrière pour corriger le tir.

Résultat : 
Dijkstra te dira que le chemin est A -> C (coût 5), alors que le vrai plus court chemin est A -> B -> C (coût 3).

============================================================================================================================================
            Campagne de tests (Couverture des cas limites)
============================================================================================================================================
Pour tester le programme sans avoir à créer manuellement des fichiers ou à taper au clavier à chaque fois,
on a utilisé des fixtures provenants de pytest :
( docu : https://docs.pytest.org/en/7.1.x/reference/reference.html?highlight=tmp_path#fixtures )

*tmp_path : crée un petit espace de travail éphémère pour tester la lecture des fichiers
    sans polluer le disque dur.

*monkeypatch : joue le rôle de l'utilisateur, il envoie automatiquement les réponses aux 'input()'
    pour qu'on puisse tester la navigation sans toucher au clavier.

*capsys : intercepte tout ce que le programme 'print' dans la console,
    ce qui nous permet de vérifier que l'affichage final est exactement celui attendu par le prof.

*sys (via monkeypatch) : nous permet de simuler de vraies commandes dans le terminal, avec des options comme '--source' 
    ou '--cible', pour valider que le fichier 'main.py' fonctionne parfaitement sans intervention humaine.

        LA COUVERTURE INCLUT :

*Chargement CSV : Test de fichiers valides, de fichiers contenant des formats erronés (ValueError interceptée), 
    et de fichiers inexistants (FileNotFoundError interceptée).

*Calcul de chemin et inatteignabilité : Test d'un chemin nominal, d'un sommet de départ égal au sommet d'arrivée (coût 0),
    et d'une cible isolée (renvoie une liste vide et +inf).

*Règle du minimum : Vérification mathématique isolée prouvant que 
    l'algorithme ne met à jour une distance que si la condition d'optimisation C(j) > C(i) + cij est strictement remplie.

*Erreur poids négatif : Test simulant la modification forcée du dictionnaire arcs avec une valeur négative.
    Le test vérifie que la méthode plus_court_chemin lève une ValueError immédiate, validant la robustesse du code.

============================================================================================================================================
            OPTIMISATIONS ALGORITHMIQUES ET PERFORMANCES
============================================================================================================================================
L'algorithme de Dijkstra classique a été remanié pour traiter 
efficacement les graphes à très grande échelle (comme le réseau de Toulouse).

=======     PERFORMANCES     =======
#                                  #
#   Le temps d'exécution sur le    #
#   fichier complet est passé de   #
#   plusieurs minutes à une        #
#   fraction de seconde.           #
====================================

* L'utilisation d'un tas binaire (File de priorité)
La recherche linéaire du sommet le plus proche a été remplacée par l'utilisation du module natif `heapq`.
Cette structure maintient le sommet ayant la distance minimale à l'index 0.
L'extraction passe d'une complexité de O(V) à O(log V).
L'algorithme manipule des tuples (distance, etiquette) pour bénéficier du tri natif de Python.

* Le pré-calcul via un dictionnaire d'adjacence
Le goulot d'étranglement majeur résidait dans la recherche dynamique des voisins.
Désormais, lors de l'initialisation du graphe, un dictionnaire `self.adjacence` est généré.
Il stocke directement l'étiquette cible et le poids précalculé pour chaque sommet,
réduisant l'accès aux voisins à une complexité de O(1) et évitant de reparcourir l'ensemble des nœuds de la carte.

* La suppression des instanciations en boucle
Dans la boucle la plus profonde de l'algorithme, la création itérative d'objets (comme les instances `Arc`)
et les conversions de types (comme les `list()`) ont été totalement retirées.
Les données sont manipulées via des tuples, ce qui réduit considérablement la charge processeur.

* La condition d'arrêt anticipé
L'algorithme n'explore pas l'entièreté de la ville si ce n'est pas nécessaire.
La boucle principale intègre une condition d'arrêt `break` qui s'active dès que
l'étiquette du noeud d'arrivée est définitivement validée (extraite du tas binaire).
