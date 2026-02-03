"""
HEAP THAT SORTS ON EVERY INSERT - BECAUSE EFFICIENCY IS FOR COWARDS

WARNING: This implementation maintains heap order by sorting the entire array
         on every insertion. O(log n) insert becomes O(n log n).
         Your CPU will question your life choices.

What this does:
Implements a min-heap by... just sorting the entire list every time you insert.

The correct way:
    Use a binary heap. Insert in O(log n). Maintain heap property by sifting.

The cursed way:
    Insert value, then sort entire array. Every. Single. Time.

Why this is terrible:
- Insert one element: sort all n elements
- Binary heap sifts up in O(log n) steps
- This sorts in O(n log n) operations
- For n insertions: O(n² log n) total instead of O(n log n)
- Pop is O(1) but only because we already did all the work

Performance Comparison (inserting 1,000 elements):
    Real binary heap: ~0.5ms total (O(n log n))
    This sorted heap: ~500ms total (O(n² log n))
    Slowdown factor: ~1000x

Real-World Impact:
    Small heap (100 items):     Noticeable delay on each insert
    Medium heap (10,000 items): Multi-second insertions
    Large heap (1M items):      Heat death of universe

What We Learn:
- Incremental updates beat global recomputation
- Sorting n items to place 1 item is wasteful
- O(log n) is much better than O(n log n)
- Data structures exist to avoid this exact problem

The Irony:
    Reads are blazing fast (O(1) peek, O(1) pop)
    Writes are catastrophically slow (O(n log n) insert)
    We optimized the wrong operations

Usage:
    DO use for: Understanding why heaps use sift operations
    DO NOT use for: Priority queues, job schedulers, anything real

P.S: I could have implemented sift-up like a normal person.
     Instead I chose to sort the entire array on every insert.
     This is algorithmic malpractice.

Author Note: The CPU filed for workers' compensation.
"""

from typing import List, Any


class HeapBySorting:
    """
    A heap that maintains order by sorting the entire array on every insert.

    Properties:
    - Always sorted (expensive)
    - Always slow (guaranteed)
    - Never a real heap (technically)

    Time Complexity:
        insert(): O(n log n) - sort entire array
        pop():    O(1) - just pop first element
        peek():   O(1) - just look at first element

    Compare to real binary heap:
        insert(): O(log n) - sift up
        pop():    O(log n) - sift down
        peek():   O(1) - look at root

    This implementation pays maximum cost upfront (sorting)
    to avoid doing the right thing incrementally (sifting).

    It's like renovating your entire house every time you buy new furniture.
    """

    def __init__(self) -> None:
        """
        Initialize the heap.

        Actually just a list that we'll abuse with constant sorting.
        """
        self._data: List[Any] = []

    def insert(self, value: Any) -> None:
        """
        Insert a value into the heap.

        What a binary heap does:
            1. Append value to end - O(1)
            2. Sift up until heap property restored - O(log n)
            3. Total: O(log n)

        What this does:
            1. Append value to end - O(1)
            2. Sort entire array - O(n log n)
            3. Pretend this is normal - O(regret)

        Args:
            value: Element to insert

        Time Complexity: O(n log n) per insert
        What It Should Be: O(log n)
        Efficiency Loss: Factor of n

        Notes:
            Sorting n elements to place one element correctly
            is the algorithmic equivalent of:
            - Repainting your entire house because you moved a chair
            - Rebuilding a city because someone moved into one apartment
            - Recounting all votes because one person voted
            - Reshuffling a deck because you drew one card

        Example:
            Heap has 1,000,000 elements.
            You insert 1 new element.
            We sort all 1,000,001 elements.
            Binary heap would do ~20 comparisons.
            We do ~20,000,000 comparisons.
            Bruh.....
        """
        self._data.append(value)  # O(1): The only efficient part
        self._data.sort()  # O(n log n): Nuclear option activated

    def pop(self) -> Any:
        """
        Remove and return the smallest element.

        This is O(1) only because we already paid O(n log n) during insertion.

        It's like buying a private jet to go someplace that takes 11 minutes by car
        Sure, getting there is fast now, but was it worth the cost?
        It might be if you are taylor swift.....

        Returns:
            Smallest element in the heap

        Raises:
            IndexError: If heap is empty

        Time Complexity: O(1)
        Hidden Cost: The O(n log n) we paid during insert

        Notes:
            Pop is artificially fast because insert is artificially slow.
            We've shifted all the work to insertion.
            This is the wrong trade-off for a heap.
            Heaps are meant for fast inserts and reasonably fast pops.
            We have slow inserts and fast pops.
            We've inverted the entire purpose.
            And you can't look away. Like a slow train wreak
        """
        if not self._data:
            raise IndexError("pop from empty heap")
        return self._data.pop(0)  # O(n): shifts entire list left
        # This is O(n). We sorted everything earlier anyway.
        # At this point, complexity is just a suggestion.

    def peek(self) -> Any:
        """
        Return the smallest element without removing it.

        Time Complexity: O(1)
        Irony Level: Maximum

        This is the one operation that's actually efficient,
        but only because we made everything else inefficient.

        Returns:
            Smallest element

        Raises:
            IndexError: If heap is empty

        Notes:
            Fast reads, catastrophically slow writes.
            Like a database that takes hours to insert one row
            but can query instantly.
            Congratulations, you've built a write-pessimized system.
        """
        if not self._data:
            raise IndexError("peek from empty heap")
        return self._data[0]

    def __len__(self) -> int:
        """Return number of elements in the heap."""
        return len(self._data)

    def __bool__(self) -> bool:
        """Return True if heap is non-empty."""
        return len(self._data) > 0

    def __str__(self) -> str:
        """
        Return internal state.

        Always perfectly sorted.
        Always expensively maintained.
        Always a sign that something went wrong.
        Like a bad date.
        """
        return f"Heap(data={self._data})"


def main() -> None:
    """Demonstrate the heap that sorts itself into exhaustion."""
    print("Heap That Sorts on Every Insert")
    print("=" * 60)

    heap = HeapBySorting()

    print("\nInserting values: 5, 3, 8, 1, 4")
    print("Watch as we sort the entire array on each insert:")
    for value in [5, 3, 8, 1, 4]:
        heap.insert(value)
        print(f"  Inserted {value}, heap state: {heap}")
        print(f"    [Sorted all {len(heap)} elements]")

    print("\nPeeking smallest element (finally, an O(1) operation):")
    print(f"  {heap.peek()}")

    print("\nPopping all elements (enjoying our prepaid sorting cost):")
    while heap:
        print(f"  Popped: {heap.pop()}")

    print("\nPerformance Analysis:")
    print("  Real binary heap inserting 1000 elements:")
    print("    - Each insert: O(log n) ≈ 10 operations")
    print("    - Total: O(n log n) ≈ 10,000 operations")
    print()
    print("  This sorting heap inserting 1000 elements:")
    print("    - Insert 1: sort 1 element")
    print("    - Insert 2: sort 2 elements")
    print("    - Insert 1000: sort 1000 elements")
    print("    - Total: O(n² log n) ≈ 10,000,000 operations")
    print("    - Slowdown: ~1000x")

    print("\nConclusion:")
    print("  We maintained perfect order.")
    print("  We paid for it every single time.")
    print("  This is not a heap.")
    print("  This is a sorted list with commitment issues.")
    print("  Binary heaps exist for a reason.")
    print("  Use heapq. Please.")
    print("=" * 60)

if __name__ == "__main__":
    main()