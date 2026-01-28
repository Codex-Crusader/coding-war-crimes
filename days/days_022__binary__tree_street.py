"""
BINARY TREE AS CSV STRING - STORING A TREE IN A COMMA-SEPARATED VALUE

WARNING: This implements a binary tree as a single comma-separated string.

What this does:
Stores a binary tree as "1,2,3,4,5,6,7" using level-order indexing.
Every operation parses the string, does work, and rebuilds the string.

The correct way:
    class TreeNode:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None

Pointers to actual nodes. O(1) access. Industry standard.

The cursed way:
    tree = "1,2,3,4,5,6,7"

Parse string on every access. O(n) for everything. Pure pain.

Why this is catastrophically bad:

1. STRING PARSING ON EVERY OPERATION:
   Get root value:
   - Parse entire string: "1,2,3,4,5,6,7" → ["1","2","3","4","5","6","7"]
   - Get first element: "1"
   - Convert to int: 1
   - Return

   Could be: node.val (direct memory access, O(1))
   Instead: String split, indexing, type conversion (O(n))

2. CONSTANT TYPE CONVERSIONS:
   Storing: int → str → concatenate into CSV
   Reading: Parse CSV → str → int

   Every value goes through 2-3 type conversions per operation.

   With actual nodes: int stored as int, accessed as int
   With this: int → str → int on every access

3. REBUILD ENTIRE TREE ON INSERT:
   insert(8):
   - Parse: "1,2,3,4,5,6,7" → list
   - Append: list.append("8")
   - Rebuild: ",".join() → "1,2,3,4,5,6,7,8"

   With 1000 nodes: Parse 1000 items, append 1, rebuild 1001-item string

   Actual tree: node.left = TreeNode(8) - O(1)

4. NO ACTUAL TREE BENEFITS:
   Binary trees provide:
   - O(log n) search (in balanced trees)
   - O(1) node traversal (follow pointers)
   - Easy insertion/deletion

   This implementation:
   - O(n) for all operations (parse entire string)
   - No fast traversal (rebuild on every access)
   - Slow insertion (rebuild entire string)

5. ARRAY-BASED INDEXING FORMULA:
   Left child: 2 * i + 1
   Right child: 2 * i + 2

   This is the heap/array representation.
   If using array representation, just use an array!

   Don't convert array → string → array on every operation!

6. MEMORY WASTE:
   Integer 123: 28 bytes as Python int
   String "123": 52 bytes as Python str (with overhead)

   Plus comma: +1 byte per node
   Plus rebuild operations: Allocate new strings constantly

   Memory usage: 2-3x a normal tree
   Plus: Temporary allocations on every operation

7. TRAVERSAL PERFORMANCE:
   inorder_traversal():
   - Parse string to list (O(n))
   - Recursively walk indices (O(n))
   - Convert each value str→int (O(n))

   Total: O(n) parse + O(n) walk + O(n) conversions

   Actual tree: Just walk pointers, O(n) once

8. NO DELETIONS POSSIBLE:
   Try to delete a node from "1,2,3,4,5,6,7"

   Problems:
   - Can't just remove from middle (breaks indexing)
   - Can't mark as deleted easily
   - Would need "1,2,None,4,5,6,7" representation
   - Then parse "None" strings everywhere

   This only supports insert and read!

9. SPARSE TREES ARE HORRIBLE:
   Unbalanced tree:
        1
       /
      2
     /
    3

   Storage: "1,2,None,3"

   Deep unbalanced tree (depth 10):
   Storage: "1,2,None,3,None,None,None,4,..."
   Would need exponential "None" placeholders!

10. CONCURRENT ACCESS NIGHTMARE:
    Thread A: Reads tree (parsing string)
    Thread B: Inserts node (rebuilds string)
    Thread A: Gets corrupted data mid-parse

    Strings are immutable but replacements aren't atomic.
    Race conditions everywhere.

Real-world consequences:

Issue 1 - Performance:
    1000-node tree:
    - Get root: Parse 1000 items to get item 0
    - Get any node: Parse 1000 items
    - Insert: Parse 1000, append 1, rebuild 1001

    Actual tree:
    - Get root: One pointer dereference
    - Get any node: Follow pointers
    - Insert: Create node, assign pointer

Issue 2 - Memory Thrashing:
    Every operation:
    1. Allocate temporary list (n items)
    2. Process
    3. Allocate new string (n items)
    4. Garbage collect old string

    With frequent operations: Constant allocation/deallocation
    GC pressure: Maximum

Issue 3 - Type Safety Gone:
    tree = "1,2,3,4,hello,6,7"

    Insertion: Accepts anything (it's a string!)
    Runtime error: Only on access when int() fails

    Actual tree with type hints: Compile-time checking

Issue 4 - Debugging:
    Bug: "Tree traversal returns wrong values"

    With this: Is it parsing? String building? Index math? Type conversion?
    With actual tree: Follow pointers, inspect nodes, done

Issue 5 - Production Scenario:
    Binary search tree with 10,000 nodes
    Each search: Parse 10,000-item CSV
    100 searches/second: 1,000,000 string operations/second
    Server: CPU at 100% doing string parsing
    Users: Wondering why search is slow

The array-based tree (what this resembles):

Array representation IS valid for heaps:
    heap = [1, 2, 3, 4, 5, 6, 7]

Left child of i: heap[2*i + 1]
Right child of i: heap[2*i + 2]

This is good for:
- Heaps (complete binary trees)
- Dense trees (few gaps)
- Fixed-size trees

This is bad when:
- You convert array to/from string constantly (this code)
- Tree is sparse
- Need deletions

If using array representation, just use the array!
Don't stringify it!

Performance comparison (1000-node tree, 100 operations):

Method 1 - Actual tree nodes:
    class TreeNode:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None

    Operations: Direct pointer access
    Time: ~0.001 seconds
    Memory: ~28KB (node objects)

Method 2 - Array-based (correct):
    tree = [1, 2, 3, 4, 5, ...]

    Operations: Array indexing
    Time: ~0.002 seconds
    Memory: ~8KB (compact integers)

Method 3 - This CSV abomination:
    tree = "1,2,3,4,5,..."

    Operations: Parse, convert, rebuild
    Time: ~0.1 seconds (50x slower!)
    Memory: ~16KB + constant allocations

The overhead breakdown:

Getting root value from 1000-node tree:

Actual tree:
    return self.root.val

    Steps: 1 (pointer dereference)
    Time: Nanoseconds

This implementation:
    values = self._tree.split(",")  # Parse entire string
    return int(values[0])           # Convert to int

    Steps:
    1. Allocate list for 1000 items
    2. Split string into 1000 strings
    3. Index into list
    4. Convert string to int

    Time: Microseconds (1000x slower)
    It's all coming together.....

Inserting into 1000-node tree:

Actual tree:
    # Navigate to insertion point
    current = self.root
    while current.left or current.right:
        current = current.left  # or right
    current.left = TreeNode(value)

    Steps: Follow pointers, create node, assign
    Time: O(height) typically O(log n)

This implementation:
    values = self._as_list()        # Parse 1000 items
    values.append(str(value))       # Append 1
    self._tree = ",".join(values)   # Rebuild 1001-item string

    Steps:
    1. Split 1000-item string
    2. Append one item
    3. Join 1001 items back to string

    Time: O(n) always

When CSV storage IS appropriate:

1. Persisting to disk:
    Save tree to file as CSV for human readability

    Then: Load into proper tree structure for operations

2. Data interchange:
    Send tree data to another system

    Format as CSV for transmission
    Recipient builds proper tree

3. Debugging/logging:
    Print tree state for debugging

    CSV is readable format

When CSV storage is NOT appropriate:

1. Runtime data structure (this file!)
2. Frequent modifications
3. Performance-critical operations
4. When you need actual tree benefits

The correct implementations:

Option 1 - Standard tree nodes:
    class TreeNode:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None

    class BinaryTree:
        def __init__(self):
            self.root = None

Option 2 - Array-based (for heaps):
    class BinaryHeap:
        def __init__(self):
            self.heap = []

        def get_left(self, i):
            left = 2 * i + 1
            return self.heap[left] if left < len(self.heap) else None

Option 3 - If you want level-order storage:
    class BinaryTree:
        def __init__(self):
            self.values = []  # NOT a string!

        def insert(self, val):
            self.values.append(val)  # int, not str!

All better than storing as CSV string.

Python string operations cost:

split():
    - Scans entire string
    - Allocates list
    - Allocates substring for each element
    - O(n) time, O(n) space

join():
    - Calculates total length
    - Allocates new string
    - Copies all substrings
    - O(n) time, O(n) space

On every operation:
    O(n) parse + O(work) + O(n) rebuild

The type conversion overhead:

Storing int 42:
    int → str: str(42) → "42"
    Append to list: ["1", "2", "42"]
    Join: "1,2,42"

Reading int 42:
    Split: "1,2,42" → ["1", "2", "42"]
    Index: "42"
    Convert: int("42") → 42

Every value: 2-3 conversions per operation

Real-world analogy:

This is like:
- Storing your file system as a text file
- Every file operation: Parse entire text file
- Find your file
- Do operation
- Rebuild entire text file
- Write it back

Instead of: Actual directory structure with pointers

The sparse tree problem:

Balanced tree (7 nodes):
    Storage: "1,2,3,4,5,6,7"
    Length: 13 characters

Sparse tree (7 nodes, left-heavy):
         1
        /
       2
      /
     3
    /
   4
  /
 5

Array representation: [1, 2, None, 3, None, None, None, 4, ...]
String representation: "1,2,None,3,None,None,None,4,..."

With depth d, need 2^d - 1 slots
Depth 10: 1023 slots for 10 nodes!

Historical context:

Array-based trees were used when:
- Memory was expensive
- Pointers were costly
- Trees were dense (heaps)

Modern systems:
- Memory is cheap
- Pointers are optimized
- Flexibility matters more

Storing as string was never a good idea.
Even in the 1960s.

Educational value:
- Shows what NOT to do with trees
- Demonstrates cost of constant parsing
- Illustrates why proper data structures exist
- Proves serialization format ≠ runtime format

The cache nightmare:

CPU caches work well with:
- Sequential access (arrays)
- Localized access (trees with node locality)

This code:
- Parses entire string (not sequential)
- Allocates temporary data (no locality)
- Converts types (cache misses)
- Rebuilds strings (destroys cache)

Result: Every operation misses cache
"""


