"""
IBM Ponder This - March 2024 Challenge

Solutions:
X_1000 = 115192665
X_2024 = 117778830159

Packages installed: numpy, gmpy2
"""

import argparse
import time

import numpy as np
from gmpy2 import is_prime


def get_primes_till_n(n: int) -> np.ndarray:
    sieve = np.ones(n + 1, dtype=bool)
    sieve[:2] = False
    sieve[4::2] = False

    for i in range(int(n**0.5) + 1):
        if sieve[i]:
            sieve[3 * i::2 * i] = False

    return sieve


def get_initial_naive(n: int, start_term: int = 1) -> int:
    """
    The most naive approach to find the initial term of the sequence.
    This function will find X_1000, but it will take too much time.

    :param n: Number of elements in the sequence
    :param start_term: From which term to start the check
    :return: The initial term that was found
    """

    initial = start_term

    while True:
        curr_term = initial

        for i in range(n):
            curr_term += i

            if is_prime(curr_term):
                initial += 1
                break

        else:
            return initial


def get_initial_short_seq(n: int, steps_arr_size: int, start_term: int) -> int:
    """
    Finds a valid sequence by iterating on a possible sequence from the largest term
    to the smallest term and eliminating future sequences in the process.

    We eliminate future sequences by setting: steps[term - seq] = False
    By running on a sequence from the largest term to the smallest and finding a prime number,
    we can eliminate the maximum number of steps for each prime we find.
    We also make sure each prime number is encountered at most one time.

    A step is an offset of the initial sequence (1, 2, 4, 7, ...)

    The function precompute all the primes in the range [0:steps_arr_size]

    :param n: Number of elements in the sequence
    :param steps_arr_size: Length of the steps array
    :param start_term: From which term to start the check
    :return: The initial term that was found
    """

    seq = np.flip(np.cumsum(np.arange(n)))
    seq_odd = seq[seq % 2 != 0]
    seq_even = seq[seq % 2 == 0]
    primes = get_primes_till_n(steps_arr_size)
    steps = np.ones(steps_arr_size, dtype=bool)
    offset = start_term - 1

    while True:
        offset += 1

        if steps[offset]:
            # We check only the odd number because even number are not primes
            curr_seq = seq_even if offset % 2 != 0 else seq_odd

            for term in curr_seq + offset:
                if primes[term]:
                    # mark all the places in 'steps[term - seq]' as False,
                    # so we'll know to skip them if we'll reach them
                    steps[term - seq] = False
                    break
            else:
                return offset


def get_initial_any_seq(n: int, steps_arr_size: int, start_term: int) -> int:
    """
    Finds a valid sequence by iterating on a possible sequence from the largest term
    to the smallest term and eliminating future sequences in the process.

    We eliminate future sequences by setting: steps[term - seq] = False
    By running on a sequence from the largest term to the smallest and finding a prime number,
    we can eliminate the maximum number of steps for each prime we find.
    We also make sure each prime number is encountered at most one time.

    A step is an offset of the initial sequence (1, 2, 4, 7, ...)

    To be able to deal with any sequence length, the function calculates each prime number when it reaches it.
    The function has a fixed-size steps array which is reset and offset every time the current step
    passes the array size.

    :param n: Number of elements in the sequence
    :param steps_arr_size: Length of the steps array
    :param start_term: From which term to start the check
    :return: The initial term that was found
    """

    seq = np.flip(start_term + np.cumsum(np.arange(n)))
    seq_odd = seq[seq % 2 != 0]
    seq_even = seq[seq % 2 == 0]
    steps = np.ones(steps_arr_size, dtype=bool)
    global_offset = start_term
    offset = 0

    while True:
        if steps[offset]:
            # We check only the odd number because even number are not primes
            curr_seq = seq_even if offset % 2 != 0 else seq_odd

            for idx, term in enumerate(curr_seq + offset):
                if is_prime(int(term)):
                    try:
                        # Mark all the places in 'steps[term - seq[idx + 1:]]' as False (skip step)
                        # Starting seq from idx to prevent getting negative values
                        steps[term - seq[idx + 1:]] = False

                    except IndexError:
                        print(
                            f"Adding offset. Current offset = {global_offset + offset}"
                        )

                        # Adding offset to the sequence
                        global_offset += offset
                        seq += offset
                        seq_odd = seq[seq % 2 != 0]
                        seq_even = seq[seq % 2 == 0]

                        # Creating a new initialed steps array
                        steps = np.ones(steps_arr_size, dtype=bool)
                        # We need to multiply idx by 2 because we divided seq into 2 arrays
                        steps[term - seq[idx * 2 + 1:]] = False

                        offset = 0
                    break
            else:
                return global_offset + offset

        offset += 1


def get_sequence_initial(n: int, start_term: int = 1) -> int:
    """
    Finding the initial term of the sequence.
    The function 'get_initial_any_seq' can calculate the initial term for any sequence length.
    The function 'get_initial_short_seq' precalculate all the primes in a certain range,
    so for short sequence this function is faster.

    :param n: Number of elements in the sequence
    :param start_term: From which term to start the check
    :return: The initial term that was found
    """

    if n < 1:
        raise ValueError(f"n is smaller than 1 (n = {n})")
    if n == 1:
        return 1
    if n == 2:
        return 8
    if n == 3:
        return 9

    if start_term < 1:
        start_term = 1

    if n <= 1000:
        return get_initial_short_seq(n, 200000000, start_term)

    return get_initial_any_seq(n, 1000000000, start_term)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-n",
        "--numbers",
        default=1000,
        type=int,
        dest="numbers",
        help="number of terms in the sequence",
    )
    parser.add_argument(
        "-st",
        "--start-term",
        default=0,
        type=int,
        dest="start_term",
        help="start solve from this term",
    )

    return parser.parse_args()


def main(args: argparse.Namespace):
    start_term = args.start_term
    n = args.numbers
    print("Starting...")

    start = time.time()
    res = get_sequence_initial(n, start_term)
    end = time.time()

    print("Finished!")
    print(f"Total time = {end - start} seconds")
    print(f"{n=}, {start_term=}")
    print(f"Initial term found = {res}")


if __name__ == "__main__":
    main(parse_args())
