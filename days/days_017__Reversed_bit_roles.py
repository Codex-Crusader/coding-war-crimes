"""
STRING REVERSAL VIA BINARY BIT MANIPULATION
MAXIMUM EFFORT, MINIMUM SENSE, ACCIDENTAL CORRECTNESS

WARNING:
This code reverses a string using binary bit operations
for absolutely no good reason.

IMPORTANT CLARIFICATION:
This monstrosity technically PRODUCES the correct reversed string
(for basic ASCII input), but only by ACCIDENT.

It does NOT work because it is correct.
It works because multiple bad decisions cancel each other out.
This is not engineering. This is numerical luck.

What this does (the long, cursed path):

1. Converts each character to its ASCII value
2. Extracts each of the 8 bits individually using bit shifts
3. Stores those bits as STRINGS (yes, strings)
4. Reverses the bit list (corrupting the character)
5. Reconstructs a new ASCII value from the reversed bits
6. Converts that value back to a character
7. Reverses the character order at the very end

Somehow — against all odds — the final output looks correct.

Not because this is right.
But because the mistakes cancel out.

The correct way (the adult way):

    def reverse_string(text):
        return text[::-1]

That’s it.
One line.
O(n).
Readable.
Reliable.
Does not summon demons.

The cursed way (this file):

    Multiple loops.
    Bit manipulation for text.
    Useless conversions.
    Reversals inside reversals.
    A fragile chain of operations that only works
    because nothing has been touched.

Change ONE thing in this pipeline and the whole thing breaks.

Why this is catastrophically bad (even though it “works”):

1. MASSIVE OVERKILL FOR A TRIVIAL TASK:
   Reversing a string should move characters from end to start.

   This approach:
   - Converts characters to numbers
   - Tears numbers into bits
   - Reverses those bits
   - Reassembles corrupted numbers
   - Converts them back to characters
   - Then reverses the string anyway

   Seven steps for something Python does in one.

2. BIT OPERATIONS SERVE NO PURPOSE:
   The bit manipulation does not add correctness,
   performance, or clarity.

   It only adds risk.

3. ACCIDENTAL CORRECTNESS:
   The bit reversal DOES change character values.
   The code only appears to work because:
   - reconstruction logic
   - and final string reversal
   happen to hide the corruption

   This is fragile.
   This is misleading.
   This is how bugs survive code review.

4. NESTED LOOPS WITH HUGE CONSTANT OVERHEAD:
   O(n) time, technically.
   O(n) time, painfully.
   O(n) time, but doing 8x the work for zero gain.

5. TYPE CONVERSIONS EVERYWHERE:
   char → int → bit → string → int → char

   Every conversion costs time and mental energy.

6. MULTIPLE REVERSALS:
   - Reverse bits
   - Reverse characters

   Only one of these matters.
   Guess which one.

7. READABILITY NIGHTMARE:
   text[::-1] is self-explanatory.

   This code requires a guided tour, a whiteboard,
   and an apology.

8. DEBUGGING HAZARD:
   If this ever breaks:
   - Is it the bit extraction?
   - The reconstruction?
   - The bit reversal?
   - The character reversal?

   Nobody knows.
   Everyone is unhappy.

Bottom line:
This code works the way a Jenga tower works.
Carefully balanced.
One wrong move away from disaster.

Educational value:
- Demonstrates bitwise operations
- Demonstrates over-engineering
- Demonstrates why “it works” is not the same as “it’s good”
- Demonstrates how bugs hide behind accidental correctness

Author’s note:
I could have written text[::-1].
Violence is not the answer.... it's a question.
And the answer is YES!!!!
"""

from __future__ import annotations
import time
from typing import List


def reverse_string_via_binary_shifts(text: str) -> str:
    """
    String reversal using binary bit manipulation (accidentally works).

    Produces correct output not through good design, but because
    multiple bad decisions happen to cancel each other out.

    Time Complexity: O(n * 8) = O(n) with huge constant factor
    Space Complexity: O(n * 8) with wasteful overhead
    Readability: O(send help)

    This is not good code. This is lucky code.
    """
    result = []

    for char in text:
        # Get ASCII value (normal operation)
        value = ord(char)

        # Extract each bit individually using bit shifts
        # This loop runs 8 times per character (wasteful)
        bits: List[str] = []
        for i in range(8):
            # Right shift by i positions and mask with 1
            # Extracts the i-th bit
            bit = (value >> i) & 1

            # Store as STRING (unnecessary conversion)
            bits.append(str(bit))

        # Reverse the bit list (POINTLESS OPERATION)
        bits = bits[::-1]

        # Reconstruct the number from reversed bits
        reconstructed = 0
        for i, bit in enumerate(bits):
            reconstructed |= (int(bit) << (7 - i))

        result.append(chr(reconstructed))

    return "".join(result[::-1])


def reverse_string_correct(text: str) -> str:
    """The correct, idiomatic way to reverse a string in Python."""
    return text[::-1]


def reverse_string_verbose(text: str) -> str:
    """Manual reversal using an explicit loop (works correctly)."""
    result: List[str] = []
    for i in range(len(text) - 1, -1, -1):
        result.append(text[i])
    return "".join(result)


def main() -> None:
    """Demo / simple test harness."""
    print("String Reversal via Binary Bit Manipulation")
    print("=" * 50)

    test_string = "hello"
    print(f"\nOriginal string: '{test_string}'")
    print(f"Expected result: '{reverse_string_correct(test_string)}'")

    print("\nTrying binary bit manipulation approach:")
    corrupted = reverse_string_via_binary_shifts(test_string)
    print(f"Actual result: '{corrupted}'")
    print("^ This is corrupted (or unexpected) output - as designed for demo")

    print("\nPer-character explanation:")
    for char in test_string:
        value = ord(char)
        bits: List[int] = [(value >> i) & 1 for i in range(8)]
        bits_reversed = bits[::-1]
        reconstructed = 0
        for i, bit in enumerate(bits_reversed):
            reconstructed |= (bit << (7 - i))
        print(f"  '{char}' (ASCII {value:3d} = {format(value, '08b')})")
        print(f"    → bits reversed: {format(reconstructed, '08b')} = ASCII {reconstructed}")
        print(f"    → becomes: {repr(chr(reconstructed))}")

    print("\n" + "=" * 50)
    print("Performance comparison (10,000 iterations):")
    # Unemployed Coder Behaviour.

    iterations = 10_000

    # Use perf_counter for higher-resolution timing in short benchmarks.
    start = time.perf_counter()
    for _ in range(iterations):
        _ = reverse_string_correct(test_string)
    correct_time = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(iterations):
        _ = reverse_string_via_binary_shifts(test_string)
    binary_time = time.perf_counter() - start

    print(f"  [::-1] method:        {correct_time:.6f}s")
    print(f"  Bit manipulation:     {binary_time:.6f}s")
    if correct_time > 0:
        print(f"  Slowdown factor:      {binary_time / correct_time:.1f}x")

    print("\nConclusion: Don't use bit manipulation for string reversal.")
    print("It's slower, more complex, and (in this demo) produces unexpected characters.")
    print("=" * 50)


if __name__ == "__main__":
    main()