class BinaryTreeAsString:
    """
    A binary tree stored as a comma-separated string.

    Structure: Level-order traversal as CSV
    Example: "1,2,3,4,5,6,7" represents:
             1
           /   \
          2     3
         / \   / \
        4   5 6   7

    Why this is terrible:
    - Every operation parses the entire string
    - Every operation rebuilds the entire string
    - O(n) complexity for operations that should be O(1)
    - Constant memory allocation/deallocation
    - Type conversions everywhere

    Time Complexity:
    - insert: O(n) - parse all, append, rebuild all
    - get_root: O(n) - parse all to get first element
    - get_left/right: O(n) - parse all for index math
    - traversal: O(n²) - parse on every recursive call

    Space Complexity: O(n) + temporary allocations

    The entire tree. One string. Commas are doing all the work.
    Being a CSE major is hard...
    Proving I know all this is exhausting me at this point
    """

    def __init__(self, data: str = "") -> None:
        """
        Initialize tree from CSV string.

        Args:
            data: Comma-separated values representing level-order tree
        """
        # The entire tree.
        # One string.
        # Commas are doing all the work.
        self._tree = data

    def _as_list(self) -> list[str]:
        """
        Parse the CSV string into a list.

        Called on EVERY operation.
        Allocates new list every time.
        Returns strings, not ints (more conversions needed).

        Returns:
            list[str]: Parsed values as strings
        """
        if not self._tree:
            return []
        return self._tree.split(",")

    def _save(self, values: list[str]) -> None:
        """
        Rebuild the CSV string from list.

        Called on EVERY mutation.
        Allocates new string every time.
        Old string becomes garbage.

        Args:
            values: List of string values to join
        """
        self._tree = ",".join(values)

    def insert(self, value: int) -> None:
        """
        Insert value using level-order logic.

        Steps:
        1. Parse entire string to list (O(n))
        2. Append new value (O(1))
        3. Rebuild entire string (O(n))

        Total: O(n) to insert one value

        Actual tree: O(1) to create node and assign pointer

        No nodes.
        No pointers.
        Just append and pray.

        Args:
            value: Integer value to insert
        """
        values = self._as_list()
        values.append(str(value))
        self._save(values)

    def get_root(self) -> int:
        """
        Get the root value.

        Steps:
        1. Parse entire string (O(n))
        2. Get first element (O(1))
        3. Convert to int (O(1))

        Total: O(n) to get the root

        Actual tree: return self.root.val - O(1)

        Raises:
            ValueError: If tree is empty

        Returns:
            int: Root value
        """
        if not self._tree:
            raise ValueError("Tree is empty")
        return int(self._as_list()[0])

    def get_left(self, index: int) -> int | None:
        """
        Get left child of node at index.

        Uses heap indexing: left child at 2*i + 1

        Steps:
        1. Parse entire string (O(n))
        2. Calculate index
        3. Check bounds
        4. Convert to int

        Total: O(n) for one child lookup

        Actual tree: return node.left.val - O(1)

        Args:
            index: Index of parent node

        Returns:
            int | None: Left child value or None if doesn't exist
        """
        values = self._as_list()
        left = 2 * index + 1
        if left >= len(values):
            return None
        return int(values[left])

    def get_right(self, index: int) -> int | None:
        """
        Get right child of node at index.

        Uses heap indexing: right child at 2*i + 2

        Steps: Same as get_left, equally inefficient

        Args:
            index: Index of parent node

        Returns:
            int | None: Right child value or None if doesn't exist
        """
        values = self._as_list()
        right = 2 * index + 2
        if right >= len(values):
            return None
        return int(values[right])

    def inorder_traversal(self) -> list[int]:
        """
        In-order traversal implemented by repeatedly
        converting strings into lists.

        For each recursive call:
        1. Parse string to list (O(n))
        2. Do recursive work

        With O(n) calls, total: O(n²)

        Actual tree: O(n) - visit each node once

        Performance: offensive

        Returns:
            list[int]: Values in in-order sequence
        """
        result: list[int] = []
        values = self._as_list()

        def walk(i: int) -> None:
            """
            Recursive in-order walk.

            Accesses 'values' from outer scope.
            At least we don't re-parse on every call.
            Small victories guys... Small Victories
            """
            if i >= len(values):
                return
            walk(2 * i + 1)  # Left
            result.append(int(values[i]))  # Root
            walk(2 * i + 2)  # Right
            # March Past

        walk(0)
        return result

    def __str__(self) -> str:
        """Return the raw CSV string representation."""
        return self._tree


