"""
IBM Ponder This - April 2024 Challenge

Solution:
16511310

Bonus:
1169723214
"""

from copy import deepcopy
from time import time
from typing import Any, Dict, List, Tuple

from sympy.ntheory.modular import crt

HanoiTower = Dict[int, List[Any]]
WinningSteps = Dict[str, int | List[int]]
GeneralWin = Tuple[int, int]  # represent a general winning step and its repetitions: 'winning_step + period * k'


class Hanoi:
    def __init__(self, n: int, moves: str):
        self.disks: int = n
        self.moves: str = moves
        self._disk_1_location: int = 0
        self._winning_steps: WinningSteps = {}
        self.hanoi: HanoiTower = self.build_hanoi(n)

    @staticmethod
    def build_hanoi(n: int) -> HanoiTower:
        """
        Build the initial Hanoi tower
        We set the first disk in each rod to 'inf' so we won't be able to move it
        """

        hanoi = {
            0: [float("inf")] + list(range(n, 1, -1)),
            1: [float("inf")],
            2: [float("inf")],
        }

        return hanoi

    def print_hanoi(self) -> None:
        """
        Print the Hanoi tower
        """

        hanoi_copy: HanoiTower = deepcopy(self.hanoi)
        hanoi_copy[self._disk_1_location].append(1)

        # Find the maximal number of disks located on a single rod
        max_len = len(max(hanoi_copy.values(), key=lambda x: len(x)))

        # Pad the rods with " " so all the rods will contain lists with the same length
        for rod in hanoi_copy.values():
            if len(rod) < max_len:
                none_disks: List[str] = [" "] * (max_len - len(rod))
                rod.extend(none_disks)

        # Print the Hanoi tower
        for _ in range(max_len - 1):
            for rod in hanoi_copy.values():
                print(rod.pop(), " ", end="")
            print()

        print("_  _  _")

    def reset(self) -> None:
        """
        Reset the Hanoi tower to default values
        """

        self.hanoi = self.build_hanoi(self.disks)
        self._winning_steps = {}
        self._disk_1_location = 0

    @property
    def winning_steps(self):
        """
        Return the winning steps of the Hanoi tower.
        If the _winning_steps variable is empty, it calculates it and sets it.
        """

        if not self._winning_steps:
            self._winning_steps = self._find_winning_steps()

        return self._winning_steps

    def _find_winning_steps(self) -> WinningSteps:
        """
        Find all the winning steps of a game.

        Since the winning steps are cyclic, it is enough to find all the winning steps in a single cycle
        and the cycle size (period).

        Each winning step is represented by:
        phases + period * k, where k is 0,1,2,...
        Where 'phase' is a winning step and 'period' represents how many more steps we will reach a winning state again.

        The structure of WinningSteps:
        WinningSteps = {
            period: int,
            phases: List[int]
        }

        At any point we can call the function 'print_hanoi(hanoi)', to print the current Hanoi tower for debug purposes.
        """

        hanoi = self.hanoi
        step = -1
        winning_steps: List[int] = []
        moves_len = len(self.moves)
        moves_list = list(map(lambda x: int(x) + 1, self.moves))  # shift the moves by 1 and make it a list of ints
        stop_condition = self.disks  # all the disks on a single rod (except from disk "1")
        winning_moves = set()  # store all indices of the moves that belong to a winning states

        while True:
            for move in moves_list:
                step += 1

                # if all disks are located in rod "1" we found a winning state
                if len(hanoi[1]) == stop_condition and self._disk_1_location == 1:
                    r = step % moves_len

                    # if r is in winning_moves we are starting a new winning cycle, so we can stop
                    if r in winning_moves:
                        return {
                            "period": step - winning_steps[0],
                            "phases": winning_steps
                        }

                    winning_moves.add(r)
                    winning_steps.append(step)

                # dealing with the case: "Take a disk which is not "1" and move it to another rod"
                if move == 3:
                    rod1_idx = (self._disk_1_location + 1) % 3
                    rod2_idx = (self._disk_1_location + 2) % 3

                    rod1 = hanoi[rod1_idx]
                    rod2 = hanoi[rod2_idx]

                    # determine which disk to move
                    if rod1[-1] > rod2[-1]:
                        rod1.append(rod2.pop())

                    elif rod1[-1] < rod2[-1]:
                        rod2.append(rod1.pop())

                # update the location of disk "1"
                else:
                    self._disk_1_location = (self._disk_1_location + move) % 3


def combine_phased_rotations(
    a_period: int, a_phase: int, b_period: int, b_phase: int
) -> Tuple[int, int] | None:
    """
    Combine two phased rotations into a single phased rotation

    Returns: combined_period, combined_phase

    The combined rotation is at its reference point if and only if both a and b
    are at their reference points.

    Reference:
        https://math.stackexchange.com/a/3864593
    """

    gcd, s, t = extended_gcd(a_period, b_period)
    phase_difference = a_phase - b_phase
    pd_mult, pd_remainder = divmod(phase_difference, gcd)

    if pd_remainder:
        return None

    combined_period = a_period // gcd * b_period
    combined_phase = (a_phase - s * pd_mult * a_period) % combined_period

    return combined_period, combined_phase


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Greatest Common Divisor Algorithm

    Returns:
        gcd: The greatest common divisor of a and b.
        s, t: Coefficients such that s*a + t*b = gcd

    Reference:
        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
    """

    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def find_synced_wins(
        winning_steps1: List[GeneralWin], winning_steps2: List[GeneralWin]
) -> List[GeneralWin]:
    """
    The function gets the winning steps of 2 games and finds all the synced wins of these games.

    Each GeneralWin is of the form (period, phase), which represents: winning_step + period * k

    The result is:
    [(period1, phase1), (period2, phase2), (period3, phase3), ...]

    """

    res = []

    for period1, phase1 in winning_steps1:
        for period2, phase2 in winning_steps2:
            if period_phase := combine_phased_rotations(period1, phase1, period2, phase2):
                res.append(period_phase)

            # We can alternatively use the crt (chinese remainder theorem) function from the sympy package
            # to obtain the combined period and phase
            # if phase_period := crt([period2, period1], [phase2, phase1]):
            #     res.append((phase_period[1], phase_period[0]))

    return res


def min_synced_winning_step(games) -> int:
    """
    The function receive a list of games and return the minimal number of steps.
    at which all games reach a winning state at the same time.
    If no such step exists, return -1.
    """

    curr = [(1, 1)]

    for game in games:
        hanoi = Hanoi(**game)
        wins = hanoi.winning_steps

        # Create a list of winning steps, e.g.: [(period1, phase1), (period2, phase2), ...]
        phases = wins["phases"]
        periods = [wins["period"]] * len(phases)
        periods_phases = list(zip(periods, phases))

        curr = find_synced_wins(periods_phases, curr)

    return -1 if not curr else min(curr, key=lambda x: x[1])[1]


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
        "moves": "20202020021212121121202120200202002121120202112021120020021120211211202002112021120211200212112020212120211",
    }

    start = time()

    # games = [game1, game2]
    games = [game1, game2, game3]
    result = min_synced_winning_step(games)

    end = time()

    print(f"Solution: {result}")
    print(f"Total time = {end - start} seconds")


if __name__ == "__main__":
    main()
