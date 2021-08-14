###
#
# implémentation de la structure de données arbre BK permettant la 
# recherche de mots proches en utilisant la distance de 
# Damerau-Levenshtein 
#
###

def distDL(u, v):
    """
        Calcul de la distance Damereau-Levenshtein entre le mot u et v
    """

    # "Infini" -- Utilisée pour empêcher les transpositions des premiers caractères
    INF = len(u) + len(v)

    # Matrix: (M + 2) x (N + 2)
    matrix  = [[INF for n in xrange(len(v) + 2)]]
    matrix += [[INF] + range(len(v) + 1)]
    matrix += [[INF, m] + [0] * len(v) for m in xrange(1, len(u) + 1)]

    # Contient la dernière ligne de chaque élément rencontré: DA dans le pseudocode Wikipedia
    last_row = {}

    # remplissage de la table des coûts
    for row in xrange(1, len(u) + 1):
        # Caractere courant dans u
        ch_u = u[row-1]

        # la colonne du dernier match de la ligne: DB dans le pseudocode
        last_match_col = 0

        for col in xrange(1, len(v) + 1):
            # Caractere courant dans v
            ch_v = v[col-1]

            # Derniere ligne avec un match
            last_matching_row = last_row.get(ch_v, 0)

            # Cout de la substitution
            cost = 0 if ch_u == ch_v else 1

            # Calcul de la distance de la sous-chaine
            matrix[row+1][col+1] = min(
                matrix[row][col] + cost, # Substitution
                matrix[row+1][col] + 1,  # Addition
                matrix[row][col+1] + 1,  # Deletion

                # Transposition
                matrix[last_matching_row][last_match_col]
                    # Couts des lettres entre celles transposées
                    # 1 addition + 1 suppression = 1 substitution
                    + max((row - last_matching_row - 1),
                          (col - last_match_col - 1))
                    # Cout de la transposition
                    + 1)

            # S'il y a match, on met last_match_col à jour
            if cost == 0:
                last_match_col = col

        # Mettre à jour la derniere ligne pour le caractère courant
        last_row[ch_u] = row

    # Retourner le dernier element
    return matrix[-1][-1]

""" 
décommenter pour tester la fonction
"""
#distDL("faute_de_frappe", "fote_de_farppe")

def dict_words(path):
    """
        charge le dictionnaire à partir de son chemin
    """
    with open(path, 'r') as file:
        data = file.read()
    return data.split()

"""
charger le dictionnaire
"""
dict = dict_words("Dict.txt")

def calcul_distance_dict(dict, mot, e):
    """
    calcule la distance entre mot et tous les mots de dict
    et affiche les mots à au plus e de mot
    """
    for word in dict:
        dist = distDL(word, mot)
        if dist <= e:
            print("distance("),
            print(word),
            print(","),
            print(mot),
            print(") ="),
            print(dist)
                
#calcul_distance_dict(dict, "accommodate", 5)

def time_of(func, *args):
    """
    calcule le temps d'exécution d'une méthode ou fonction
    param: func: le nom de la fonction à tester
    param: *args: les arguments passés à func (séparés par (,) si plusieurs) 
    """
    import time
    t = time.time()
    res = func(*args)
    print("Time: ", (time.time() - t))
    return res

#print(time_of(calcul_distance_dict, dict, "accommodate", 5))

def construireArbBK(dict):
        """
            Construction de l'arbre
        """
        it = iter(dict)
        racine = next(it)
        arbBK = (racine, {})

        for i in it:
            inserer_mot(arbBK, i)
        return arbBK

def inserer_mot(arbBK, mot):
    """
    Ajoute un mot à l'arbre
    :param arbBK: l'arbre où insérer le mot 
    :param mot: le mot à insérer 
    """
    noeud = arbBK
    if noeud is None:
        arbBK = (mot, {})
        return

    while True:
        parent, fils = noeud
        distance = distDL(mot, parent)
        noeud = fils.get(str(distance))
        if noeud is None:
            fils[str(distance)] = (mot, {})
            break
            
def chercherArbBK(arbBK, mot, e):
        """
            renvoie l’ensemble de tous les mots dans arbBK à distance au plus e de mot
            la recherche se fait par procédé récursif.
        """
        def recuperer_liste(parent):
            p_mot, fils = parent
            distance = distDL(mot, p_mot)
            res = []
            if distance <= e:
                res.append((distance, p_mot))

            for i in range(distance - e, distance + e + 1):
                f = fils.get(str(i))
                if f is not None:
                    res.extend(recuperer_liste(f))
            return res

        # tri ascendant par distance
        return sorted(recuperer_liste(arbBK))

def sauvegarderArbBK(arbBK, chemin):
        import json
        if not chemin:
            import os
            chemin = os.path.join(os.getcwd(), 'tree.json')
        with open(chemin, 'w') as file:
            file.write(json.dumps(arbBK))

def restaurerArbBK(chemin):
        import json
        if not chemin:
            import os
            chemin = os.path.join(os.getcwd(), 'tree.json')
        with open(chemin, 'r') as file:
            arbBK = json.loads(file.read())
        return arbBK


"""
construire l'arbre
"""
#tree = construireArbBK(dict)

"""
Rechercher dans l'arbre
"""
#chercherArbBK(tree, "word", 4)

"""
Sauvegarde de l'arbre
"""
#sauvegarderArbBK(tree, "output")

"""
Restauration de l'arbre
"""
#arbreBK = restaurerArbBK("output")

