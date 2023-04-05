"""
-----------------------
Ce document est un brouillon.
Sont stockés ici des morceaux de codes et de test
Le contenu de ce fichier n'est pas à prendre en compte dans la correction.
Il a uniquement pour but de ne pas polluer les autres fichiers
------------------------

"""



"""
Ne fonctionne pas
dot = graphviz.Digraph(comment='The Round Table')
dot.node('A', 'King Arthur')  # doctest: +NO_EXE
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')
dot.render('exemple_graphique', view=True)
"""

from graph import Graph, graph_from_file
"""
g = Graph([k for k in range(5)])

g.add_edge(0, 1, 10)
g.add_edge(1, 2, 10)
g.add_edge(1, 3, 15)
g.add_edge(1, 5, 15)
g.add_edge(5, 6, 15)
g.add_edge(2, 4, 10)
g.add_edge(3, 4, 10)

g2 = g.kruskal()


a , b = g2.find_parents(1)
"""
#print(g2.get_path_opti(3, 6, a, b))

#print(g)
#print(g.graph)
#print(g.edges)
#a, b = g.kruskal()
#print(b)

#print(g.get_path_with_power(1, 4, 10))
#print(g.min_power(1, 4))
#b = g.kruskal()
#print(b.get_path_with_power(1, 4, 10))
#print(b.get_path_mst(1, 4))
#print(b.min_power_mst(1, 4))


#print(g.min_power(1, 4))
#print(g.min_power_mst(1, 4))


"""
h = graph_from_file("input/network.2.in")
h.kruskal()
profondeurs, parents = h.find_parents(1)
print(h.get_path_opti(4, 5, profondeurs, parents))
"""

"""
h = graph_from_file("input/network.00.in")
h_mst = h.kruskal()
"""


#print(h.get_path_with_power(1, 9, 50))
#print(h.min_power(1, 5))
#print(h.min_power_mst(1, 5))

def camion_par_routes2(dict_route, dict_camion, tree):

    """
    On cherche à améliorer le dicitionnaire des routes.
    Pour l'instant on a pour chaque trajet (numéroté par un entier),
    une liste avec [source, destinationation, utilité].
    On cherche pour chacun de ces trajets, à rajouter le min_power
    pour effectuer le trajet et le meilleur camion.
    Le meilleur camion est le camion le moins cher
    parmi tous les camions qui ont la puissance nécéssaire.
    Comme on a un stock infini de camions, on a pas à
    s'inquiéter si un camion est mis pour plusieurs trajets.

    Paramètres:
        -----------
        dict_route: dict
            Dictionnaire des trajets qui à chaque trajet (numéroté par un
            entier) associe la liste [source, destination, gain]
        dict_camion: dict
            Dictionnaire des camions qui à chaque camion (numéroté par un
            entier) associe la liste [puissance, cout]
        tree : Graph
            Arbre couvrant minimal associé aux routes et camions

        Résultats :
        -----------
        XX
    """

    dict_route_complete = dict_route

    profondeurs, parents = tree.find_parents(1)

    check = 0

    for trajet in dict_route_complete:
        check = check + 1
        print(check)
        src, dest, gain = dict_route[trajet]
        # On cherche le min_power du trajet
        inutile, p = tree.min_power_opti(src, dest, profondeurs, parents)
        dict_route_complete[trajet].append(p)
        # On trouve les camions qui peuvent effectuer le trajet
        #camions_possibles = []
        
        """
        for camion in dict_camion:
            indice_camion = indice_camion + 1
            puissance = dict_camion[camion][0]
            #cout = dict_camion[camion][1]
            if puissance >= p:
                a = dict_camion[camion].copy()
                #a.append(indice_camion)
                camions_possibles.append(a)
                print(camions_possibles)
        # On trouve celui au coût minimal
        cout_minimal = min([i[1] for i in camions_possibles])
        indice = [i[1] for i in camions_possibles].index(cout_minimal)
        meilleur_camion = camions_possibles[indice]
        dict_route_complete[trajet].append(meilleur_camion[1])
        """
        indice_camion = 0
        meilleur_camion = 0
        coutmin = dict_camion[1][1]

        for camion in dict_camion:
            indice_camion += 1
            puissance = dict_camion[camion][0]
            if puissance >= p:
                if dict_camion[camion][1] <= coutmin:
                    coutmin = dict_camion[camion][1]
                    meilleur_camion = indice_camion
                    print(meilleur_camion)

        dict_route_complete[trajet].append(meilleur_camion)
                
    return dict_route_complete


def knapsack2(B, pt, ut, n):
   
    """_summary_

    Args:
        B (int): Budget
        pt (prix): _description_
        ut (_type_): _description_
        n (_type_): _description_

    Returns:
        _type_: _description_
    """
    if n==0 or B==0:
        return 0
    if pt[n-1]>B:
        return knapsack(B, pt, ut, n-1)
    else:
        return max(ut[n-1]+knapsack(B-pt[n-1],pt,ut,n-1),knapsack(B, pt, ut, n-1))
