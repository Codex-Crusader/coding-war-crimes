"""
FIBONACCI - THE EXPONENTIAL NIGHTMARE

WARNING: Do NOT call this with n > 40 unless you have time to waste.

What this does:
Calculates Fibonacci numbers using pure recursion with ZERO optimization.
Every call recalculates all previous values from scratch.

The Fibonacci sequence:
F(0) = 0
F(1) = 1
F(n) = F(n-1) + F(n-2)

Sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89...

Time Complexity: O(2^n) - EXPONENTIAL
Space Complexity: O(n) - call stack depth
Pain Complexity: O(watching paint dry)

Why this is catastrophically slow:

The recursion tree for fib(5):
                    fib(5)
                   /      \
              fib(4)        fib(3)
             /     \        /     \
        fib(3)   fib(2)  fib(2)  fib(1)
        /   \     /   \   /   \
    fib(2) fib(1) ...  ... ...  ...

Notice: fib(3) is calculated TWICE, fib(2) THREE times, fib(1) FIVE times!

Number of function calls for each n:
- fib(5):  15 calls
- fib(10): 177 calls
- fib(20): 21,891 calls
- fib(30): 2,692,537 calls
- fib(40): 331,160,281 calls (this takes ~30 seconds)
- fib(50): Would take HOURS

The function calls grow exponentially: roughly 2^n calls for fib(n)

Redundant calculations:
For fib(6):
- fib(1) is calculated 8 times
- fib(2) is calculated 5 times
- fib(3) is calculated 3 times
- fib(4) is calculated 2 times
- fib(5) is calculated 1 time

We're doing the SAME calculation over and over and over...

Performance breakdown (on typical modern CPU):
- fib(10): ~0.00001 seconds
- fib(20): ~0.002 seconds
- fib(30): ~0.3 seconds
- fib(35): ~3 seconds
- fib(40): ~30 seconds
- fib(45): ~5 minutes
- fib(50): ~several hours

Each increment by 1 roughly DOUBLES the time!

The correct ways:

Method 1 - Memoization (cache results):
    cache = {}
    def fib(n):
        if n in cache:
            return cache[n]
        if n <= 1:
            return n
        cache[n] = fib(n-1) + fib(n-2)
        return cache[n]

    Time: O(n), Space: O(n)

Method 2 - Iteration (no recursion):
    def fib(n):
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n+1):
            a, b = b, a + b
        return b

    Time: O(n), Space: O(1)

Method 3 - Python's built-in (from Python 3.2+):
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def fib(n):
        if n <= 1:
            return n
        return fib(n-1) + fib(n-2)

    Time: O(n), Space: O(n)
    Same code, automatic memoization!

Method 4 - Matrix exponentiation (advanced):
    Time: O(log n), Space: O(1)
    Uses the matrix: [[1,1],[1,0]]^n

Method 5 - Closed form (Binet's formula):
    phi = (1 + sqrt(5)) / 2
    fib(n) = (phi^n - (-phi)^-n) / sqrt(5)

    Time: O(1), but has floating point precision issues

Comparison for fib(35):

This version:
- Function calls: 29,860,703
- Time: ~3 seconds

With memoization:
- Function calls: 35
- Time: < 0.001 seconds

Speedup: ~3000x faster!

Why this exists in textbooks:
- Perfect example of overlapping subproblems
- Demonstrates the power of dynamic programming
- Shows exponential vs linear time complexity
- Motivates learning memoization

Real-world analogy:
Imagine calculating 100 + 50 by:
1. Counting from 1 to 100
2. Counting from 1 to 50
3. Adding them

Then, to calculate 100 + 51, you:
1. Count from 1 to 100 AGAIN
2. Count from 1 to 51 AGAIN
3. Add them

Instead of just remembering "100" from before.

Mathematical insight:
The number of calls to calculate fib(n) is actually fib(n+1) - 1
So to calculate the 40th Fibonacci number, you make 165,580,141 calls!

Educational value:
- Classic example of recursion
- Demonstrates exponential time complexity
- Motivates dynamic programming
- Shows why caching matters
- Proves that "simple" ≠ "efficient"

Warning signs you're doing this wrong:
- Your laptop starts heating up
- Small inputs take forever
- You add 1 to n and runtime doubles
- You question your life choices

The irony:
Fibonacci numbers grow exponentially: F(n) ≈ φ^n / √5
And this algorithm takes exponential time to compute them!

Author's note: I could have added one line for memoization.
                I chose pain instead.
                Every. Single. Recalculation. Hurts.
"""


def fibonacci(n):
    """
    Calculate the nth Fibonacci number using pure recursion.

    No memoization. No optimization. Just raw, exponential recursion.

    Args:
        n: The position in the Fibonacci sequence (0-indexed)

    Returns:
        The nth Fibonacci number

    Time Complexity: O(2^n) - exponential disaster
    Space Complexity: O(n) - maximum call stack depth

    Warning: Do NOT call with n > 40 unless you enjoy waiting.

    For n=40: ~30 seconds and 331 million function calls
    For n=50: Several hours and ~12 billion function calls

    Comparison:
    - This version: fibonacci(40) ≈ 30 seconds
    - With memoization: fibonacci(40) ≈ 0.001 seconds
    The same code with one decorator (@lru_cache) is 30,000x faster.
    """
    # Base cases (the only part that doesn't hurt)
    if n == 0:
        return 0
    if n == 1:
        return 1

    # The pain: recalculate everything again. Every. Single. Time.
    # fib(5) calls fib(4) and fib(3)
    # fib(4) calls fib(3) and fib(2) ← fib(3) calculated AGAIN
    # fib(3) calls fib(2) and fib(1) ← fib(2) calculated AGAIN
    # And so on, creating an exponential explosion of redundant work
    return fibonacci(n - 1) + fibonacci(n - 2)


# Example usage with performance measurements
if __name__ == "__main__":
    import time

    print("Fibonacci - The Exponential Nightmare")
    print("=" * 50)

    # Calculate and time small values
    print("\nCalculating Fibonacci numbers (watch it slow down):\n")

    test_values = [5, 10, 15, 20, 25, 30, 35]

    for num in test_values:
        start = time.time()
        result = fibonacci(num)
        elapsed = time.time() - start

        print(f"fib({num:2d}) = {result:>10,} | Time: {elapsed:>8.5f}s")

        if elapsed > 5:
            print("\n[PAUSE]  Taking too long, stopping here...")
            print("Try fib(40) if you have 30 seconds to spare!")
            break

    print("\n" + "=" * 50)
    print("The correct way (with memoization):")
    print("=" * 50)

    from functools import lru_cache


    @lru_cache(maxsize=None)
    def fib_fast(n):
        if n <= 1:
            return n
        return fib_fast(n - 1) + fib_fast(n - 2)


    print("\nSame algorithm, just add @lru_cache:\n")

    for num in [35, 40, 50, 100]:
        start = time.time()
        result = fib_fast(num)
        elapsed = time.time() - start
        print(f"fib({num:3d}) = {result:>25,} | Time: {elapsed:>10.7f}s")

    print("\n" + "=" * 50)
    print("One decorator. 1000x+ speedup.")
    print("This is why memoization exists.")
    print("=" * 50)