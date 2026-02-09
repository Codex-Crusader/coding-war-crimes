"""
CIRCULAR BUFFER THAT SHIFTS THE ENTIRE ARRAY ON EVERY PUSH - BECAUSE O(1) IS BORING

WARNING: This implementation maintains a circular buffer by shifting all elements
         left on every insertion. O(1) push becomes O(n).
         Array copying as a lifestyle choice.

What this does:
Implements a circular buffer by keeping everything in order at all times through
aggressive array shifting instead of using index arithmetic.

The correct way:
    Use modulo arithmetic. Track head pointer. O(1) push and get.

The cursed way:
    Shift entire array left on every push. O(n) push. Zero math required.

Why this is terrible:
- Push one element: shift all n elements left
- Real circular buffer: update one pointer
- This version: copy n elements in memory
- For n pushes: O(n²) total instead of O(n)
- Cache misses everywhere
- Memory writes dominate

Performance Comparison (1,000 element buffer):
    Real circular buffer:
        - 1000 pushes: ~0.1ms (just pointer updates)
        - Get by index: O(1) with modulo

    This shifting buffer:
        - 1000 pushes: ~500ms (shift array 1000 times)
        - Get by index: O(1) (at least we got this right)
        - Slowdown: 5000x

Real-World Impact:
    Small buffer (10 items):     Barely noticeable
    Medium buffer (1000 items):  Multi-second delays
    Large buffer (100k items):   Application freezes

What We Learn:
- Index arithmetic exists for a reason
- Copying arrays repeatedly is expensive
- O(1) with simple math beats O(n) with simple logic
- Physical order ≠ logical order
- Modulo is your friend

The Irony:
    We eliminated all the "confusing" modulo math.
    In exchange, we shift gigabytes of data.
    Congratulations, we traded thinking for copying.

Usage:
    DO use for: Understanding why circular buffers use wraparound
    DO NOT use for: Ring buffers, audio processing, logging queues

P.S: I could have used (head + 1) % capacity like a normal person.
     Instead I chose to shift the entire array on every push.
     This is paying for simplicity with performance.

"""


class CursedCircularBuffer:
    """
    A circular buffer that maintains order by shifting the entire array on every push.

    This is the brute-force approach to circular buffers:
    - No wraparound
    - No modulo arithmetic
    - No head/tail pointers
    - Just shift everything left on every push

    Properties:
    - Always in perfect order (expensive)
    - No index math required (we pay with copies)
    - Get is O(1) (because we sorted our problems earlier)
    - Push is O(n) (we pay here instead)

    Time Complexity:
        push(): O(n) - shift entire array left
        get():  O(1) - direct array access

    Compare to real circular buffer:
        push(): O(1) - just update pointer
        get():  O(1) - with modulo arithmetic

    Space Complexity:
        O(n) - same as normal circular buffer
        But we thrash the cache on every push

    This implementation trades algorithmic efficiency for
    conceptual simplicity. The trade is bad.
    """

    def __init__(self, capacity: int) -> None:
        """
        Initialize the circular buffer.

        Args:
            capacity: Maximum number of items to store

        Raises:
            ValueError: If capacity <= 0

        Notes:
            We create a fixed-size array like a normal circular buffer.
            The difference is what we do with it.
            Normal: use it efficiently with modulo
            This: shift it repeatedly like we're punishing it
        """
        if capacity <= 0:
            raise ValueError("capacity must be > 0")

        self.capacity = capacity
        self.buffer = [None] * capacity
        self.size = 0  # how many valid items we have

    def push(self, value) -> None:
        """
        Add an item to the buffer.

        What a real circular buffer does:
            1. Write to buffer[head]
            2. Update head = (head + 1) % capacity
            3. Total: O(1)

        What this does:
            1. Shift everything left: buffer[i] = buffer[i+1]
            2. Write to last position
            3. Total: O(n)

        Args:
            value: Item to add

        Time Complexity: O(n) - shift entire array
        What It Should Be: O(1)
        Efficiency Loss: Factor of n

        Process:
            Buffer before: [A, B, C, _, _]
            Push D:
                Step 1: Shift left → [B, C, _, _, _]
                Step 2: Write D → [B, C, D, _, _]

            We copied 2 elements to add 1 element.
            For a full buffer, we copy n elements to add 1.

        Notes:
            Every push moves (capacity - 1) elements in memory.
            For capacity = 1000, each push moves 999 elements.
            Push 1000 times = move ~1,000,000 elements total.

            A real circular buffer with capacity 1000:
            - Push 1000 times = update 1 pointer 1000 times
            - Total work: 1000 operations

            This circular buffer with capacity 1000:
            - Push 1000 times = shift 999 elements each time
            - Total work: ~1,000,000 operations
            - Slowdown: ~1000x

        Example:
            capacity = 5, buffer is [1, 2, 3, 4, 5]
            push(6):
                - Shift: buffer[0] = buffer[1]  (2)
                - Shift: buffer[1] = buffer[2]  (3)
                - Shift: buffer[2] = buffer[3]  (4)
                - Shift: buffer[3] = buffer[4]  (5)
                - Write: buffer[4] = 6
                - Result: [2, 3, 4, 5, 6]
                - Elements copied: 4
                - Elements added: 1
                - Efficiency: 20%
        """
        if self.size < self.capacity:
            # Buffer not full yet, just append
            self.buffer[self.size] = value
            self.size += 1
        else:
            # Buffer full: shift everything left, then write at end
            # This is the cursed part
            for i in range(self.capacity - 1):
                self.buffer[i] = self.buffer[i + 1]  # O(n) array copying
                # time complexity f**ks itself over here

            # Write new value at the end
            self.buffer[self.capacity - 1] = value

    def get(self, index: int):
        """
        Get item by logical index (0 = oldest item).

        At least this part is efficient because we maintain
        perfect order through our aggressive shifting strategy.

        Args:
            index: Logical index (0 to size-1)

        Returns:
            Item at the given index

        Raises:
            IndexError: If index out of range

        Time Complexity: O(1)
        Hidden Cost: The O(n) we paid during push

        Notes:
            This is fast ONLY because we paid the cost during push.
            We've traded write performance for read performance.

            For most circular buffers, this is the wrong trade-off:
            - Usually: many writes, few reads
            - This design: optimizes reads, destroys writes

            It's like hiring a team to alphabetize your bookshelf
            every time you add a book, so finding books is fast.
            Technically correct. Economically insane.
        """
        if index < 0 or index >= self.size:
            raise IndexError("index out of range")

        # Direct access because we maintain perfect order
        # No modulo math required
        # We traded the math for array copying
        # trade deal: you receive - Bad Performance, I receive - your suffering
        return self.buffer[index]

    def to_list(self):
        """
        Return contents from oldest to newest as a list.

        Time Complexity: O(n)

        This is efficient because our buffer is already in order.
        We paid for that order with O(n) operations on every push.
        """
        return [self.buffer[i] for i in range(self.size)]

    def __len__(self) -> int:
        """Return number of items in buffer."""
        return self.size

    def __repr__(self) -> str:
        """
        Return string representation.

        Shows the buffer contents in their perfectly maintained order.
        Order maintained through blood, sweat, and array copying.
        """
        return f"CursedCircularBuffer({self.to_list()})"


