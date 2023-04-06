from graph import Graph, graph_from_file
import time

# import graphviz
# from graphviz import Digraph

data_path = "../input/"


def routes_from_file(filename):
    # Cette fonction lit les fichiers routes.x.in comme graph_from_file
    file = open(filename, 'r')
    lines = file.readlines()
    file.close()
    R = dict([(i, []) for i in range(1, int(lines.pop(0))+1)])
    i = 0
    for line in lines:
        i += 1
        words = line.split()
        R[i].append(int(words[0]))
        R[i].append(int(words[1]))
        R[i].append(int(words[2]))
    return R


def routes_from_file_2(filename):
    # Cette fonction lit les fichiers routes.x.out comme graph_from_file
    file = open(filename, 'r')
    lines = file.readlines()
    file.close()

    R = {}
    i = 0
    for line in lines:
        i += 1
        R[i] = []
        words = line.split()
        R[i].append(int(words[0]))
        R[i].append(int(words[1]))
        R[i].append(int(words[2]))
        R[i].append(int(words[3]))
        R[i].append(int(words[4]))
        R[i].append(int(words[5]))
    return R


def trucks_from_file(filename):
    # Cette fonction lit les fichiers trucks.x.in comme graph_from_file
    file = open(filename, 'r')
    lines = file.readlines()
    file.close()
    T = dict([(i, []) for i in range(1, int(lines.pop(0))+1)])
    i = 0
    for line in lines:
        i += 1
        words = line.split()
        T[i].append(int(words[0]))
        T[i].append(int(words[1]))
    return T


def truckperpath(dict_route, dict_camion, tree):

    """_summary_
    args:
        dict_route: dict
        dict_camion: dict
        tree: Graph
    returns:
        dict_route_complete: dict
    retourne un dictionnaire avec pour chaque trajet (numéroté par un entier),
    une liste avec [source, destination, utilité, min_power, meilleur camion,
    cout du meilleur camion]
    """
    dict_route_complete = dict_route
    profondeurs, parents = tree.find_parents(1)
    # check = 0
    for trajet in dict_route_complete:
        # check = check + 1
        # print(check)
        src, dest, gain = dict_route[trajet]
        # On cherche le min_power du trajet
        inutile, p = tree.min_power_opti(src, dest, profondeurs, parents)
        dict_route_complete[trajet].append(p)
        # On trouve les camions qui peuvent effectuer le trajet
        camions_possibles = []
        for camion in dict_camion:
            puissance = dict_camion[camion][0]
            if puissance >= p:
                camions_possibles.append(camion)
        # On trouve celui au coût minimal
        cout_minimal = min([dict_camion[i][1] for i in camions_possibles])
        indice = [dict_camion[i][1] for i in camions_possibles].index(cout_minimal)
        meilleur_camion = camions_possibles[indice]
        dict_route_complete[trajet].append(meilleur_camion)
        dict_route_complete[trajet].append(cout_minimal)
    return dict_route_complete


def complete_route(trucks, filename):
    """A partir du dictionnaire obtenu avec la fonction trucks from file,
    On crée un fichier routes out qui est équivalent au fichier
    routes in mais où on rajoute à chaque ligne
    le power min du trajet, le numéro du camion optimal et le cout de
    ce camion.

    """
    with open(filename, 'w') as file:
        for i in trucks.values():
            i2 = str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + " " + str(i[3]) + " " + str(i[4]) + " " + str(i[5])
            print(i2)
            Ligne = i2 + "\n"
            file.write(Ligne)


def knapsack_brute_force(B, dict_route_complete, pt=None, ut=None, n=None):

    """_summary_
    Args:
        B (int): Budget
        pt (liste): prix des trajets/camion
        ut (liste): utilité des trajets/camion
        n (int): nombre de trajets possible

    Returns:
        liste: collection de camion/trajet, et l'utilité totale

    knapsack_brute_force permet de trouver la collection de camion/trajet qui
    maximise l'utilité totale, en utilisant la méthode brute force
    """

    if n == None:
        n = len(dict_route_complete)
        pt = [dict_route_complete[i][-1] for i in dict_route_complete]
        ut = [dict_route_complete[i][2] for i in dict_route_complete]
    if n == 0 or B == 0:
        return 0
    if pt[n-1] > B:
        return knapsack_brute_force(B, dict_route_complete, pt, ut, n-1)
    else:
        return max(ut[n-1]+knapsack_brute_force(B-pt[n-1], dict_route_complete ,pt,ut,n-1),knapsack_brute_force(B, dict_route_complete, pt, ut, n-1))


def knapsack_dynamic(B, dict_route_complete):

    """_summary_
    args:
        B (int): Budget
        dict_route_complete (dict): dictionnaire des camions affectées à des
        trajets
    returns:
        liste: Collection de camion et de trajet, et l'utilité totale

    knapsack_dynamic permet de trouver la collection de camion/trajet qui
    maximise l'utilité totale, en utilisant la méthode dynamique
    """
    n = len(dict_route_complete)
    pt = [dict_route_complete[i][-1] for i in dict_route_complete]
    ut = [dict_route_complete[i][2] for i in dict_route_complete]
    K = [[0 for i in range(int(B)+1)] for j in range(len(dict_route_complete)+1)]
    for i in range(n+1):
        # print("ok")
        for j in range(int(B)+1):
            if i == 0 or j == 0:
                K[i][j] = 0
            elif pt[i-1] <= j:
                K[i][j] = max(ut[i-1]+K[i-1][j-pt[i-1]], K[i-1][j])
            else:
                K[i][j] = K[i-1][j]
    return K[n][int(B)]


