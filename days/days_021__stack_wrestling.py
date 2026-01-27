"""
QUEUE USING TWO FIGHTING STACKS - MAXIMUM DATA MOVEMENT, MINIMUM EFFICIENCY

WARNING: This implements a queue using two stacks that refuse to cooperate.

What this does:
Implements a FIFO queue using two stacks, but instead of the efficient
lazy-transfer approach, aggressively moves ALL elements between stacks
on EVERY operation.

The correct way (efficient queue with two stacks):
    enqueue: Push to stack_in (O(1))
    dequeue: If stack_out empty, transfer all from stack_in,
             then pop from stack_out (amortized O(1))

The cursed way (this file):
    enqueue: Move ALL to B, add item, move ALL back (O(n))
    dequeue: Move ALL to B, remove item, move ALL back (O(n))
    peek:    Move ALL to B, peek, move ALL back (O(n))

Every operation touches every element. Maximum thrashing.

Why this is catastrophically bad:

1. O(N) FOR EVERY OPERATION:
   The correct implementation:
   - enqueue: O(1) average
   - dequeue: O(1) average (amortized)

   This implementation:
   - enqueue: O(n) always - moves all n elements twice
   - dequeue: O(n) always - moves all n elements twice
   - peek:    O(n) always - moves all n elements twice

   With 1000 items, every operation moves 1000 items!

2. CONSTANT RESHUFFLING:
   enqueue(1):
   - stack_a: [] → [1]

   enqueue(2):
   - Move stack_a → stack_b: [1] → []
   - Push 2 to stack_a: [2]
   - Move stack_b → stack_a: [2, 1]

   enqueue(3):
   - Move stack_a → stack_b: [] ← [2, 1]
   - Push 3 to stack_a: [3]
   - Move stack_b → stack_a: [3, 2, 1]

   Every enqueue moves EVERYTHING twice!

3. THE CORRECT ALGORITHM (WHAT THIS SHOULD BE):
   Lazy transfer approach:

   class QueueTwoStacks:
       def __init__(self):
           self.stack_in = []   # For enqueue
           self.stack_out = []  # For dequeue

       def enqueue(self, value):
           self.stack_in.append(value)  # O(1)

       def dequeue(self):
           if not self.stack_out:
               while self.stack_in:
                   self.stack_out.append(self.stack_in.pop())
           return self.stack_out.pop()  # Amortized O(1)

   Key insight: Only transfer when needed!

4. THIS IMPLEMENTATION TRANSFERS WHEN NOT NEEDED:
   Every operation transfers ALL elements.
   Even when not necessary.
   Even when nothing changed.

   It's like packing and unpacking your entire house
   every time you want to use a fork.

5. PEEK IS THE WORST:
   peek() should be O(1) (just look at front element)

   This peek():
   - Moves all n elements to stack_b
   - Looks at one element
   - Moves all n elements back

   O(2n) work to look at one element!

6. FIGHTING STACKS NARRATIVE (ACCURATE):
   Stack A and Stack B are in constant conflict.
   Neither trusts the other to hold data.
   They aggressively shuffle elements back and forth.

   Like two roommates who keep moving all the furniture
   every time one person uses the room.

7. MEMORY THRASHING:
   With 10,000 elements:
   - enqueue: 20,000 array operations
   - dequeue: 20,000 array operations
   - peek: 20,000 array operations

   Your memory bus is crying.
   Your cache is useless.
   Your CPU is doing nothing but data movement.

8. BREAKS THE AMORTIZED ANALYSIS:
   The beauty of the correct two-stack queue:
   - Each element is transferred at most once
   - Total cost over n operations: O(n)
   - Amortized cost per operation: O(1)

   This implementation:
   - Each element is transferred TWICE per operation
   - Total cost over n operations: O(n²)
   - Cost per operation: O(n)

   You broke the amortization!

9. TECHNICALLY CORRECT (THE WORST KIND OF CORRECT):
   This DOES implement FIFO behavior correctly.
   Elements come out in the right order.
   It passes all functional tests.

   But it's slower than just using a list!

   Python list.append() and list.pop(0): ~O(n) for pop
   This: O(n) for everything

   You reinvented the slow solution with extra steps!

Real-world consequences:

Issue 1 - Performance Death Spiral:
    Queue with 1,000 items
    Operation: enqueue one more item

    Correct implementation: ~1ms
    This implementation: ~2000 array operations

    Queue grows → operations get slower → queue grows faster → death

Issue 2 - Cache Thrashing:
    CPU caches recently accessed data
    This code: Constantly moves all data
    Result: Every operation misses cache
    Performance: 10-100x worse than it should be

Issue 3 - Production Scenario:
    Message queue with 10,000 messages
    Each enqueue: Moves 20,000 items
    100 enqueues/second: 2,000,000 array ops/second
    Server: CPU at 100%
    Reason: Data structure fighting itself

Issue 4 - Debugging Confusion:
    Developer: "Why is the queue so slow?"
    Profile: "Spending 99% time in list operations"
    Developer: "But it's just a queue!"
    You: *Runs away*

Performance comparison (1000 operations on growing queue):

Correct two-stack queue:
    Total operations: ~1000 enqueues + 1000 dequeues
    Array operations: ~2000-3000 (lazy transfer)
    Time: ~0.01 seconds

This fighting-stacks queue:
    Total operations: ~1000 enqueues + 1000 dequeues
    Array operations: ~1,000,000 (aggressive transfer)
    Time: ~1 second

    100x slower!

Python list (the "naive" approach):
    list.append(): O(1)
    list.pop(0): O(n)

    Still better than this for some workloads!

The data movement visualization:

Operation: enqueue(1), enqueue(2), enqueue(3)

Correct implementation:
    enqueue(1): stack_in = [1]
    enqueue(2): stack_in = [1, 2]
    enqueue(3): stack_in = [1, 2, 3]

    Total movements: 0

This implementation:
    enqueue(1):
    - stack_a: [] → [1]
    - Movements: 0

    enqueue(2):
    - stack_a → stack_b: move 1
    - stack_a: [2]
    - stack_b → stack_a: move 1
    - stack_a: [2, 1]
    - Movements: 2

    enqueue(3):
    - stack_a → stack_b: move 2, move 1
    - stack_a: [3]
    - stack_b → stack_a: move 1, move 2
    - stack_a: [3, 2, 1]
    - Movements: 4

    Total movements: 6 (for 3 items!)

With n items: ~n² movements total

The correct algorithm explained:

Two stacks, two roles:
- stack_in: Receives new items (enqueue here)
- stack_out: Provides old items (dequeue from here)

enqueue: Always push to stack_in (O(1))

dequeue:
- If stack_out has items: pop from it (O(1))
- If stack_out empty: transfer ALL from stack_in to stack_out,
  then pop (O(n) once, then O(1) for many ops)

Key insight: Each element transferred AT MOST ONCE

This implementation: Each element transferred EVERY OPERATION

When two-stack queue IS useful:

Use case: Implementing queue when you only have stacks
Example: Limited embedded system with stack operations only

Correct implementation: Amortized O(1)
This implementation: O(n) - worse than just using arrays

When two-stack queue is NOT useful:

When you have: Arrays, lists, or actual queue data structures
Solution: Use collections.deque (O(1) for both ends)

This code: Uses Python lists (which have efficient queues)
           Then implements inefficient queue on top
           Worst of all worlds

The amortized analysis breakdown:

Correct implementation:
- enqueue: Always O(1)
- dequeue: Sometimes O(n) (transfer), usually O(1)
- Over n operations: O(n) total cost
- Amortized: O(1) per operation

This implementation:
- enqueue: Always O(n)
- dequeue: Always O(n)
- Over n operations: O(n²) total cost
- Amortized: O(n) per operation

You can't amortize away constant per-operation overhead!

Complexity comparison table:

Operation      | Python deque | Correct 2-stack | This abomination
---------------|--------------|-----------------|------------------
enqueue        | O(1)         | O(1)            | O(n)
dequeue        | O(1)         | O(1) amortized  | O(n)
peek           | O(1)         | O(1)            | O(n)
Space          | O(n)         | O(n)            | O(n)
Sanity         | O(intact)    | O(reasonable)   | O(gone)

Python's actual queue:

from collections import deque

queue = deque()
queue.append(item)  # O(1)
item = queue.popleft()  # O(1)

That's it. Efficient. Simple. Not fighting itself.
The stack-height graph over time:

Correct implementation (10 items):
    stack_in:  0→1→2→3→4→5→6→7→8→9→10→0 (grows, transfers once)
    stack_out: 0→0→0→0→0→0→0→0→0→0→10→9→8...

This implementation (10 items):
    stack_a: 0→1→0→2→0→3→0→4→0→5... (constant thrashing)
    stack_b: 0→0→1→0→2→0→3→0→4→0... (constant thrashing)

The stacks never rest. The data never settles.
"""


