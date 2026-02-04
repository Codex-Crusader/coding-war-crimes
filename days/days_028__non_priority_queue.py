"""
PRIORITY QUEUE THAT SORTS ON EVERY POP - THE PROCRASTINATOR'S DATA STRUCTURE

WARNING: This implementation delays all work until pop(), then does it all at once.
         Push is O(1). Pop is O(n log n). Every single time.
         Your CPU will file a grievance.

What this does:
Implements a priority queue by storing items unsorted, then sorting the entire
list every time you pop or peek.

The correct way:
    Use a binary heap. Push in O(log n), pop in O(log n).

The cursed way:
    Push in O(1) (just append), pop in O(n log n) (sort everything).

Why this is terrible:
- Push is fast but builds up debt
- Pop is catastrophically slow (sorts entire list)
- Peek also sorts entire list (destroys idempotence)
- Popping n items: sort n times = O(n² log n)
- Real heap popping n items: O(n log n)
- Slowdown factor: n

Performance Comparison (1,000 elements):
    Real heap:
        - 1000 pushes: ~0.5ms total
        - 1000 pops: ~0.5ms total
        - Total: ~1ms

    This queue:
        - 1000 pushes: ~0.1ms total (fast!)
        - 1000 pops: ~5000ms total (disaster!)
        - Total: ~5000ms
        - Slowdown: 5000x

Real-World Impact:
    Small queue (100 items):    Multi-second pop operations
    Medium queue (10,000):      Minutes per pop
    Large queue (1M):           Hours per pop, eventual crash

What We Learn:
- Deferring work doesn't eliminate it
- O(1) push + O(n log n) pop < O(log n) push + O(log n) pop
- Sorting repeatedly is worse than maintaining order
- Compound interest applies to algorithms too

The Irony:
    This is the opposite of the heap-by-sorting approach.
    That one: sort on insert, fast pop
    This one: fast insert, sort on pop
    Both are wrong. Neither is clever.

Usage:
    DO use for: Understanding why heaps maintain partial order
    DO NOT use for: Task schedulers, event loops, Dijkstra's algorithm

P.S: I could have maintained a heap property incrementally.
     Instead, I chose to procrastinate and sort everything later.
     This is algorithmic technical debt at maximum interest.
     I think.... *wink wink*
"""

from typing import List, Any


class PriorityQueueBySortingOnPop:
    """
    A priority queue that appends items unsorted and sorts the entire list on every pop.

    This is the procrastinator's approach to data structures:
    - Do nothing during insert (O(1))
    - Panic and do everything during pop (O(n log n))
    - Repeat the panic every single time

    Properties:
    - push(): O(1) - just append, no work
    - pop():  O(n log n) - sort entire list every time
    - peek(): O(n log n) - sort entire list just to look

    Compare to real heap:
    - push(): O(log n) - incremental work
    - pop():  O(log n) - incremental work
    - peek(): O(1) - just look at root

    This implementation delays all work until pop(),
    then does ALL of it at once. Repeatedly.
    Like cramming for an exam every. single. day.
    """

    def __init__(self) -> None:
        """
        Initialize the priority queue.

        Just an unsorted list. No structure. No order. Pure chaos.
        The chaos will be resolved later. Violently.
        """
        self._data: List[Any] = []

    def push(self, value: Any) -> None:
        """
        Insert a value into the priority queue.

        What a real priority queue does:
            Insert and sift up: O(log n)
            Maintains heap property incrementally

        What this does:
            Append and hope for the best: O(1)
            Maintains nothing
            Defers all consequences

        Args:
            value: Element to insert

        Time Complexity: O(1) - suspiciously fast
        Hidden Cost: Debt accumulates for later

        Notes:
            This is fast. Too fast. Unsustainably fast.
            We're not doing the work, we're just delaying it.
            Every push adds to the unsorted chaos.
            The bill comes due at pop().
            With interest.
            Compound interest.

        Example:
            Push 1000 items: 1000 × O(1) = O(n) total
            Looks great on paper.
            The reckoning comes later.
        """
        self._data.append(value)  # O(1): Suspiciously easy

    def pop(self) -> Any:
        """
        Remove and return the smallest element.

        What a real heap does:
            1. Take root (min element) - O(1)
            2. Move last element to root - O(1)
            3. Sift down to restore heap - O(log n)
            Total: O(log n)

        What this does:
            1. Sort entire list - O(n log n)
            2. Pop first element - O(n) (shift entire list)
            3. Repeat on every pop - O(regret)

        Returns:
            Smallest element

        Raises:
            IndexError: If queue is empty

        Time Complexity: O(n log n) PER POP
        What It Should Be: O(log n)
        Efficiency Loss: Factor of n/log(n)

        Notes:
            Pop one element: sort all n elements.
            Pop again: sort all n-1 elements.
            Pop n times total: sort n + (n-1) + (n-2) + ... + 1 elements
            Total work: O(n² log n)

            A real heap popping n items: O(n log n)
            This queue popping n items: O(n² log n)

            For n=1000:
            - Real heap: ~10,000 operations
            - This queue: ~10,000,000 operations
            - Slowdown: ~1000x

        Example:
            Queue has 1,000,000 elements.
            You pop once.
            We sort all 1,000,000 elements (~20,000,000 comparisons).
            You pop again.
            We sort all 999,999 elements again (~19,999,980 comparisons).
            This is not sustainable.
            MUHAHAHAHAHA!
            what differentiates a super villain from a villain?
            PRESENTATION!!
        """
        if not self._data:
            raise IndexError("pop from empty priority queue")

        # Nuclear option: sort everything every time
        self._data.sort()  # O(n log n): The panic button
        return self._data.pop(0)  # O(n): Shift entire list left

    def peek(self) -> Any:
        """
        Return the smallest element without removing it.

        Still sorts the entire list first, because consistency matters.
        Even when that consistency is consistently terrible.

        Returns:
            Smallest element

        Raises:
            IndexError: If queue is empty

        Time Complexity: O(n log n)
        What It Should Be: O(1)

        Notes:
            Peek is supposed to be a read-only operation.
            It shouldn't modify anything.
            It should be O(1).

            Instead, we sort the entire list.
            This violates idempotence.
            Calling peek() multiple times sorts multiple times.

            peek()  # Sort everything
            peek()  # Sort everything again
            peek()  # Sort everything AGAIN

            In a real heap, peek() is O(1) and can be called freely.
            Here, every peek() is O(n log n).

            If you peek() in a tight loop, you're sorting repeatedly.
            This is algorithmic self-harm.
        """
        if not self._data:
            raise IndexError("peek from empty priority queue")

        self._data.sort()  # O(n log n): Unnecessary but committed
        return self._data[0]

    def __len__(self) -> int:
        """Return number of elements in the queue."""
        return len(self._data)

    def __bool__(self) -> bool:
        """Return True if queue is non-empty."""
        return bool(self._data)

    def __str__(self) -> str:
        """
        Return internal state.

        Usually unsorted chaos.
        Momentarily sorted when we panic during pop.
        Then chaos again after next push.
        """
        return f"PriorityQueue(data={self._data})"


