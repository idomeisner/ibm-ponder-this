"""
IBM Ponder This - April 2024 Challenge

Solution:
16511310

Bonus:
1169723214
"""

from copy import deepcopy
from time import time
from typing import Any, Dict, List

Hanoi = Dict[int, List[Any]]


def print_hanoi(hanoi: Hanoi):
    """
    Print the Hanoi tower
    """

    hanoi_copy: Hanoi = deepcopy(hanoi)

    # Find the maximal number of disks located on a single rod
    max_len = len(max(hanoi_copy.values(), key=lambda x: len(x)))

    # Pad the rods with " " so all the rods will contain lists with the same length
    for rod in hanoi_copy.values():
        if len(rod) < max_len:
            lst: List[str] = [" "] * (max_len - len(rod))
            rod.extend(lst)

    # Print the Hanoi tower
    for _ in range(max_len - 1):
        for rod in hanoi_copy.values():
            print(rod.pop(), " ", end="")
        print()

    print("_  _  _")


def build_hanoi(n: int) -> Hanoi:
    """
    Build the initial Hanoi tower
    We set the first disk in each rod to 'inf' so we won't be able to move it
    """

    rods = {
        0: [float("inf")] + list(range(n, 0, -1)),
        1: [float("inf")],
        2: [float("inf")]
    }

    return rods


def find_winning_states(n: int, moves: str, number_of_wins: int = 10000) -> List[int]:
    """
    Finds winning states steps by moving the disks in the Hanoi tower according to the provided
    moves sequence until we find a win. 'number_of_wins' is the stop condition of the function,
    we return the found winning states steps only when we find 'number_of_wins' wins.

    At any point we can call the function 'print_hanoi(hanoi)', to print the current Hanoi tower for debug purposes.

    :param n: Number of disks in the Hanoi tower
    :param moves: The movement sequence of the disks
    :param number_of_wins: Number of wins we want to find before exiting the function
    :return: A list of length 'number_of_wins' with all the states that considered wins
    """

    hanoi = build_hanoi(n)
    disk_one = 0
    step = -1
    wins = []

    while True:
        for c in moves:
            step += 1

            # if all disks are located in rod "1" we found a winning state
            if len(hanoi[0]) == 1 and len(hanoi[2]) == 1:
                wins.append(step)
                if len(wins) == number_of_wins:
                    return wins

            # update the location of disk "1"
            if c == "0":
                hanoi[disk_one].pop()
                new_rod = (disk_one + 1) % 3
                hanoi[new_rod].append(1)
                disk_one = new_rod

            # update the location of disk "1"
            elif c == "1":
                hanoi[disk_one].pop()
                new_rod = (disk_one + 2) % 3
                hanoi[new_rod].append(1)
                disk_one = new_rod

            # dealing with the case: "Take a disk which is not "1" and move it to another rod"
            else:
                rod1_idx = (disk_one + 1) % 3
                rod2_idx = (disk_one + 2) % 3

                rod1 = hanoi[rod1_idx]
                rod2 = hanoi[rod2_idx]

                # determine which disk to move
                if rod1[-1] > rod2[-1]:
                    rod1.append(rod2.pop())

                elif rod1[-1] < rod2[-1]:
                    rod2.append(rod1.pop())


def min_synced_winning_step(winning_states_all: List[List[int]]) -> int:
    """
    Find the minimal number of steps at which all games reach a winning state at the same time.

    :param winning_states_all: List of lists. Each list contains the steps required to reach a winning state of each game.
    :return: The minimal number of steps at which all games reach a winning state at the same time.
             If no such step exists, return -1.
    """

    min_step = -1
    synced_wins = set(winning_states_all[0])

    for winning_states in winning_states_all[1:]:
        synced_wins &= set(winning_states)

    try:
        min_step = min(synced_wins)
    except ValueError:
        print("Minimal synced winning state step not found, try increasing the value of 'number_of_wins'")

    return min_step


def main():
    game1 = {
        "n": 7,
        "moves": "12021121120020211202121"
    }
    game2 = {
        "n": 10,
        "moves": "0211202112002"
    }
    game3 = {
        "n": 9,
        "moves": "20202020021212121121202120200202002121120202112021120020021120211211202002112021120211200212112020212120211"
    }

    start = time()

    games = [game1, game2]
    # games = [game1, game2, game3]
    winning_states_all = [find_winning_states(**game) for game in games]
    result = min_synced_winning_step(winning_states_all)

    end = time()

    print(f"Solution: {result}")
    print(f"Total time = {end - start}")


if __name__ == "__main__":
    main()