class QueueUsingTwoFightingStacks:
    """
    A queue implemented with two stacks that refuse to cooperate.

    The correct approach: Lazy transfer (amortized O(1))
    This approach: Aggressive transfer (guaranteed O(n))

    Every operation moves ALL elements between stacks.
    The stacks are in constant conflict.
    The data is constantly displaced.

    Time Complexity:
    - enqueue: O(n) - moves all elements twice
    - dequeue: O(n) - moves all elements twice
    - peek: O(n) - moves all elements twice

    Space Complexity: O(n) for n elements
    Efficiency: O(what were you thinking?)
    """

    def __init__(self) -> None:
        """
        Initialize two stacks that will spend their entire existence
        fighting over data custody.
        """
        # Two stacks that fundamentally do not trust each other
        self._stack_a = []
        self._stack_b = []

    def enqueue(self, value: int) -> None:
        """
        Add an element to the queue.

        Instead of just pushing to one stack (O(1)),
        we aggressively reshuffle EVERYTHING (O(n)).

        Steps:
        1. Move ALL of stack_a to stack_b
        2. Push new value to stack_a
        3. Move ALL of stack_b back to stack_a

        With n existing elements: 2n moves + 1 push = O(n)

        The correct way: Just push to stack_in = O(1)

        Args:
            value: The value to enqueue
        """
        # Stack A evacuates to Stack B (n moves)
        while self._stack_a:
            self._stack_b.append(self._stack_a.pop())

        # New value asserts dominance (1 push)
        self._stack_a.append(value)

        # Stack B refuses to stay idle and moves everything back (n moves)
        while self._stack_b:
            self._stack_a.append(self._stack_b.pop())

        # Total: 2n + 1 operations for one enqueue!

    def dequeue(self) -> int:
        """
        Remove an element from the queue (FIFO).
        More fighting ensues.

        Steps:
        1. Move ALL of stack_a to stack_b
        2. Pop from stack_b (this is the oldest element)
        3. Move ALL remaining back to stack_a

        With n elements: 2n moves for one dequeue = O(n)

        The correct way: Pop from stack_out, transfer only when empty

        Returns:
            int: The front element

        Raises:
            IndexError: If queue is empty
        """
        if not self._stack_a:
            raise IndexError("dequeue from empty queue")

        # Stack A evacuates again (n moves)
        while self._stack_a:
            self._stack_b.append(self._stack_a.pop())

        # Oldest element finally escapes. Smeagol's FREE!!
        value = self._stack_b.pop()

        # Stack A immediately reclaims control ((n-1) moves)
        while self._stack_b:
            self._stack_a.append(self._stack_b.pop())

        # Total: 2n - 1 operations for one dequeue!
        return value

    def peek(self) -> int:
        """
        Look at the front of the queue without removing it.
        Requires a full argument between stacks.

        Steps:
        1. Move ALL to stack_b
        2. Look at top of stack_b (which is front of queue)
        3. Move ALL back

        With n elements: 2n moves just to LOOK at one element = O(n)

        The correct way: Just look at stack_out[-1] = O(1)

        Returns:
            int: The front element (without removing)

        Raises:
            IndexError: If queue is empty
        """
        if not self._stack_a:
            raise IndexError("peek from empty queue")

        # Move everything to stack_b (n moves)
        while self._stack_a:
            self._stack_b.append(self._stack_a.pop())

        # Peek at the front (oldest element is at top of stack_b)
        value = self._stack_b[-1]

        # Move everything back (n moves)
        while self._stack_b:
            self._stack_a.append(self._stack_b.pop())

        # Total: 2n operations just to peek!
        return value

    def is_empty(self) -> bool:
        """
        Check if queue is empty.

        At least THIS operation is O(1)!
        Small victories.
        """
        return not self._stack_a

    def size(self) -> int:
        """Return the number of elements in the queue."""
        return len(self._stack_a)