def main() -> None:
    """Demonstrate the priority queue that procrastinates catastrophically."""
    print("Priority Queue That Sorts on Every Pop")
    print("=" * 60)

    pq = PriorityQueueBySortingOnPop()

    print("\nPushing values: 5, 1, 4, 2, 3")
    print("(Fast because we're not doing any real work)")
    for v in [5, 1, 4, 2, 3]:
        pq.push(v)
        print(f"  Pushed {v}, internal: {pq} (unsorted chaos)")

    print("\nPeeking (sorts entire list just to look):")
    print(f"  peek() = {pq.peek()} [sorted {len(pq)} elements]")
    print(f"  peek() = {pq.peek()} [sorted {len(pq)} elements AGAIN]")

    print("\nPopping values (each pop sorts the entire remaining list):")
    pop_count = 0
    while pq:
        size_before = len(pq)
        value = pq.pop()
        pop_count += 1
        print(f"  Pop #{pop_count}: got {value} [sorted {size_before} elements]")

    print("\nPerformance Analysis:")
    print("  Real priority queue (binary heap):")
    print("    - push(): O(log n)")
    print("    - pop():  O(log n)")
    print("    - peek(): O(1)")
    print()
    print("  This implementation:")
    print("    - push(): O(1) - too good to be true")
    print("    - pop():  O(n log n) - the truth hurts")
    print("    - peek(): O(n log n) - even worse")
    print()
    print("  Popping all n items:")
    print("    - Real heap: O(n log n) total")
    print("    - This queue: O(n² log n) total")
    print("    - We sort: n + (n-1) + (n-2) + ... + 1 times")
    print("    - Sum of first n numbers = n(n+1)/2 ≈ n²/2")
    print("    - Each sort: O(n log n)")
    print("    - Total: O(n² log n)")

    print("\nWhy This Is Bad:")
    print("  - Deferred work doesn't disappear")
    print("  - It accumulates interest")
    print("  - Sorting n items n times is worse than maintaining order")
    print("  - O(1) push is a trap when pop is O(n log n)")
    print("  - This is technical debt at maximum interest rate")

    print("\nConclusion:")
    print("  We postponed the work.")
    print("  The work did not go away.")
    print("  It came back with compound interest.")
    print("  Incremental maintenance beats deferred panic.")
    print("  Use heapq. Please.")
    print("=" * 60)


if __name__ == "__main__":
    main()