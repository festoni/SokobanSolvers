# SokobanSolvers

Language : Python3

SokobanSolvers is a set of solvers for the puzzle game Sokoban. An example version of the game, Pufiban, can be played online [here](https://www.sokobanonline.com/play/web-archive/jordi-domenech/pufiban). 

The solvers use different graph searching algorithms like Best First Search, A-star search with heuristics, and Branch and Bound. Each implementation also has an optimized copy using ranking and unranking of graph states. 

The levels are represented in text format using the following convention found [here](http://sokobano.de/wiki/index.php?title=Level_format). You can write your own level as per the convention, or use the example levels provided in the 'levels' folder, and use them as described below.

The output of the algorithms is length of the path to the shortest solution. If the verbose paramater is set to true, then the actual path to the shortest solution is also printed.

sokoban_solvers.py is the main file showcasing all the searches. This file and
all other individual search files take input as STDIN or as an argument

Usage: Any of following three methods of loading a level work:

  `python sokoban_solvers.py levels/5.txt`

  `python sokoban_solvers.py < levels/5.txt`

  `cat levels/5.txt | python sokoban_solvers.py`

This project is avaliable through git via:
- SSH: git@src-code.simons-rock.edu:fkastrati13/SokobanSolvers.git
- HTTPS: https://src-code.simons-rock.edu/git/fkastrati13/SokobanSolvers.git