def main() -> None:
    """Demonstrate the circular buffer that shifts itself into exhaustion."""
    print("Circular Buffer That Shifts on Every Push")
    print("=" * 60)

    buffer = CursedCircularBuffer(capacity=5)

    print("\nPushing values to non-full buffer:")
    for value in [1, 2, 3]:
        buffer.push(value)
        print(f"  Pushed {value}: {buffer}")
        print(f"    [No shifting yet, buffer not full]")

    print("\nFilling the buffer:")
    for value in [4, 5]:
        buffer.push(value)
        print(f"  Pushed {value}: {buffer}")

    print("\nNow the buffer is full. Watch the shifting begin:")
    for value in [6, 7, 8]:
        print(f"\n  Pushing {value}:")
        print(f"    Before: {buffer.to_list()}")
        buffer.push(value)
        print(f"    After:  {buffer.to_list()}")
        print(f"    [Shifted {buffer.capacity - 1} elements left]")

    print("\nGetting elements by index (at least this is O(1)):")
    for i in range(len(buffer)):
        print(f"  buffer.get({i}) = {buffer.get(i)}")

    print("\nPerformance Analysis:")
    print("  Real circular buffer (capacity 1000):")
    print("    - Push 1000 items: ~1000 pointer updates")
    print("    - Total operations: ~1000")
    print()
    print("  This shifting buffer (capacity 1000):")
    print("    - Push 1: shift 0 elements")
    print("    - Push 2: shift 1 element")
    print("    - ...")
    print("    - Push 1000: shift 999 elements")
    print("    - Push 1001: shift 999 elements (buffer full)")
    print("    - Total shifts for 1000 pushes: ~500,000 elements moved")
    print("    - Slowdown: ~500x")

    print("\nMemory Access Pattern:")
    print("  Real circular buffer:")
    print("    - Write to one location")
    print("    - Update one integer (head pointer)")
    print("    - Cache friendly")
    print()
    print("  This shifting buffer:")
    print("    - Write to every location except the first")
    print("    - Copy (n-1) elements")
    print("    - Cache thrashing")

    print("\nConclusion:")
    print("  We eliminated modulo arithmetic.")
    print("  In exchange, we copy arrays constantly.")
    print("  Reads are fast because writes are slow.")
    print("  This is the wrong trade-off for most use cases.")
    print("  Modulo is cheaper than memcpy.")
    print("  Use real circular buffers. Please.")


if __name__ == "__main__":
    main()