# DiceIO

DiceIO est un lanceur de dés (dice roller) implémenté en Python pur avec les modules `regex` et `random`.

# Guide de l'utilisateur

## Lancer des dés (Classique)

Pour lancer un seul dé à X faces, utilisez la commande `dX` (par exemple `d6` pour un dé à six faces).
La somme des dés sera affichée en premier, puis le résultat individuel de chaque dé séparé par une virgule.
La commande ci-dessus pourrait donner par exemple :
```
# 5
5
```

Si vous voulez lancer plus d'un seul dé, spécifiez-le en ajoutant un nombre avant le `d` (par exemple `5d20` pour cinq dés à vingt faces chacun). Exemple de résultat :
```
# 48
7, 14, 3, 5, 19
```

## Dés explosifs

Pour lancer des dés explosifs, utilisez la commande `eX` à la place de `dX`. Un dé explosif est relancé tant qu'il obtient sa valeur maximale, et les nouveaux résultats sont ajoutés. Par exemple, pour `2e6` :
```
# 18
4, 6, 6, 2
```

## Ajouter / Soustraire des dés ou des constantes

Il est possible d'ajouter / soustraire un nombre fixe à la somme totale, pour cela rien de plus simple, rajoutez un signe d'addition / soustraction puis le nombre constant. Par exemple `d20+4`:
```
# 15
11
```
Notez que le `4` n'est pas présent dans les résultats des dés, il est seulement ajouté à la somme.

Vous pouvez également réaliser ces opérations entre des dés. Par exemple `d20-d6` :
```
# 6
14, 1, 5, 2
```

Calculer avec uniquement des nombres constants est aussi possible. Par exemple `30-7+8`.

## Options de lancer

Vous pouvez ajouter des options de tri, de sélection ou de filtrage directement à la suite de vos lancers de dés :

- **Trier les dés (`s`)** :
  Ajoutez un `s` pour trier les résultats. Par exemple `5d20s` :
  ```
  # 55
  3, 5, 7, 14, 19
  ```

- **Garder des dés (`k`)** :
  Ajoutez un `k` suivi d'un nombre pour ne conserver que les dés les plus élevés ou les plus bas.
  - `4d6k3` : Lance 4 dés à 6 faces et garde les 3 plus élevés.
  - `4d6k-2` : Lance 4 dés à 6 faces et garde les 2 plus bas.

- **Filtrer les résultats (`[ ]`)** :
  Ajoutez `[ ]` contenant une condition pour ne garder que les dés qui la respectent.
  Les opérateurs disponibles sont `>`, `<`, `=`, et `!`.
  - `5d10[>5]` : Lance 5 dés à 10 faces et ne garde que les résultats strictement supérieurs à 5.
  - `4d6[!1]` : Lance 4 dés à 6 faces et ignore tous les 1.

## Tirer au sort dans une liste (Choix)

DiceIO permet de tirer au sort parmi plusieurs choix, séparés par des virgules. Un espace est requis après la commande.

- **Choix avec remise (`l` - classique)** :
  Tire un ou plusieurs éléments qui peuvent être choisis plusieurs fois.
  Syntaxe : `<nombre>l <choix1>, <choix2>, ...`
  Exemple `2l Pile, Face` :
  ```
  Pile, Pile
  ```

- **Choix sans remise (`u` - unique)** :
  Tire un ou plusieurs éléments uniques (ils ne peuvent pas être choisis plusieurs fois).
  Syntaxe : `<nombre>u <choix1>, <choix2>, ...`
  Exemple `3u Guerrier, Mage, Voleur, Clerc` :
  ```
  Voleur, Guerrier, Mage
  ```

## Mode Shadowrun

DiceIO dispose d'un mode spécifique pour le jeu de rôle *Shadowrun*.
Tapez la commande `sr` pour activer ou désactiver ce mode.
Lorsqu'il est activé, un simple lancer de dés à 6 faces sans options (comme `5d6`) affichera des statistiques utiles spécifiques à Shadowrun au lieu du résultat classique :
```
Nombre de 6   : 1
Nombre de 5/6 : 3
Nombre de 1   : 0
```