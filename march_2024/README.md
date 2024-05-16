# IBM Ponder This - March 2024 Challenge

Challenge: [Composite Sequences](https://research.ibm.com/haifa/ponderthis/challenges/March2024.html) <br>
My Solution: [Code](march_2024.py)


## Solution
Solution: `115192665` <br>
Bonus: `117778830159`


## General Idea
I have an array `seq` representing the base sequence `(1,2,4,7,...)` and another array representing all the possible offsets of the base sequence.<br>
In every iteration, I increment the offset by 1 and check the sequence `cur_seq`, `(cur_seq = seq + offset)`.<br>
Every iteration I run on `cur_seq` and check each term if it is a prime number. If it is a prime number I set all the offsets represented by `prime_found - cur_seq` as invalid offsets, so we will skip these offsets if we ever reach them.<br>
By doing so we make sure each prime number is encountered at most one time.<br>
If we run on the entire sequence without finding a prime number - we find a solution.<br>

**Optimizations**:
- I run on `cur_seq` from the largest term to the smallest. That way when a prime number is found we eliminate the maximal number of offsets.
- We know that except for the number `2`, even numbers are not primes, so we split the sequence into two sequences - even numbers and odd numbers. In each iteration, we check only the odd numbers.
- Using Numpy for vector operations.
- Because the solution reaches big numbers, for short sequences `(n <= 1000)` I use the Sieve of Eratosthenes algorithm to precompute all the prime numbers. 


## Run Code

```
❯ python march_2024.py [-n] number [-st] start_term

    -n : number of terms in the sequence
    -st: start solve from this term
```

### Examples

- Run the code with default arguments: <br>
(`n=1000`, `st=0`)
```bash
❯ python march_2024.py
```

- Solve for sequence with `2024` numbers and start from term `100000000000`: <br>
```bash
❯ python march_2024.py -n 2024 -st 100000000000
```