def knapsack_dynamic_2(B, dict_route_complete):

    """_summary_
    args:
        B (int): Budget
        dict_route_complete (dict): dictionnaire des camions affectées à des
        trajets
    returns:
        liste: Collection de camion et de trajet, et l'utilité totale

    knapsack_dynamic_2 permet de trouver la collection de camion/trajet qui
    maximise l'utilité totale, en utilisant la méthode dynamique
    quand tous les couts sont multiples de 10 000
    """
    n = len(dict_route_complete)
    pt = [dict_route_complete[i][-1] // 10000 for i in dict_route_complete]
    ut = [dict_route_complete[i][2] for i in dict_route_complete]
    K = [[0 for i in range(B//10000+1)] for j in range(len(dict_route_complete)+1)]
    for i in range(n+1):
        # print("ok")
        for j in range(B//10000+1):
            if i == 0 or j == 0:
                K[i][j] = 0
            elif pt[i-1] <= j:
                K[i][j] = max(ut[i-1]+K[i-1][j-pt[i-1]], K[i-1][j])
            else:
                K[i][j] = K[i-1][j]
    return K[n][B//10000]


def rapport(B, dict_route_complete):
    """
    args:
        B (int) : Budget
        dict_route_complete (dict): dictionnaire des camions affectées à des
        trajets
    returns:
        liste : liste des trajets choisis et des camions associes
        int : utilite totale

    Cette fonction implémente un algorithme glouton pour résoudre de manière
    locale en choisissant les trajets avec le meilleur rapport utilite/cout
    jusqu'à remplir le budget.

    """

    # On commence par établir la liste des trajets avec le camion qui
    # l'effectue et la rapport utilite/cout du trajet
    Liste_trajets_rapports = []
    for trajet in dict_route_complete:
        numero_trajet = trajet
        numero_camion = dict_route_complete[trajet][4]
        utilite_trajet = dict_route_complete[trajet][2]
        cout_trajet = dict_route_complete[trajet][5]
        list_trajet = [numero_trajet, numero_camion, utilite_trajet / cout_trajet]
        Liste_trajets_rapports.append(list_trajet)
    # On trie la liste par rapport au rapport utilite/cout
    Liste_triee = sorted(Liste_trajets_rapports, key=lambda x: x[1])
    # On ajoute les camions des trajets avec les meilleurs rapports
    # jusqu'à remplir le budget
    somme_cout = 0
    utilite = 0
    Liste_trajet_finale = []

    for j in range(len(Liste_triee)):
        numero = Liste_triee[j][0]
        camion = Liste_triee[j][1]
        somme_cout = somme_cout + dict_route_complete[numero][5]
        if somme_cout < B:
            Liste_trajet_finale.append([numero, camion])
            utilite = utilite + dict_route_complete[numero][2]
        else:
            return Liste_trajet_finale, utilite
    return Liste_trajet_finale, utilite


# Génération des routes ci_dessous

"""
Exemple de la génération du fichier routes.1.out
qui associe routes.1.in, network.1.in et trucks.1.in

h = graph_from_file("input/network.1.in")
h_mst = h.kruskal()
r = routes_from_file("input/routes.1.in")
t = trucks_from_file("input/trucks.1.in")

z = truckperpath(r, t, h_mst)
complete_route(z, "input/routes.1.out")

----------------------------------------

Exemple de la génération du fichier routes.2_1.out
qui associe routes.2.in, network.2.in et trucks.1.in

h = graph_from_file("input/network.2.in")
h_mst = h.kruskal()
r = routes_from_file("input/routes.2.in")
t = trucks_from_file("input/trucks.2.in")

z = truckperpath(r, t, h_mst)
complete_route(z, "input/routes.2_2.out")

---------------------------------------

Exemple de la génération du fichier routes.2_1.out
qui associe routes.2.in, network.2.in et trucks.2.in

h = graph_from_file("input/network.2.in")
h_mst = h.kruskal()
r = routes_from_file("input/routes.2.in")
t = trucks_from_file("input/trucks.2.in")

z = truckperpath(r, t, h_mst)
complete_route(z, "input/routes.2_2.out")

"""

# Ci dessous le calcul des temps et des résultats pour le problème du sac à dos

"""

z = routes_from_file_2("input/routes.1.out")


debut = time.perf_counter()
print(knapsack_dynamic_2(250000, z))
fin = time.perf_counter()
print(fin-debut, "temps1")

debut2 = time.perf_counter()
a, b = rapport(int(250000), z)
print(b)
fin2 = time.perf_counter()
print(fin2-debut2, "temps2")

debut3 = time.perf_counter()
print(knapsack_dynamic(250000, z))
fin3 = time.perf_counter()
print(fin3-debut3, "temps3")

"""
