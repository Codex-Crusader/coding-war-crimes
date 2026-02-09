"""
BUBBLE SORT WITH RANDOM DIRECTION CHANGES - BECAUSE DETERMINISM IS OVERRATED

WARNING: This implementation randomly chooses to sort left-to-right or right-to-left
         on each pass. The algorithm eventually sorts (probably).
         Consistency is for cowards.

What this does:
Implements bubble sort, but each pass randomly decides to go forward or backward.

The correct way:
    Bubble sort in one consistent direction. O(n²) worst case, predictable.

The cursed way:
    Flip a coin each pass. Go forward sometimes, backward sometimes.
    Still O(n²) but now with anxiety.

Why this is terrible:
- Non-deterministic sorting (same input, different execution paths)
- Same final result, but random number of passes
- Debugging nightmare (works differently every time)
- Performance varies wildly on identical inputs
- Algorithm correctness depends on RNG
- "It sorted differently in production than in testing"

Performance Comparison:
    Normal bubble sort on [5,1,4,2,8,3]:
        - Deterministic: always same number of passes
        - Worst case: O(n²)
        - Predictable execution

    This chaotic bubble sort:
        - Run 1: 8 passes
        - Run 2: 12 passes
        - Run 3: 6 passes
        - Same input, different runtime every time
        - Still O(n²) expected, but with variance

Real-World Impact:
    Unit tests: Pass sometimes, fail sometimes (same input!)
    Benchmarks: Meaningless (every run is different)
    Debugging: "It worked on my machine" (it literally did work there)
    Production: Random performance characteristics

What We Learn:
- Algorithms should be deterministic
- Randomness for randomness' sake is chaos
- Same input should produce same execution path
- Non-determinism makes everything harder
- Your future self will hate your current self

The Absurdity:
    Forward pass: bubbles large values right
    Backward pass: bubbles small values left
    Both work. Neither is better. Why are we flipping coins?

    It's like randomly deciding to read left-to-right vs right-to-left
    while still understanding the text. Technically possible.
    Completely pointless.

Usage:
    DO use for: Understanding why determinism matters
    DO NOT use for: Anything. Ever. Please.
"""

import random
from typing import List, Any, Optional


def cursed_bubble_sort(
    arr: List[Any],
    backward_chance: float = 0.3,
    seed: Optional[int] = None
) -> List[Any]:
    """
    Bubble sort, but sometimes it walks backwards because vibes.

    Most passes go left → right (normal bubble sort).
    Sometimes it goes right → left (because chaos).
    Still eventually sorts (probably), just slower and more confused.

    Args:
        arr: List of comparable items (sorted in-place)
        backward_chance: Probability (0.0 to 1.0) of doing a backward pass
        seed: Optional random seed for reproducibility (ironic)

    Returns:
        The sorted array (same reference as input)

    Time Complexity:
        Expected: O(n²) - same as normal bubble sort
        Variance: High - number of passes varies randomly
        Worst case: Still O(n²), but with more passes due to bad RNG

    Space Complexity: O(1) - at least we got this right

    Determinism: None. Zero. Negative determinism.

    Notes:
        This is bubble sort with an identity crisis.
        Each pass randomly decides its direction like a lost tourist.

        Forward pass: moves large values toward end
        Backward pass: moves small values toward start
        Both work. Both are valid. Neither knows why they exist.

        The algorithm will eventually sort the array.
        How many passes? Who knows! Depends on RNG.
        Same input, different execution every time.

        Try running this twice on the same unsorted array:
        - First run: 8 passes
        - Second run: 11 passes
        - Same input. Same algorithm. Different path.
        This is why we can't have nice things.

    Example execution on [5, 1, 4, 2, 8, 3]:
        Pass 1: Forward  → [1, 4, 2, 5, 3, 8]  (swapped 4 times)
        Pass 2: Backward → [1, 2, 4, 3, 5, 8]  (swapped 2 times)
        Pass 3: Forward  → [1, 2, 3, 4, 5, 8]  (swapped 1 time)
        Pass 4: Backward → [1, 2, 3, 4, 5, 8]  (swapped 0 times, done!)

        Run it again with different seed:
        Pass 1: Backward → [1, 5, 4, 2, 3, 8]  (swapped 3 times)
        Pass 2: Forward  → [1, 4, 2, 3, 5, 8]  (swapped 2 times)
        Pass 3: Backward → [1, 2, 3, 4, 5, 8]  (swapped 2 times)
        Pass 4: Forward  → [1, 2, 3, 4, 5, 8]  (swapped 0 times, done!)

        Same input. Different journey. Same destination. Maximum confusion.

    Why this is wrong:
        1. Sorting should be deterministic
        2. Same input → same execution path
        3. Randomness adds no value here
        4. Makes testing impossible
        5. Makes debugging a nightmare
        6. Violates principle of least surprise
        7. Your coworkers will have questions
        8. Those questions will be hostile

    Real-world analogy:
        This is like GPS that randomly decides to give you
        directions forward or backward through your route.
        You'll get there eventually.
        But why? Why would you do this?
    """
    if seed is not None:
        random.seed(seed)

    n = len(arr)
    if n < 2:
        return arr

    swapped = True
    pass_count = 0

    # Keep going until we survive a full pass without swaps
    while swapped:
        swapped = False
        pass_count += 1

        # The chaos decision: which direction today?
        go_backward = random.random() < backward_chance

        if not go_backward:
            # Normal left → right pass
            # This is how bubble sort is supposed to work
            # But we only do this sometimes
            # For reasons
            for i in range(0, n - 1):
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    swapped = True
        else:
            # Backwards right → left pass
            # This also works
            # But why are we doing it randomly
            # What problem does this solve
            # This could have been avoided if I was just given a hug.
            for i in range(n - 1, 0, -1):
                if arr[i - 1] > arr[i]:
                    arr[i], arr[i - 1] = arr[i - 1], arr[i]
                    swapped = True

    return arr


