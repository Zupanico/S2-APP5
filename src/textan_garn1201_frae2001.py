#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" Ce fichier contient la classe TextAn, à utiliser pour résoudre la problématique.
    C'est un gabarit pour l'application de traitement des fréquences de mots dans les oeuvres d'auteurs divers.

    Les méthodes apparaissant dans ce fichier définissent une API qui est utilisée par l'application
    de test test_textan.py
    Les paramètres d'entrée et de sortie (Application Programming Interface, API) sont définis,
    mais le code est à écrire au complet.
    Vous pouvez ajouter toutes les méthodes et toutes les variables nécessaires au bon fonctionnement du système

    La classe TextAn est invoquée par la classe TestTextAn (contenue dans test_textan.py) :

        - Tous les arguments requis sont présents et accessibles dans args (dans le fichier test_textan.py)
        - Note : vous pouvez tester votre code en utilisant les commandes :
            + "python test_textan.py"
            + "python test_textan.py -h" (donne la liste des arguments possibles)
            + "python test_textan.py -v" (mode "verbose", qui indique les valeurs de tous les arguments)

    Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
"""

from textan_common import TextAnCommon
import math
import re


class TextAn(TextAnCommon):
    """Classe à utiliser pour coder la solution à la problématique :

        - La classe héritée TextAnCommon contient certaines fonctions de base pour faciliter le travail :
            - recherche des auteurs
            - ouverture des répertoires
            - et autres (voir la classe TextAnCommon pour plus d'information)
            - La classe ParsingClassTextAn est héritée par TextAnCommon et lit la ligne de commande
        - Les interfaces du code à développer sont présentes, mais tout le code est à écrire
        - En particulier, il faut compléter les fonctions suivantes :
            - dot_product_dict (dict1, dict2)
            - dot_product_aut (auteur1, auteur2)
            - doct_product_dict_aut (dict, auteur)
            - find_author (oeuvre)
            - gen_text (auteur, taille, textname)
            - get_nth_element (auteur, n)
            - analyze()

    Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
    """

    # Signes de ponctuation à retirer (compléter cette liste incomplète)
    PONC = ["!", ",", ".", ":", ";", "?", "'"]

    def __init__(self) -> None:  # Nicolas
        """Initialize l'objet de type TextAn lorsqu'il est créé

        Args :
            (void) : Utilise simplement les informations fournies dans la classe TextAnCommon

        Returns :
            (void) : Ne fait qu'initialiser l'objet de type TextAn
        """

        # Initialisation des champs nécessaires aux fonctions fournies
        super().__init__()

        # Au besoin, ajouter votre code d'initialisation de l'objet de type TextAn lors de sa création
        self.compte_mots = {}  # int(occurence):tuple(ngram)

        return

    # TODO Ajouter les structures de données et les fonctions nécessaires à l'analyse des textes,
    #   la production de textes aléatoires, la détection d'oeuvres inconnues,
    #   l'identification des n-ièmes mots les plus fréquents
    #
    # If faut coder les fonctions find_author(), gen_text(), get_nth_element() et analyse()
    # La fonction analyse() est appelée en premier par test_textan.py
    # Ensuite, selon ce qui est demandé, les fonctions find_author(), gen_text() ou get_nth_element() sont appelées

    @staticmethod
    def dot_product_dict(
            dict1: dict, dict2: dict,
    ) -> float:
        """Calcule le produit scalaire NORMALISÉ de deux vecteurs représentés par des dictionnaires

        Args :
            dict1 (dict) : le premier vecteur
            dict2 (dict) : le deuxième vecteur

        Returns :
            dot_product (float) : Le produit scalaire normalisé de deux vecteurs

        Copyright 2023, F. Mailhot et Université de Sherbrooke
        """
        # Changer valeurs et clés

        new_dict1 = {}
        new_dict2 = {}

        for key, values in dict1.items():
            for ngram in values:
                new_dict1[ngram] = key

        for key, values in dict2.items():
            for ngram in values:
                new_dict2[ngram] = key

        # Calculer le produit scalaire

        fusion_cles = tuple(new_dict1.keys() & new_dict2.keys())

        produit = sum(new_dict1[ngram] * new_dict2[ngram] for ngram in fusion_cles)

        # Calculer les normes

        norme_vecteur1 = math.sqrt(sum(value ** 2 for value in new_dict1.values()))
        norme_vecteur2 = math.sqrt(sum(value ** 2 for value in new_dict2.values()))

        # Diviser le produit scalaire par le produit des normes
        dot_product = produit / (norme_vecteur1 * norme_vecteur2)

        return dot_product

    def dot_product_aut(self, auteur1: str, auteur2: str) -> float:
        """Calcule le produit scalaire normalisé entre les oeuvres de deux auteurs, en utilisant dot_product_dict()

        Args :
            auteur1 (str) : le nom du premier auteur
            auteur2 (str) : le nom du deuxième auteur

        Returns :
            dot_product (float) : Le produit scalaire normalisé des n-grammes de deux auteurs

        Copyright 2023, F. Mailhot et Université de Sherbrooke
        """

        # Les lignes qui suivent ne servent qu'à éliminer un avertissement.
        # Il faut les retirer et les remplacer par du code fonctionnel

        dot_product = self.dot_product_dict(self.compte_mots[auteur1], self.compte_mots[auteur2])

        return dot_product

    def dot_product_dict_aut(self, dict_oeuvre: dict, auteur: str) -> float:
        """Calcule le produit scalaire normalisé entre une oeuvre inconnue et les oeuvres d'un auteur,
           en utilisant dot_product_dict()

        Args :
            dict_oeuvre (dict) : la liste des n-grammes d'une oeuvre inconnue
            auteur (str) : le nom d'un auteur

        Returns :
            dot_product (float) : Le produit scalaire normalisé des n-grammes de deux auteurs

        Copyright 2023, F. Mailhot et Université de Sherbrooke
        """

        # TODO Les lignes qui suivent ne servent qu'à éliminer un avertissement.
        # TODO Il faut les retirer et les remplacer par du code fonctionnel

        dot_product = self.dot_product_dict(dict_oeuvre, self.compte_mots[auteur])

        return dot_product

    def find_author(self, oeuvre: str) -> []:
        """Après analyse des textes d'auteurs connus, retourner la liste d'auteurs
            et le niveau de proximité (un nombre entre 0 et 1) de l'oeuvre inconnue
            avec les écrits de chacun d'entre eux

        Args :
            oeuvre (str) : Nom du fichier contenant l'oeuvre d'un auteur inconnu

        Returns :
            resultats (Liste[(string, float)]) : Liste de tuples (auteurs, niveau de proximité),
            où la proximité est un nombre entre 0 et 1)
        """

        resultats = 0

        self.analyze()

        for auteur in self.auteurs:
            resultats = self.dot_product_dict(self.oeuvre, self.compte_mots[auteur])

        return resultats

    def gen_text_all(self, taille: int, textname: str) -> None:
        """Après analyse des textes d'auteurs connus, produire un texte selon des statistiques de l'ensemble des auteurs

        Args :
            taille (int) : Taille du texte à générer
            textname (str) : Nom du fichier texte à générer.

        Returns :
            void : ne retourne rien, le texte produit doit être écrit dans le fichier "textname"
        """

        # Ce print ne sert qu'à éliminer un avertissement. Il doit être retiré lorsque le code est complété
        print(self.auteurs, taille, textname)

        return

    def gen_text_auteur(self, auteur: str, taille: int, textname: str) -> None:
        """Après analyse des textes d'auteurs connus, produire un texte selon des statistiques d'un auteur

        Args :
            auteur (str) : Nom de l'auteur à utiliser
            taille (int) : Taille du texte à générer
            textname (str) : Nom du fichier texte à générer.

        Returns :
            void : ne retourne rien, le texte produit doit être écrit dans le fichier "textname"
        """

        # Ce print ne sert qu'à éliminer un avertissement. Il doit être retiré lorsque le code est complété
        print(self.auteurs, auteur, taille, textname)

        return

    def get_nth_element(self, auteur: str, n: int) -> [[str]]:
        """Après analyse des textes d'auteurs connus, retourner le k-ième plus fréquent n-gramme de l'auteur indiqué

        Args :
            auteur (str) : Nom de l'auteur à utiliser
            n (int) : Indice du n-gramme à retourner

        Returns :
            ngram (List[Liste[string]]) : Liste de liste de mots composant le n-gramme recherché
            (il est possible qu'il y ait plus d'un n-gramme au même rang)
        """

        liste_ordonne = list(self.compte_mots[auteur].keys())  # fait une liste des occurences
        liste_ordonne.sort(reverse=True)    # classe les occurences en ordre decroissant
        nth_element = self.compte_mots[auteur][liste_ordonne[n-1]]  # valeur a l'index
        return nth_element

    def analyze(self) -> None:
        """Fait l'analyse des textes fournis, en traitant chaque oeuvre de chaque auteur

        Args :
            void : toute l'information est contenue dans l'objet TextAn

        Returns :
            void : ne retourne rien, toute l'information extraite est conservée dans des structures internes
        """

        # TODO Ajouter votre code ici pour traiter l'ensemble des oeuvres de l'ensemble des auteurs
        # TODO Pour l'analyse :  faire le calcul des fréquences de n-grammes pour l'ensemble des oeuvres
        # TODO   d'un certain auteur, sans distinction des oeuvres individuelles,
        # TODO       et recommencer ce calcul pour chacun des auteurs
        # TODO   En procédant ainsi, les oeuvres comprenant plus de mots auront un impact plus grand sur
        # TODO   les statistiques globales d'un auteur.

        pattern = "|".join(map(re.escape, [char for char in self.PONC]))  # expression reguliere pour les caracteres

        for auteur in self.auteurs:
            for fichier in self.get_aut_files(auteur):
                with open(fichier, "r", encoding="utf-8") as texte:
                    mots_precedents = []
                    for line in texte:
                        line = line.lower()  # mets les lignes en minuscules

                        if self.keep_ponc:  # regarde si keep_ponc est True
                            line = re.split(f'({pattern})', line)  # separe les lignes avec le pattern
                        else:
                            line = re.split(f'({pattern})', line)

                        line = [word.strip() for word in line if word.strip()]  # enleve les espaces des mots
                        line = [word.split() for word in line if word.split()]  # separe chaque mots dans une liste
                        line = [word for sublist in line for word in sublist]  # remplace chaque liste par ses éléments

                        if self.remove_word_1:  # enlever les mots de 1 lettre
                            line = [word for word in line if len(word) != 1]
                        if self.remove_word_2:  # enlever les mots de 2 lettres
                            line = [word for word in line if len(word) != 2]

                        # Indexation des mots
                        mots = mots_precedents + line  # ajoute les mots à la liste des mots precedents

                        for i in range((len(mots) - self.ngram)):
                            prefix = tuple(mots[i:i + self.ngram])  # initialise le prefix
                            suffix = mots[i + self.ngram]  # initialise le suffixe

                            if prefix in self.mots_auteurs[auteur]:  # si le suffixe existe, ajouter a au dictionnaire
                                self.mots_auteurs[auteur][prefix].append(suffix)
                            else:  # sinon cree l'entree avec le prefix
                                self.mots_auteurs[auteur][prefix] = [suffix]

                        mots_precedents = line[-self.ngram:]

            # Compte le nombre d'occurence des ngrammes
            self.compte_mots[auteur] = {}
            for ngram in self.mots_auteurs[auteur]:
                # self.compte_mots[auteur][ngram] = len(self.mots_auteurs[auteur][ngram]) # Ancienne façon
                occurence = len(self.mots_auteurs[auteur][ngram])  # nombres d'occurences d'un ngramme

                # verification si l'occurence existe deja, ajoute a la liste
                if occurence in self.compte_mots[auteur]:
                    self.compte_mots[auteur][occurence].append(ngram)
                # sinon, cree la valeur
                else:
                    self.compte_mots[auteur][occurence] = [ngram]

        return