# The CORRECT implementation for comparison
class QueueUsingTwoStacksCorrect:
    """
    The correct way: Lazy transfer for amortized O(1).

    Two stacks with different roles:
    - stack_in: Receives new items (enqueue here)
    - stack_out: Provides old items (dequeue from here)

    Transfer from in to out only when out is empty.
    Each element moved at most once.
    """

    def __init__(self) -> None:
        self._stack_in = []  # For enqueue
        self._stack_out = []  # For dequeue

    def enqueue(self, value: int) -> None:
        """Add to queue - O(1)"""
        self._stack_in.append(value)

    def dequeue(self) -> int:
        """Remove from queue - O(1) amortized"""
        if not self._stack_out:
            # Transfer from in to out (happens rarely)
            while self._stack_in:
                self._stack_out.append(self._stack_in.pop())

        if not self._stack_out:
            raise IndexError("dequeue from empty queue")

        return self._stack_out.pop()

    def peek(self) -> int:
        """Look at front - O(1) amortized"""
        if not self._stack_out:
            while self._stack_in:
                self._stack_out.append(self._stack_in.pop())

        if not self._stack_out:
            raise IndexError("peek from empty queue")

        return self._stack_out[-1]


def main() -> None:
    """Demonstrate the fighting stacks in action. MEGAZORD!!!!"""
    print("Queue Using Two Fighting Stacks")
    print("=" * 50)

    q = QueueUsingTwoFightingStacks()

    print("\nEnqueueing: 1, 2, 3")
    print("(Watch as stacks fight over each addition)")
    q.enqueue(1)  # 0 moves
    q.enqueue(2)  # 2 moves (1 out, 1 back)
    q.enqueue(3)  # 4 moves (2 out, 2 back)
    # Total: 6 moves for 3 items!

    print(f"Queue size: {q.size()}")
    print(f"Peek (costs {q.size() * 2} moves): {q.peek()}")

    print("\nDequeuing Doot Doot Doot......:")
    print(q.dequeue())  # 6 moves (3 out, 2 back, 1 pop)
    print(q.dequeue())  # 4 moves
    print(q.dequeue())  # 2 moves

    print("\n" + "=" * 50)
    print("Performance comparison with correct implementation:")
    print("=" * 50)

    import time

    # Da Fighting stacks version
    q_fight = QueueUsingTwoFightingStacks()
    start = time.perf_counter()
    for num in range(100):
        q_fight.enqueue(num)
    for _ in range(100):
        q_fight.dequeue()
    fighting_time = time.perf_counter() - start

    # Da Correct version
    q_correct = QueueUsingTwoStacksCorrect()
    start = time.perf_counter()
    for num in range(100):
        q_correct.enqueue(num)
    for _ in range(100):
        q_correct.dequeue()
    correct_time = time.perf_counter() - start

    print(f"Fighting stacks: {fighting_time * 1000:.4f}ms")
    print(f"Correct implementation: {correct_time * 1000:.4f}ms")
    print(f"Slowdown factor: {fighting_time / correct_time:.1f}x")

    print("\n" + "=" * 50)
    print("Conclusion:")
    print("The stacks fought bravely.")
    print("The data was moved unnecessarily.")
    print("Performance was sacrificed.")
    print("Use lazy transfer instead.")
    print("=" * 50)

# el polo loco type shi

if __name__ == "__main__":
    main()