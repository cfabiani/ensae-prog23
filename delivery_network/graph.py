

class Graph:
    """
    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented. 
    Attributes:
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]
        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges.
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges.
        Parameters:
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
        self.edges = []

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output

    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is
        added to the adjacency list of both end nodes.
        Parameters:
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1
        self.edges.append([node1, node2, power_min, dist])

    def voisin_acc(self, node1, power):

        """
        Cette fonction donne tous les voisins d'un sommet accessible, c'est-à-
        dire qu'il existe une arete reliant ce sommet à son voisin dont la
        puissance est inférieure à la puissance indiquée.

        Paramètres:
        -----------
        node1: NodeType
            Sommet dont on cherche les voisins
        power: int
            Puissance maximale qu'on accepte

        Résultats :
        -----------
        v : list
            Liste de tous les voisins accessibles
        """
        v = []
        for i in self.graph[node1]:
            if i[1] <= power:
                v.append(i[0])
        return v

    def get_path_with_power(self, src, dest, power):

        """
        Cette fonction donne le chemin entre deux sommets du graph.
        Si les deux sommets sont dans la même composante connexe, alors on
        parcourt avec une file le graph pour chercher la destination
        tout en enregistrant le parcours effectué.


        Si les deux sommets ne sont pas dans la même composante connexe, alors
        on renvoit None (car il n'existe alors pas de chemin). On pourrait
        vérifier dès le début que les deux points sont dans la même composante
        connexe pour éviter de parcourir le graph pour rien. Mais par la suite,
        on utilisera presque uniquement des graphes connexes, donc on évitera
        de faire à chaque fois le calcul couteux des composantes connexes

        Paramètres:
        -----------
        src: NodeType
            Sommet de départ
        dest: NodeType
            Sommet d'arrivée
        power: int
            Puissance maximale qu'on accepte sur l'ensemble du chemin

        Résultats :
        -----------
        chemin : list
            liste de tous les sommets qui constitue parcourus pour aller
            de la source à la destination. None s'il n'existe pas de chemin
        None : Nonetype
            On renvoit None s'il n'existe aucun chemin possible
        """

        seen = []
        # On construit la file
        stack = [(src, [src])]

        while stack:
            (node, chemin) = stack.pop()
            if node == dest:
                # On est arrivé, on peut arrêter l'algorithme ici
                return chemin
            if node not in seen:
                seen.append(node)
                # On récupère les voisins accessibles
                for voisin in self.voisin_acc(node, power):
                    stack.append((voisin, chemin + [voisin]))

        # La destination n'a pas été trouvé
        return None

    def parcours_en_profondeur(self, node, seen=None):

        """
        Cette fonction visite tous les sommets du graph accessibles par des
        arêtes à partir du point de départ de manière
        récursive. On explore chaque branche et si on finit d'explorer
        une branche, on revient autant en arrière que nécessaire
        pour trouver des sommets que l'on a pas encore vu

        Paramètres:
        -----------
        node: NodeType
            Point de départ du parcours en profondeur
        seen: list or Nonetype, optional
            Donne les noeuds déjà vu, évite de revenir sur nos pas dans
            la recherche d'un voisin
            Par défaut seen = None

        Résultats :
        -----------
        seen: list
            Liste de tous les sommets parcourus (qui sont donc les sommets
            réliés par un chemin existant au sommet initial)
        """

        if seen is None:
            # Si on a rien vu pour l'instant on initialise avec une liste vide
            seen = []
        if node not in seen:  # On vérifie qu'on a pas déjà vu le sommet
            seen.append(node)
            unseen = []
            for t in self.graph[node]:
                if t[0] not in seen:
                    unseen.append(t[0])
            for node in unseen:  # On travaille par récursivité
                self.parcours_en_profondeur(node, seen)
        return seen

    def connected_components(self):

        """
        Cette fonction donne les composantes connexes d'un graphe.
        On prend un premier sommet, on trouve grâce au parcours en
        profondeur tous les sommets accessibles et qui sont donc
        dans la même composante connexe. Une fois cela fait
        on prend le premier sommet qui n'est pas déjà dans une composante
        connexe, et on refait la même opération

        Paramètres:
        -----------

        Résultats :
        -----------
        connected : list
            Liste de listes (chacune des listes représente une composante
            connexe)

        """
        connected = []

        for node in self.nodes:
            if connected == []:
                connected.append(self.parcours_en_profondeur(node))
            else:
                a = True
                for cc in connected:
                    if node in cc:
                        a = False
                if a:
                    connected.append(self.parcours_en_profondeur(node))
        return connected

    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component),
        For instance, for network01.in:
        {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))

    def min_power(self, src, dest):

        """
        Cette fonction donne le power minimum nécessaire pour aller
        d'un sommet à un autre. Il peut exister plusieurs chemins
        pour aller d'un sommet A à un sommet B. On regarde
        pour tous ces chemins et on prend celui telle que la puissance
        maximale rencontrée sur l'ensenble du chemin soit minimale.
        On procédera par dichotomie

        Paramètres:
        -----------
        src : Nodetype
            Sommet de départ

        dest : Nodetype
            Sommet d'arrivée

        Résultats :
        -----------
        chemin : list
            Liste de tous les chemins parcourus pour aller
            de src à dest de telle sorte que la puissance maximale
            rencontrée soit minimale
        puissance : int
            puissance maximale rencontrée sur le chemin optimale

        """
        t = 1
        # On cherche les bornes initiales par dichotomie
        while self.get_path_with_power(src, dest, t) is None:
            t = t*2
        a = t // 2
        # print("ok1")
        b = t
        c = 0

        # On cherche par dichotomie la puissance
        while b > a:
            c = (b + a) // 2

            if self.get_path_with_power(src, dest, c) is None:
                a = c + 1
            else:
                b = c
            # print("ok2")

        chemin = self.get_path_with_power(src, dest, b)
        puissance = b
        return chemin, puissance

    def find(self, parent, x):
        """
        Cette fonction permet de trouver le parent d'un sommet

        Paramètres:
        -----------
        parent : list
            Liste des parents
        x : Nodetype
            Sommet dont on cherche le parent

        Résultats :
        -----------
        x : Nodetype
            Renvoie le parent du sommet de départ
        """

        if parent[x] == x:
            return x
        return self.find(parent, parent[x])

    def union(self, parent, rang, x, y):
        """
        Cette fonction permet de créer un lien entre x et y.
        On regarde la position et le rang de chaque sommet.
        On connecte celui qui a le rang le plus faible à celui qui
        a le rang le plus élevé. Pour cela on dit que le parent
        de celui qui a le plus faible rang est l'autre sommet.
        S'ils ont le même rang, on attribue arbitrairement
        la parenté.
        Le rang correspond au nombre d'enfants de chaque sommet.

        Paramètres:
        -----------
        parent : list
            Liste des parents
        rang : list
            Liste des rangs de chaque sommet
        x : Nodetype
            Sommet que l'on cherche à relier
        x : Nodetype
            Sommet que l'on cherche à relier
        """
        xracine = self.find(parent, x)
        yracine = self.find(parent, y)
        if rang[xracine] < rang[yracine]:
            parent[xracine] = yracine
        elif rang[xracine] > rang[yracine]:
            parent[yracine] = xracine
        else:
            parent[yracine] = xracine
            rang[xracine] += 1

    def kruskal(self):
        """
        Cette fonction permet de créer un arbre couvrant minimal
        à partir d'un graphe. On récupère la liste des
        arêtes, on  la trie par ordre croissant des power.
        On ajoute une à une les arêtes à condition que cela ne crée
        pas un cycle. On obtient ainsi un arbre couvrant minimal.
        Le résultat n'est pas unique. L'arbre possède V - 1 arêtes
        avec V le nombre de sommet du graphe initial.

        /!\ On suppose que le graphe en entrée est connexe

        Paramètres:
        -----------

        Résultats :
        -----------
        g_mst : Graph
            Arbre couvrant minimal obtenu.
            Il n'est pas unique.
        """
        # On crée les listes nécéssaires à unionfind
        parent = []
        rang = []

        # Liste de toutes les arêtes conservées
        resultat = []

        # On crée un graphe vide qu'on va remplir
        g_mst = Graph()

        """
        On pouvait utiliser cette méthode pour récupérer la liste de toutes
        les arêtes et ensuite les trier. Mais il apparaissait plus rapide
        de conserver les arêtes dans une liste créer au moment de la création
        du graph.

        liste_arete = []
        seen = []
        for i in self.nodes:
            for j in self.graph[i]:

                a = j[0]
                b = j[1]

                if [i, a] and [a, i] not in seen:
                    seen.append([i, a])

                    liste_arete.append([i, a, b])
        """
        # On trie les arêtes par ordre croissant des power
        liste_arete = self.edges  # On récupère la liste de toutes les arêtes
        liste_croissante_arete = sorted(liste_arete, key=lambda x: x[2])

        V = self.nb_nodes

        # On initialise la liste des parents et du rang avec les valeurs
        # de base
        for n in range(V+1):
            parent.append(n)
            rang.append(0)

        # On parcourt toutes les aretes

        for i in liste_croissante_arete:
            if len(resultat) == V - 1:
                # On a V-1 aretes, c'est un arbre couvrant
                return g_mst

            # On vérifie que les deux sommets n'ont pas le même
            # parent pour ne pas former de cycles
            x = self.find(parent, i[0])
            y = self.find(parent, i[1])

            if x != y:
                resultat.append(i)
                # On ajoute l'arete dans l'arbre
                g_mst.add_edge(i[0], i[1], i[2])
                # On relie les points grâce à union
                self.union(parent, rang, x, y)

        # Si le graph est déjà un arbre, on arrive ici
        return g_mst

    def get_path_mst(self, src, dest):

        """
        On cherche le chemin entre deux sommets. On suppose ici que le graph
        utilisé est un arbre couvrant minimal. Le chemin sera donc unique
        Fonction identique à get_path_with_power à l'exception qu'on ne
        retrouve plus en entrée le power. En échange, on enregistre les
        puissances rencontrées et on renvoit la liste des puissances en
        plus de chemin. Cela nous servira pour la fonction get_path_mst.
        Il n'est également plus nécessaire d'utiliser la fonction voisin
        accessible.

        Paramètres:
        -----------
        src: NodeType
            Sommet de départ
        dest: NodeType
            Sommet d'arrivée

        Résultats :
        -----------
        chemin : list
            liste de tous les sommets qui constitue parcourus pour aller
            de la source à la destination. None s'il n'existe pas de chemin
        power: list
            Liste des puissances rencontrées sur le chemin
        None : Nonetype
            On renvoit None s'il n'existe aucun chemin possible
        """
        seen = []
        stack = [(src, [src], [])]
        # Cette fois-ci on a dans la queue une liste pour les power rencontrés
        while stack:
            (node, chemin, power) = stack.pop()
            if node == dest:
                return chemin, power
            if node not in seen:
                seen.append(node)
                # On parcout tous les voisins
                for voisin in self.graph[node]:
                    a = (voisin[0], chemin + [voisin[0]], power + [voisin[1]])
                    stack.append(a)
        return None

    def min_power_mst(self, src, dest):

        """
        Dans le cas d'un arbre couvrant minimal, on a une unique
        chemin pour relier deux sommets. Il suffit donc de récupérer
        le power max rencontré dans le chemin pour
        connaitre la puissance minimale nécéssaire à effectuer le trajet

        Paramètres:
        -----------
        src: NodeType
            Sommet de départ
        dest: NodeType
            Sommet d'arrivée

        Résultats :
        -----------
        max(power) : int
            Puissance nécessaire pour effectuer le trajet
        """
        # On récupère la liste des puissances du chemin
        chemin, power = self.get_path_mst(src, dest)
        return max(power)

    def find_parents(self, start):

        """
        On considère que le graph utilisé est un arbre. On prend
        un noeud quelconque qui sera le sommet de l'arbre.
        On cherche la profondeur de chaque noeud, c'est-à-dire
        combien d'arêtes sont nécessaire pour aller au sommet de l'arbre.
        On cherche également un dictionnaire des parents, qui donnerait
        le parent de chaque noeud, c'est-à-dire le voisin dans le sens
        qui va vers le sommet de l'arbre

        Paramètres:
        -----------
        start: NodeType
            Point de départ

        Résultats :
        -----------
        pronfondeurs : dict
            Dictionnaire qui à chaque noeud associe sa profondeur
        parents : dict
            Dictionnaire qui à chaque noeud associe une liste contenant son
            parent et la puissance de l'arête qui le relie à son parent
        """
        # On crée les dictionnaires
        parents = {}
        profondeur = dict([(sommet, 0) for sommet in self.nodes])
        deja_vu = dict([(sommet, False) for sommet in self.nodes])
        # On fixe des valeurs initiales pour le point de départ
        deja_vu[start] = True
        parents[start] = [start, -1]

        # On crée un parcours en profondeur de l'arbre

        def find_parents_auxiliaires(graph, node):
            # On parcourt les voisins
            for neighbor, power, distance in graph[node]:
                if not deja_vu[neighbor]:
                    deja_vu[neighbor] = True
                    # On ajoute les valeurs aux dicitionnaires
                    parents[neighbor] = [node, power]
                    # A chaque fois, on est plus profond que son parent
                    profondeur[neighbor] = profondeur[node] + 1
                    find_parents_auxiliaires(graph, neighbor)

        # On lance la fonction
        arbre = self.graph
        find_parents_auxiliaires(arbre, start)

        return profondeur, parents

    def min_power_opti(self, src, dest, profondeurs, parents):

        """
        On prend en entrée uniquement des arbres couvrant minimaux.
        On sait que le chemin entre deux noeuds est unique.
        On cherche l'ancètre commun aux deux noeuds et on
        fait le chemin src -> ancêtre commun -> dest
        Cette fonction étant longue, on détaillera dans le corps du texte

        Paramètres:
        -----------
        src: Nodetype
            Point de départ
        dest: Nodetype
            Point d'arrivée
        profondeurs : dict
            dictionnaire des profondeurs
        parents : dict
            dictionnaires des parents

        Résultats :
        -----------
        path_final : list
            chemin pour aller de src à dest
        max(powerfinal) :  int
            puissance maximale rencontrée, qui est la min_power pour ce trajet
        """

        # Initialisation
        prof_src = profondeurs[src]
        prof_dest = profondeurs[dest]
        # Chemin de la source à l'ancêtre commun
        pathsrc = [src]
        powerpathsrc = []
        # Chemin de la destination à l'ancêtre commun
        pathdest = [dest]
        powerpathdest = []

        """
        Si les deux noeuds sont à profondeurs différentes, on
        ramène le point le plus profond à la même profondeur que
        l'autre. On enregistre le chemin parcouru
        """
        if prof_src > prof_dest:
            for i in range(prof_src - prof_dest):
                p = parents[pathsrc[-1]][0]
                power = parents[pathsrc[-1]][1]
                # On ajoute le parent du noeud
                pathsrc.append(p)
                # On ajoute les puissances parcourues
                powerpathsrc.append(power)
        elif prof_dest > prof_src:
            for i in range(prof_dest - prof_src):
                p = parents[pathdest[-1]][0]
                power = parents[pathdest[-1]][1]
                # On ajoute le parent du noeud
                pathdest.append(p)
                # On ajoute les puissances parcourues
                powerpathdest.append(power)

        """
        Maintenant qu'on est à la même profondeur, on remonte en vérifiant
        à chaque fois si on a pas trouvé un ancêtre commun
        """

        while pathdest[-1] != pathsrc[-1]:
            p1 = parents[pathsrc[-1]]
            p2 = parents[pathdest[-1]]
            pathsrc.append(p1[0])
            powerpathsrc.append(p1[1])
            pathdest.append(p2[0])
            powerpathdest.append(p2[1])

        """
        on a l'ancêtre commun et les chemins :
        - src -> ancêtre commun
        - dest -> ancêtre commun
        On concatène les listes, ce qui est un peu laborieux
        """
        if len(pathsrc) != 1 and len(pathdest) != 1:
            pathdest.reverse()
            powerpathdest.reverse()
            pathfinal = pathsrc + pathdest[1:]
            powerfinal = powerpathsrc + powerpathdest[1:]

        if len(pathdest) == 1:
            pathfinal = pathsrc
            powerfinal = powerpathsrc

        if len(pathsrc) == 1:
            pathdest.reverse()
            powerpathdest.reverse()
            pathfinal = pathdest[1:]
            powerfinal = powerpathdest[1:]

        if powerfinal == []:
            return [], 0

        return pathfinal, max(powerfinal)

    """
    Ci-dessous l'algorithme de Dijkstra
    """

    def find_min_Dijkstra(self, Q, d):
        mini = float('inf')
        node = -1
        for s in Q:
            if d[s] < mini:
                mini = d[s]
                node = s
        return node

    def dist_Dijkstra(self, node1, node2, power):
        d = 0
        a = True
        for i in self.graph[node1]:
            if node2 == i[0] and i[1] <= power:
                d = i[2]
                a = False
        if a:
            d = float('inf')
        return d

    def maj_dist_Dijkstra(self, node1, node2, d, power, ancestor):
        P = self.dist_Dijkstra(node1, node2, power)
        if d[node2] > d[node1]+P:
            d[node2] = d[node1]+P
            ancestor[node2] = node1
        return (d, ancestor)

    def Dijkstra(self, src, dest, power, ancestor=None):
        assert src in self.parcours_en_profondeur(dest)
        d = {}
        for node in self.nodes:
            d[node] = float('inf')
        d[src] = 0
        if ancestor is None:
            ancestor = {}
        Q = self.parcours_en_profondeur(src)
        while Q != []:
            node1 = self.find_min_Dijkstra(Q, d)
            if node1 == dest:
                path = []
                node = dest
                while node != src:
                    path = [node]+path
                    node = ancestor[node]
                return [src]+path
            if node1 != -1:
                Q.remove(node1)
            else:
                break
            for a in self.graph[node1]:
                d, ancestor = self.maj_dist_Dijkstra(node1, a[0], d, power, ancestor)
        return None

    """
    Fin l'algorithme de Dijkstra
    """


def graph_from_file(filename):
    with open(filename, "r") as file:
        n, m = map(int, file.readline().split())
        g = Graph(range(1, n+1))
        for _ in range(m):
            edge = list(map(int, file.readline().split()))
            if len(edge) == 3:
                node1, node2, power_min = edge
                g.add_edge(node1, node2, power_min)  # will add dist=1 by default
            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)
            else:
                raise Exception("Format incorrect")
    return g



