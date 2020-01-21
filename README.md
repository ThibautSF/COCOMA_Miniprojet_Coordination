# COCOMA Miniprojet Coordination & Allocation de ressources

Le mini-projet consiste simplement à produire un notebook qui permettra d'illustrer deux protocoles pour la coordination à base d'enchères:

- les protocoles SSI (version classique et regret)

- le protocole CBAA (version simple: une seule ressource par agent). Pour ce protocole, on implémentera bien sûr une version synchrone, avec une alternance de tours au cours desquels les agents (1) font des offres et modifie éventuellement l'objet qu'il (pense) obtenir, et (2) échangent les messages avec les vecteurs de prix. A la fin du tour l'aggrégation de tous les messages reçus par les voisins est réalisée.

On s'inspirera de la fiche exemple donnée en pdf. Pour les deux protocoles, les agents/robots doivent être situés sur un graphe, dont les arcs sont valués (distance), ou encore sur une grille, en utilisant la distance de Manhattan (dans ce cas, vous pourrez supposer que les agents ont un rayon de communication limitée dans le cas de CBAA).

Le notebook devra permettre d'illustrer le fonctionnement des deux protocoles, pour un nombre d'agents quelconque. Vous pourrez produire quelques tests sur des répartitions ou des topologies différentes. 

Questions posées:

* CBAA est présenté avec des utilités à maximiser. Technique classique pour passer des coûts à des utilités: calcul d'un chemin total qui passe par tous les sites, disons MAX (pas nécessaire qu'il soit optimal, mais le même pour tous les agents par contre). Les utilités des agents sont ensuite: MAX - coût(chemin). Notez que dans CBAA chaque agent ne reçoit qu'un objet. Dans ce cas, le MAX peut simplement être la valeur la distance max entre n'importe quel agent et n'importe quel site...

Rendu: notebook (et code associé si besoin), le vendredi 24 Janvier 23:59. 
