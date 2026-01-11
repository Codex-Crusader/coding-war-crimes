"""
BOOLEAN LOGIC USING ONLY ARITHMETIC - BECAUSE WHY NOT

WARNING: This code pretends computers don't have logical operators.

What this does:
Implements boolean AND, OR, NOT, and XOR using only arithmetic operations.
No 'and', 'or', 'not', or '^' operators allowed. Just math.

The "Boolean as Integer" approach:
- True = 1
- False = 0
- Then use arithmetic to mimic logical operations

How each operation works:

AND (a * b):
    0 * 0 = 0 (False AND False = False)
    0 * 1 = 0 (False AND True = False)
    1 * 0 = 0 (True AND False = False)
    1 * 1 = 1 (True AND True = True)

    Why it works: Multiplication is 1 only when BOTH are 1

OR (a + b - a*b):
    0 + 0 - 0 = 0 (False OR False = False)
    1 + 0 - 0 = 1 (False OR True = True)
    0 + 1 - 0 = 1 (True OR False = True)
    1 + 1 - 1 = 1 (True OR True = True)

    Why it works: Addition gives 1 if EITHER is 1, but 1+1=2,
                  so we subtract (a*b) to handle the both-true case

    Alternative: min(a + b, 1) or (a + b) >= 1
    But where's the fun in that?

NOT (1 - a):
    1 - 0 = 1 (NOT False = True)
    1 - 1 = 0 (NOT True = False)

    Why it works: Simple flip in binary

XOR ((a + b) % 2):
    (0 + 0) % 2 = 0 (False XOR False = False)
    (1 + 0) % 2 = 1 (True XOR False = True)
    (0 + 1) % 2 = 1 (False XOR True = True)
    (1 + 1) % 2 = 0 (True XOR True = False)

    Why it works: XOR is true when inputs DIFFER, which means
                  odd sum (1), false when inputs MATCH (even sum: 0 or 2)

Time Complexity: O(1) for each operation
Space Complexity: O(1)
Historical Accuracy: O(vacuum tube computers from 1945)

Why this is terrible:
1. Python has 'and', 'or', 'not', '^' built-in
2. No type safety - bool_and(5, 7) = 35 (definitely not a boolean)
3. Less readable than actual boolean operators
4. Doesn't handle True/False keywords, only 1/0
5. Slower than native logical operations (though barely measurable)

The correct way:
    def bool_and(a, b): return a and b
    def bool_or(a, b): return a or b
    def bool_not(a): return not a
    def bool_xor(a, b): return a ^ b

Or better yet, just use the operators directly:
    result = x and y
    result = x or y
    result = not x
    result = x ^ y

Educational value:
- Shows how boolean logic can be represented mathematically
- Demonstrates that computers ultimately do arithmetic on bits
- Proves that abstraction exists for a reason
- Historical context: early computers actually did this!

Fun facts:
- Early computers used arithmetic circuits for logic
- Boolean algebra was invented by George Boole in 1854
- Modern CPUs have dedicated logic gates, not arithmetic units for this
- This approach breaks if you pass non-binary values

Real-world usage:
None. Absolutely none. Don't do this in production.
Unless you're emulating a 1940s computer, in which case, carry on.

Author's note: I could have typed 'and', 'or', 'not'.
                I chose to do arithmetic instead.
                I have no excuse.
"""


def bool_and(a, b):
    """
    Boolean AND using multiplication.

    Returns 1 only if both a and b are 1.

    WARNING: Breaks if you pass anything other than 0 or 1.
    bool_and(5, 7) = 35, which is... not a boolean.
    """
    # AND: 1 * 1 = 1, everything else = 0
    return a * b


def bool_or(a, b):
    """
    Boolean OR using the formula: a + b - (a * b)

    Returns 1 if at least one input is 1.

    The (a * b) subtraction handles the case where both are 1,
    preventing us from returning 2.

    Alternative formulas that also work:
    - min(a + b, 1)
    - int((a + b) >= 1)
    - a + b - a * b  (what we use)
    """
    # OR: a + b - (a * b)
    # 0+0-0 = 0
    # 1+0-0 = 1
    # 0+1-0 = 1
    # 1+1-1 = 1
    return a + b - (a * b)


def bool_not(a):
    """
    Boolean NOT using subtraction from 1.

    Flips 0 to 1 and 1 to 0.

    This is the simplest operation because boolean NOT
    is literally just binary flip.
    """
    # NOT: 1 - a
    # 1 - 1 = 0
    # 1 - 0 = 1
    return 1 - a


def bool_xor(a, b):
    """
    Boolean XOR using modulo arithmetic.

    Returns 1 if inputs are different, 0 if they're the same.

    Works because:
    - Different values sum to 1 (odd) → 1 % 2 = 1
    - Same values sum to 0 or 2 (even) → (0 or 2) % 2 = 0
    """
    # XOR: (a + b) % 2
    return (a + b) % 2


# Inputs (only 0 or 1 allowed, but we have no enforcement)
true = 1
false = 0

# Demonstration
if __name__ == "__main__":
    print("Boolean Logic via Arithmetic Operations")
    print("=" * 50)

    print("\nAND (multiplication):")
    print(f"  {true} AND {true} = {bool_and(true, true)}")  # 1
    print(f"  {true} AND {false} = {bool_and(true, false)}")  # 0
    print(f"  {false} AND {false} = {bool_and(false, false)}")  # 0

    print("\nOR (a + b - a*b):")
    print(f"  {true} OR {false} = {bool_or(true, false)}")  # 1
    print(f"  {false} OR {false} = {bool_or(false, false)}")  # 0
    print(f"  {true} OR {true} = {bool_or(true, true)}")  # 1

    print("\nNOT (1 - a):")
    print(f"  NOT {true} = {bool_not(true)}")  # 0
    print(f"  NOT {false} = {bool_not(false)}")  # 1

    print("\nXOR ((a + b) % 2):")
    print(f"  {true} XOR {false} = {bool_xor(true, false)}")  # 1
    print(f"  {true} XOR {true} = {bool_xor(true, true)}")  # 0
    print(f"  {false} XOR {false} = {bool_xor(false, false)}")  # 0

    print("\n" + "=" * 50)
    print("The correct way to do this:")
    print("  a and b")
    print("  a or b")
    print("  not a")
    print("  a ^ b")
    print("=" * 50)

    print("\nBonus - What happens with invalid inputs:")
    print(f"  bool_and(5, 7) = {bool_and(5, 7)} (expected 0 or 1, got 35)")
    print(f"  bool_or(3, 4) = {bool_or(3, 4)} (expected 0 or 1, got {bool_or(3, 4)})")
    print("\nThis is why we have type systems.")