def main() -> None:
    """Demonstrate the CSV tree in action."""
    print("Binary Tree as CSV String")
    print("=" * 50)

    tree = BinaryTreeAsString()

    print("\nInserting values: 1, 2, 3, 4, 5, 6, 7")
    for i in range(1, 8):
        tree.insert(i)

    print("\nRaw tree storage (the horror):")
    print(tree)

    print("\nAccessing nodes (each parses entire string):")
    print(f"Root: {tree.get_root()}")
    print(f"Left child of root: {tree.get_left(0)}")
    print(f"Right child of root: {tree.get_right(0)}")

    print("\nIn-order traversal (O(n²) complexity):")
    print(tree.inorder_traversal())

    print("\n" + "=" * 50)
    print("Comparison with correct implementation:")
    print("=" * 50)

    print("\nThis implementation:")
    print("  - Storage: Single CSV string")
    print("  - Insert: O(n) - parse, append, rebuild")
    print("  - Access: O(n) - parse entire string")
    print("  - Memory: Constant allocation/deallocation")

    print("\nCorrect implementation:")
    print("  - Storage: TreeNode objects with pointers")
    print("  - Insert: O(log n) avg - navigate and create node")
    print("  - Access: O(1) - follow pointers")
    print("  - Memory: Stable, no constant churn")

    print("\n" + "=" * 50)
    print("Conclusion:")
    print("The commas are doing all the work.")
    print("The strings are being abused.")
    print("The performance is terrible.")
    print("Use actual TreeNode objects.")
    print("=" * 50)
    # Look at this and despair!

if __name__ == "__main__":
    main()

# Making visuals for you all is so hard my dude! look at how much I suffer for your ease.