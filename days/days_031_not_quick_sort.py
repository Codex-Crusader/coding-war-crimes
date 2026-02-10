"""
QUICKSORT THAT ALWAYS PICKS THE WORST PIVOT - MASOCHISM AS ALGORITHM DESIGN

WARNING: This implementation deliberately chooses the worst possible pivot.
         On sorted data (common in real life), this degrades to O(n²) every time.
         Your call stack will file a complaint.

What this does:
Implements quicksort by always picking the first element as pivot, guaranteeing
worst-case performance on sorted or nearly-sorted data.

The correct way:
    Pick median-of-three, random pivot, or any strategy that avoids worst case.
    Achieve O(n log n) average case reliably.

The cursed way:
    Always pick first element. On sorted data: guaranteed O(n²).
    Turn the best general-purpose sort into the worst.

Why this is terrible:
- Sorted input (very common): O(n²) every time
- Nearly sorted input (also common): O(n²) usually
- Random input (rare): O(n log n) sometimes
- We've optimized for the wrong case
- Creates maximally unbalanced partitions
- Stack depth becomes O(n) instead of O(log n)
- Risk of stack overflow on large sorted inputs

Performance Comparison (10,000 elements):
    Random data:
        - Good quicksort: ~5ms
        - This quicksort: ~5ms (gets lucky)

    Sorted data:
        - Good quicksort: ~5ms (detects and handles)
        - This quicksort: ~5000ms (O(n²) nightmare)
        - Slowdown: 1000x

Real-World Impact:
    Sorted logs: Takes minutes instead of milliseconds
    Database results: Already sorted, maximum pain
    Sequential IDs: Worst case every time
    Time series data: Chronologically cursed

What We Learn:
- Pivot selection is critical to quicksort performance
- Sorted data is common, not a corner case
- O(n²) on real-world data is worse than O(n log n) always
- Worst-case behavior matters
- Stack depth matters

The Irony:
    Quicksort is called "quick" for a reason.
    This version is quick only when it doesn't matter.
    On common inputs, it's slower than bubble sort.

Usage:
    DO use for: Understanding why pivot selection matters
    DO NOT use for: Sorting anything ever
"""

from typing import List, Any


def cursed_quick_sort(arr: List[Any]) -> List[Any]:
    """
    Quicksort that always picks the WORST possible pivot.

    For sorted or reverse-sorted arrays, the worst pivot is the first or last element.
    This version ALWAYS picks the first element as pivot.

    If the input is sorted (common in real life), this degrades to O(n²).
    On purpose. Every time.

    Args:
        arr: List to sort

    Returns:
        New sorted list (creates O(n) extra space too!)

    Time Complexity:
        Best case:    O(n log n) - random data with luck
        Average case: O(n log n) - if data is shuffled
        Worst case:   O(n²) - sorted/reverse/nearly-sorted (COMMON!)

    Space Complexity:
        O(n) - creates new lists for partitions (inefficient!)
        Also O(n) recursion depth in worst case (stack overflow risk!)

    Compare to good quicksort:
        - Uses median-of-three or random pivot
        - O(n log n) expected on ALL inputs
        - O(log n) recursion depth expected
        - In-place partitioning (no extra lists)

    This is quicksort with a self-destructive personality.

    Notes:
        Quicksort's performance depends critically on pivot choice.

        Good pivot (median):
            - Divides array roughly in half
            - Recursion depth: O(log n)
            - Total work: O(n log n)

        Bad pivot (first element on sorted data):
            - One partition has 0 elements, other has n-1
            - Recursion depth: O(n)
            - Total work: O(n²)
            - Stack overflow risk on large inputs

        Example on sorted [1,2,3,4,5]:
            Pick 1 as pivot:
                - Left partition: [] (0 elements)
                - Right partition: [2,3,4,5] (4 elements)
            Pick 2 as pivot:
                - Left partition: [] (0 elements)
                - Right partition: [3,4,5] (3 elements)
            Pick 3 as pivot:
                - Left partition: [] (0 elements)
                - Right partition: [4,5] (2 elements)
            ...

            Each level does O(n) work.
            We have O(n) levels.
            Total: O(n²)

        This is the pathological case.
        And we trigger it on every sorted input.
        On purpose.

    Real-world scenarios where this fails spectacularly:
        - Sorting database query results (often pre-sorted by index)
        - Sorting log files (chronological = sorted)
        - Sorting user IDs (sequential = sorted)
        - Sorting timestamps (monotonic = sorted)
        - Re-sorting already sorted data (common in UI)
        - Sorting nearly-sorted data (insertion sort would be faster!)

    Why this is worse than other O(n²) sorts:
        - Bubble sort is consistently O(n²), at least it's honest
        - Insertion sort is O(n) on nearly-sorted data (good!)
        - This quicksort: O(n log n) on random, O(n²) on common
        - We've optimized for the rare case, failed on the common case
        - This is backwards optimization
    """
    # Base case: arrays of size 0 or 1 are already sorted
    if len(arr) <= 1:
        return arr

    # The cursed choice: pick the first element as pivot
    # On sorted input, this is the WORST possible pivot every time.
    # It creates maximally unbalanced partitions.
    # One side gets 0 elements, the other gets n-1.
    # This is the definition of bad partitioning.
    pivot = arr[0]

    # Partition the rest into left and right
    # We're also creating new lists here (O(n) extra space)
    # instead of partitioning in-place like a proper quicksort
    left = []
    right = []

    for x in arr[1:]:
        if x < pivot:
            left.append(x)
        else:
            right.append(x)

    # Recursively sort (slowly, painfully, deeply)
    # On sorted input, left is always empty
    # So we recurse on arrays of size n-1, n-2, n-3...
    # Recursion depth: O(n)
    # Work per level: O(n)
    # Total: O(n²)
    # Stack frames: O(n) - risk of stack overflow!
    return cursed_quick_sort(left) + [pivot] + cursed_quick_sort(right)


