# DiceIO

DiceIO est lanceur de dès (dice roller) implémenté en Python pure avec le module `regex` et `random`.

# Guide de l'utilisateur

## Les bases

Pour lancer un seul dès à X face, utilisez la commande `dX` (par exemple `d6` pour un dès à six faces).
La somme des dès sera affichée en premier, puis le résultat individuel de chaque dès séparé par une virgule.
La commande ci-dessus pourrait donner par exemple :
```
# 5
6
```

Si vous voulez lancer plus d'un seul dès, spécifiez-le en ajoutant un nombre avant le `d` (par exemple `5d20` pour cinq dès à vingt faces chacun). Exemple de résultat :
```
# 48
7, 14, 3, 5, 19
```

## Ajouter / Soustraire des dès ou des constantes

Il est possible d'ajouter / soustraire un nombre fixe à la somme totale, pour cela rien de plus simple, rajouter un signe d'addition / soustraction puis le nombre constant. Par exemple `d20+4`:
```
# 15
11
```
Notez que le `4` n'est pas présent dans les dès, il est seulement ajouté à la somme.

Vous pouvez également réaliser ces opérations entre des dès. Par exemple `d20-d6` :
```
# 6
14, 1, 5, 2
```

Calculer avec uniquement des nombres constants est aussi possible. Par exemple `30-7+8`.

## Ordonner les dès
Mettez un `s` pour trier le résultat