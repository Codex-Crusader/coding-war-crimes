"""
FIZZBUZZ WITH NESTED TERNARIES - NO IF STATEMENTS ALLOWED

WARNING: This code violates the Geneva Conventions on readable code.

What is FizzBuzz:
A classic programming exercise where you print:
- "Fizz" for multiples of 3
- "Buzz" for multiples of 5
- "FizzBuzz" for multiples of both (15)
- The number itself otherwise

What this implementation does:
Solves FizzBuzz using ONLY nested ternary (conditional) expressions.
No if statements. No match/case. Just ternaries all the way down.

The Ternary Operator:
    result = value_if_true if condition else value_if_false

The Horror:
When you nest them, you get a sideways pyramid of pain that reads like:
    A if X else (B if Y else (C if Z else D))

Time Complexity: O(n) - at least this part is fine
Space Complexity: O(1) - we're not making this worse than it needs to be
Readability: O(my eyes are bleeding)

Why this is cursed:
1. Nested ternaries are hard to read
2. The indentation forms a diagonal line of sadness
3. Each condition is checked in sequence (can't short-circuit easily)
4. Imagine debugging this at 2 AM
5. Adding a new condition means re-nesting everything

The correct way:
    if i % 15 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)

Clear, readable, maintainable. Everything this code is not.

Why we check 15 first:
Because 15 is divisible by both 3 and 5, we need to check it before
checking 3 or 5 individually. Otherwise we'd never print "FizzBuzz".

Educational value:
- Shows that "clever" one-liners are often just hard to read
- Demonstrates why if-elif-else chains exist
- Proves that fewer lines ≠ better code
- A cautionary tale about premature optimization of line count

Fun fact:
Some languages don't have ternary operators. Those languages are blessed.

Author's note: I could have just used if statements. I chose violence.
"""


def fizzbuzz(n: int = 100) -> None:
    """
    Print FizzBuzz for 1..n using nested ternary (conditional) expressions only.
    """
    for i in range(1, n + 1):
        s = ("FizzBuzz" if i % 15 == 0
             else ("Fizz" if i % 3 == 0
                   else ("Buzz" if i % 5 == 0
                         else str(i))))
        print(s)

if __name__ == "__main__":
    fizzbuzz(30)  # example: prints FizzBuzz results for 1..30