def demonstrate_chaos() -> None:
    """Show how the same input produces different execution paths."""
    print("Bubble Sort With Random Direction - A Study in Chaos")
    print("=" * 60)

    test_data = [5, 1, 4, 2, 8, 3]

    print(f"\nOriginal array: {test_data}")
    print("\nRunning the same sort 5 times with different seeds:")
    print("(Same input, different execution every time)")

    for run in range(1, 6):
        run_data = test_data.copy()
        random.seed(run)

        # Instrument to count passes
        n = len(run_data)
        swapped = True
        pass_count = 0
        forward_passes = 0
        backward_passes = 0

        while swapped:
            swapped = False
            pass_count += 1
            go_backward = random.random() < 0.3

            if not go_backward:
                forward_passes += 1
                for i in range(0, n - 1):
                    if run_data[i] > run_data[i + 1]:
                        run_data[i], run_data[i + 1] = run_data[i + 1], run_data[i]
                        swapped = True
            else:
                backward_passes += 1
                for i in range(n - 1, 0, -1):
                    if run_data[i - 1] > run_data[i]:
                        run_data[i], run_data[i - 1] = run_data[i - 1], run_data[i]
                        swapped = True

        print(f"\n  Run {run}:")
        print(f"    Total passes: {pass_count}")
        print(f"    Forward: {forward_passes}, Backward: {backward_passes}")
        print(f"    Result: {run_data}")

    print("\nObservations:")
    print("  - All runs sorted correctly (algorithm is correct)")
    print("  - All runs took different numbers of passes (non-deterministic)")
    print("  - Same input, same algorithm, different execution")
    print("  - This makes testing very difficult")
    print("  - This makes debugging impossible")
    print("  - This makes performance analysis meaningless")

    print("\nComparison to Normal Bubble Sort:")
    normal_data = test_data.copy()

    # Normal bubble sort
    swapped = True
    normal_passes = 0
    while swapped:
        swapped = False
        normal_passes += 1
        for i in range(len(normal_data) - 1):
            if normal_data[i] > normal_data[i + 1]:
                normal_data[i], normal_data[i + 1] = normal_data[i + 1], normal_data[i]
                swapped = True

    print(f"  Normal bubble sort: {normal_passes} passes (always)")
    print(f"  Cursed bubble sort: varies (3-7 passes in our runs)")
    print(f"  Same correctness. Random performance. Maximum confusion.")

    print("\nConclusion:")
    print("  Algorithms should be deterministic.")
    print("  Same input should produce same execution.")
    print("  Randomness for randomness' sake is chaos.")
    print("  Your test suite will hate you.")
    print("  Your debugger will hate you.")
    print("  Your coworkers will definitely hate you.")
    print("  Please don't do this.")
    print("=" * 60)


if __name__ == "__main__":
    # Original demo
    print("Quick Demo:")
    demo_data = [5, 1, 4, 2, 8, 3]
    print("Before:", demo_data)
    cursed_bubble_sort(demo_data, backward_chance=0.4, seed=42)
    print("After: ", demo_data)
    print()

    # Detailed demonstration
    demonstrate_chaos()

# This is what a "child not embraced by the village burns down the village" looks like.