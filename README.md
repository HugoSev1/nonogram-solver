# EN

⚠️**Disclaimer**⚠️: This project is only a personal passion project, the goal isn't to be perfectly optiimzed. I made this project for a Youtube video (in French, my native language) inspired by what other people such as Code Bullet have done for other games. Note that not everything is fully optimized, that some functions may be outdated by other similar and more effective functions, and that errors may occur.

I put the source code here for curious people because it doesn't cost anything to do it. But if you want to use it, here's what you should know (don't hesitate to tell if you find any issue, preferably with a screenshot of the board including the blue square around the board), or fork if you want to make it better or do whatever you want):

First, on the website, there's 5x5, 10x10, 15x15, 20x20 and 25x25 games. There's also a daily 30x25 game, a weekly 30x30 game as well as a 50x50 monthly game.

To debug and use the program, I use VSCode. There's a few variables and controls to use the program.
1. In solver.py (which mainly contains the code for the Pygame part), there's a few variables:
   * **is_pygame_used** : If True, then we use the Pygame part (more convenient for larger boards such as the monthly 50x50)
   * **double_check_line** : If True, then another Pygame window will open where we can click on a line to change its content (when the character detection isn't right, which happens more often for larger boards)
   * **use_save_file** : If True, then a save folder will be used for the board and the lines (useful for larger games in case of mistakes or if there's an issue with the program)
   * **end_char** : Character to use after entering the numbers when typing the lines to change while double-checking
   * **pygame_width** : Level of zoom of the grid by default with Pygame (can be changed with the **+** and **-** keys)
   * **is_tile_found** : If True and followed by a **break** statement at both points where it's applied (for T and F), then this loop stops
2. In nonoSolvFunc.py which contains most of the functions that solve the game, there's spacing_threshold that we can change: this variable helps to make the difference between numbers such as a 1 followed by a 2 (1 2 / one then two) compared to a 12 (twelve)
3. Controls in Pygame:
   * **R**: Runs repeatSolve() which runs every relative function (i.e. except the beginning which doesnt' take the tiles that are already on the board into account, as there's none when the game starts)
   * **T**: Checks each tile that isn't filled, and replaces it when it's impossible (i.e. replaces a black tile by a cross, and vice-versa). ⚠️**This can take up to several minutes, especially on larger boards that are barely filled**⚠️
   * **←** and **→**: Uses the previous or next save (similar to a Ctrl + Z / Ctrl + Y to Undo / Redo)
   * **↑** and **↓**: Zoom in / Zoom out
   * **S** and **L**: Save (**S**) / Load (**L**) a savestate
   * **H**: Highlights the lines for the case on which the mouse cursor is standing
   * **P**: Places the tiles in-game in the browser (The same spot / zoom must be used since the program has been run)
4. More info:
   * In the variable game_board, a **T** (for True) corresponds to a black tile, an **F** (for False) corresponds to a cross, which is represented by a red square in Pygame, and finally a **0** corresponds to a tile that hasn't been filled yet. In some functions, this 0 may be temporarily changed to another number, then switched back to either a T, an F or a 0 in this same function.
   * When you launch the program, make sure that the blue square around the board is entirely present, as it is used to detect where the board is located.

📽️Video link ➡️ https://youtu.be/0wWwbnne4ho

🎮Game link ➡️ https://www.puzzle-nonograms.com

# FR

⚠️**Disclaimer**⚠️ : Ce projet est uniquement un projet personnel de passion, le but n'est pas d'être le plus optimal pour faire le travail. Il s'agit d'un projet fait pour ma vidéo Youtube inspirée de ce qu'ont fait d'autres personnes comme Code Bullet sur d'autres jeux. Notez que tout n'est pas parfaitement optimisé, que certaines fonctions sont peut-être obsolètes par d'autres fonctions similaires et plus efficaces et que des erreurs peuvent survenir.

Je mets le code source ici pour les curieux parce que ça me coûte rien de le faire. Mais si vous voulez l'utiliser, voici ce qu'il y a à savoir (et n'hésitez pas à dire si vous trouvez des problèmes, de préférence avec une capture d'écran de la game qui inclue le carré bleu autour, ou à fork si vous le souhaitez pour l'améliorer ou faire ce que vous voulez) :

D'abord, sur le site, il y a des games de 5x5, 10x10, 15x15, 20x20 et 25x25. Il y a également une game quotidienne en 30x25, une game hebdomadaire en 30x30, ainsi qu'une game de 50x50 mensuelle.

Pour debug et utiliser le programme, j'utilise VSCode. Il y a quelques variables et contrôles pour utiliser le programme.
1. Dans solver.py (qui contient le code pour la partie avec Pygame principalement), il y a quelques variables :
   * **is_pygame_used** : Si True, alors on passe par la partie Pygame (plus pratique pour les grilles plus grandes comme le 50x50 mensuel)
   * **double_check_line** : Si True, alors une autre fenêtre de Pygame s'ouvre où on peut cliquer sur une ligne pour y modifier le contenu (lorsque la détection de caractères n'est pas correcte, ce qui est plus fréquent pour de plus grandes grilles)
   * **use_save_file** : Si True, alors un dossier de sauvegarde sera utilisé pour la grille et les lignes (utile pour les plus grandes games en cas d'erreur ou de problème avec le programme)
   * **end_char** : Caractère à utiliser après avoir entré les nombres lors de la saisie des lignes à modifier dans le double-check
   * **pygame_width** : niveau de zoom de la grille par défaut sur Pygame (modifiable avec les touches **+** et **-**)
   * **is_tile_found** : Si True puis suivie d'un **break** aux deux applications (pour T et F), alors cette boucle s'arrête
2. Dans nonoSolvFunc.py qui contient la plupart des fonctions qui résoudent la game, il y a spacing_threshold qui est modifiable : cette variable permet de différencier des nombres tels qu'un 1 suivi d'un 2 (1 2 / un puis deux) comparé à un 12 (douze)
3. Les contrôles dans Pygame :
   * **R** : Lance repeatSolve() qui exécute toutes les fonctions dites relatives (i.e. à part le tout début qui est indépendant des cases déjà cochées puisqu'aucune ne l'est lorsque la partie commence)
   * **T** : Coche chaque case non-remplie de la grille, puis la remplace si c'est impossible (i.e. remplace une case cochée en noir par une croix, et vice-versa). ⚠️**Ceci peut prendre jusqu'à plusieurs minutes, surtout avec de grandes grilles peu remplies**⚠️
   * **←** et **→** : Utilise la sauvegarde précédente ou suivante (similaire à un Ctrl + Z / Ctrl + Y pour annuler / refaire)
   * **↑** et **↓** : Zoom ou dézoom
   * **S** et **L** : Sauvegarde (**S**) / Charge (**L**) une savestate
   * **H** : Surligne les lignes de la case sur laquelle le curseur de la souris se situe
   * **P** : Place les cases dans le jeu dans le navigateur (Le même emplacement / zoom doit être conservé depuis que le programme a été lancé)
4. Infos supplémentaires :
   * Dans la variable game_board, un **T** (pour True, soit Vrai en français) correspond aux cases cochées en noir, un **F** (pour False, soit Faux en français) correspond à une croix, qui est représentée par un carré rouge dans Pygame, et enfin un *0** correspond aux cases qui ne sont pas encore remplies. Dans certaines fonctions, ce 0 est parfois temporairement changé en un autre nombre, puis changé en soit un T, soit un F, soit un 0 dans cette même fonction.
   * Lorsque vous lancez le programme, assurez-vous que le carré bleu autour de la grille est entièrement présent, car il est utilisé pour détecter ou se situe la grille.

📽️Lien de la vidéo ➡️ https://youtu.be/0wWwbnne4ho

🎮Lien du site du jeu ➡️ https://www.puzzle-nonograms.com