def demonstrate_pathological_behavior() -> None:
    """Show how this quicksort fails on common inputs."""

    print("Quicksort That Always Picks the Worst Pivot")
    print("=" * 60)

    # Test 1: Already sorted data (common case, worst performance)
    print("\nTest 1: Sorted data (worst case for this implementation)")
    sorted_data = list(range(1, 11))
    print(f"  Input:  {sorted_data}")
    result = cursed_quick_sort(sorted_data)
    print(f"  Output: {result}")
    print(f"  Recursion depth: O(n) = {len(sorted_data)}")
    print(f"  Time complexity: O(n²)")
    print(f"  This is the COMMON case in real applications!")

    # Test 2: Reverse sorted (still terrible)
    print("\nTest 2: Reverse sorted data (also worst case)")
    reverse_data = list(range(10, 0, -1))
    print(f"  Input:  {reverse_data}")
    result2 = cursed_quick_sort(reverse_data)
    print(f"  Output: {result2}")
    print(f"  Recursion depth: O(n)")
    print(f"  Time complexity: O(n²)")

    # Test 3: Random data (performs acceptably)
    print("\nTest 3: Random data (performs okay by accident)")
    random_data = [7, 2, 9, 1, 5, 3, 8, 4, 6]
    print(f"  Input:  {random_data}")
    result3 = cursed_quick_sort(random_data)
    print(f"  Output: {result3}")
    print(f"  Recursion depth: O(log n) (lucky!)")
    print(f"  Time complexity: O(n log n) (when we get lucky)")

    # Test 4: Nearly sorted (still bad)
    print("\nTest 4: Nearly sorted data (common in practice)")
    nearly_sorted = [1, 2, 3, 4, 5, 7, 6, 8, 9, 10]
    print(f"  Input:  {nearly_sorted}")
    result4 = cursed_quick_sort(nearly_sorted)
    print(f"  Output: {result4}")
    print(f"  Still creates unbalanced partitions")
    print(f"  Time complexity: Close to O(n²)")

    print("\nWhy First Element is the Worst Pivot Choice:")
    print("  Sorted data → always smallest → left partition empty")
    print("  Reverse sorted → always largest → right partition empty")
    print("  Nearly sorted → usually extreme → unbalanced partitions")
    print("  Result: O(n) recursion depth instead of O(log n)")

    print("\nBetter Pivot Strategies:")
    print("  1. Random element: O(n log n) expected on all inputs")
    print("  2. Median-of-three: Good balance, prevents worst case")
    print("  3. Middle element: Better than first/last")
    print("  4. Anything except first/last on sorted data!")

    print("\nReal-World Impact:")
    print("  Database results: Often sorted by index → O(n²)")
    print("  Log files: Chronological order → O(n²)")
    print("  User IDs: Sequential → O(n²)")
    print("  File listings: Often sorted → O(n²)")
    print("  Time series: Monotonic → O(n²)")

    print("\nPerformance on 1000 sorted elements:")
    print("  Good quicksort: ~1ms")
    print("  This quicksort: ~1000ms")
    print("  Insertion sort: ~10ms (yes, insertion sort is faster!)")

if __name__ == "__main__":
    # Quick demo
    print("Quick Demo:")
    print("\nSorted data (worst case):")
    sorted_input = list(range(1, 11))
    print("Before:", sorted_input)
    sorted_result = cursed_quick_sort(sorted_input)
    print("After: ", sorted_result)

    print("\nReverse sorted (also worst case):")
    reverse_input = list(range(10, 0, -1))
    print("Before:", reverse_input)
    reverse_result = cursed_quick_sort(reverse_input)
    print("After: ", reverse_result)

    # Detailed demonstration
    demonstrate_pathological_behavior()