# IBM Ponder This - April 2024 Challenge

Challenge: [Simultaneous Towers of Hanoi](https://research.ibm.com/haifa/ponderthis/challenges/April2024.html) <br>
My Solution: [Code](april_2024.py)


## Solution
Solution: `16511310` <br>
Bonus: `1169723214`


## General Idea
The winning steps of each game are cyclic. For each game, we need to find all the winning steps in the first cycle and the period of the cycle to know all the possible winning steps.
Each winning step is `phase + period * k`, where `k=0,1,2,..` and `phase` is a winning step in the first cycle.
For each game, we will have a list of `(phase, period)` that represent all the winning steps of the game.

Once we find all the winning steps of two games, we compare each winning step from one game with all the winning steps of the second game and find all the synchronized wins of the games.
A synchronized win will also be in the format `phase + period * k`, and all the synchronized wins between the games will also be a list of `(phase, period)`. 
The solution for two games will be the minimum phase in this list.

To find the synchronized wins with a third game, we repeat the process - we compare the winning steps of the third game with the list we found in the previous step. 
This will give us a list of all the synchronized wins between the three games. The solution will be the minimum phase in this list.


## Run Code
```
❯ python april_2024.py [-g] games_input_file

    -g: the input games file name
```

### Examples

- Run the code with default arguments: <br>
(`g=challenge`)
```bash
❯ python april_2024.py
```

- Run the code with the bonus game: <br>
```bash
❯ python april_2024.py -g bonus
```
