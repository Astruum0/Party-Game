# Party-Game

YDAY Algo 2020-2021.

Party-game est un sorte de groupe de mini-jeux où le joueur s'affronte avec un bot ayant une difficulté que le joueur à défini en lancant le jeu.

Ce projet propose 4 mini-jeux:

- Puissance 4
- Bataille Navale
- Flappy Bird
- Dots & Box

Le joueur à le choix entre 3 niveaux de difficultés pour chacun des jeux.

# Installation

Dans le dossier racine du projet, faites cette commande:

```
pip install -r requirements.txt
```

# Lancement

Pour lancer le projet, faites

```
python launcher.py
```

# Jeu 1 : Puissance 4

![Puissance 4](https://i.imgur.com/gK16uGa.png)

A tour de rôle, chaque joueur doit placer un jeton dans la colonne qu'il souhaite, le joueur gagne lorsqu'il arrive à aligner 4 de ses jetons que ce soit horizontalement, verticalement ou en diagonale.

# Jeu 2 : Bataille Navale

![Bataille Navale](https://i.imgur.com/XJQArvh.png)

La bataille Navale est un jeu où deux joueurs doivent placer des « navires » sur une grille tenue secrète et tenter de « toucher » les navires adverses. Le gagnant est celui qui parvient à couler tous les navires de l'adversaire avant que tous les siens ne le soient. On dit qu'un navire est coulé si chacune de ses cases a été touchées par un coup de l'adversaire.

Chaque joueur possède les mêmes navires, dont le nombre et le type sont les suivantes:

- Porte-avions (5 cases)
- Croiseur (4 cases)
- Contre-torpilleurs (3 cases)
- Torpilleur (2 cases)

# Jeu 3 : Flappy Bird

![Flappy Bird](https://i.imgur.com/ePI2ayk.png)

Flappy Bird est un jeu à la base jouable en solo : le but est de passer à travers des tuyaux en controlant un oiseau et d'aller le plus loin possible.
Dans le cadre d'un jeu en multijoueur, le but est d'aller plus loin que l'adversaire pour gagner.

# Jeu 4 : Dots & Box

A tour de rôle, chaque joueur doit relier 2 points entre eux, le joueur remporte un point lorsqu'il complete un carré en tracant la dernière ligne, il peut ainsi rejouer. La partie se termine quand tous les points sont reliés entre eux.
