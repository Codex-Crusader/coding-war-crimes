"""
LINKED LIST AS FILESYSTEM - STORING NODES AS INDIVIDUAL TEXT FILES

WARNING: This implements a linked list where each node is a separate file on disk.

What this does:
Stores linked list nodes as text files in a directory.
Each node file contains its value and the filename of the next node.
Every operation involves file I/O.

The correct way:
    class Node:
        def __init__(self, val):
            self.val = val
            self.next = None

    class LinkedList:
        def __init__(self):
            self.head = None

Pointers in memory. O(1) node access. Standard practice.

The cursed way:
    node_1.txt: "value=1\nnext=node_2.txt"
    node_2.txt: "value=2\nnext=node_3.txt"
    node_3.txt: "value=3\nnext=NONE"

Filesystem as memory. Disk I/O for everything. Pure horror.

Why this is catastrophically bad:

1. DISK I/O FOR EVERY NODE ACCESS:
   Traverse 10-node list:
   - Open file 1, read, parse, close
   - Open file 2, read, parse, close
   - Open file 3, read, parse, close
   - ... repeat 10 times

   In-memory: 10 pointer dereferences (nanoseconds)
   This: 10 file operations (milliseconds)

   Slowdown: ~1,000,000x

2. FILESYSTEM AS MEMORY:
   Memory access: ~1 nanosecond
   SSD read: ~100 microseconds
   HDD read: ~10 milliseconds

   This code treats disk like RAM.
   Disk is 100,000x to 10,000,000x slower than RAM!

3. APPEND IS O(N) FILE OPERATIONS:
   To append to end of 1000-node list:
   - Read head file
   - Read node 2 file
   - Read node 3 file
   - ... read all 1000 files to find tail
   - Write new file
   - Rewrite previous tail file

   Total: 1000 reads + 2 writes = 1002 file operations

   In-memory: O(n) pointer traversals (fast)
   This: O(n) disk operations (extremely slow)

4. NO TRANSACTIONS:
   delete() process:
   1. Find node to delete
   2. Rewrite previous node's file (points to next)
   3. Delete node file

   Crash between step 2 and 3:
   - Previous node points to deleted file
   - Traversal breaks on missing file
   - Linked list corrupted
   - No rollback mechanism

5. MANUAL PARSING OF TEXT FILES:
   Node format: "value=5\nnext=node_3.txt"

   Every access:
   - Read file
   - Split by newline
   - Split by "="
   - Parse value to int
   - Extract next filename

   Could be: node.val and node.next (direct access)

6. FILENAME AS POINTER:
   Pointer in memory: 8 bytes (memory address)
   Filename as pointer: "node_123.txt" = 12 bytes + filesystem overhead

   Plus: Every "pointer dereference" is a file open operation

7. NO MEMORY BENEFITS:
   "But it's persistent!"

   Yes, but:
   - Loading persisted list: O(n) file reads
   - In-memory with pickle: O(1) file read
   - In-memory with database: O(n) with proper indexing

   You get persistence with terrible performance.

8. FILESYSTEM LIMITS:
   Many filesystems have limits:
   - Max files per directory: ~65,000 (ext4)
   - Max open files per process: ~1024 (ulimit)

   Large linked list:
   - 100,000 nodes = 100,000 files
   - Might hit directory limits
   - Definitely hits file descriptor limits during traversal

9. CONCURRENT ACCESS DISASTER:
   Thread A: Traversing list (reading files)
   Thread B: Deleting node (removing file)
   Thread A: Tries to read deleted file
   Result: FileNotFoundError mid-traversal

   In-memory: Proper threading with locks
   This: Race conditions everywhere

10. BACKUP/SYNC NIGHTMARE:
    1000-node list = 1000 individual files

    Cloud sync (Dropbox, Google Drive):
    - Syncs 1000 files individually
    - Takes minutes instead of seconds
    - Any file sync conflict breaks the list

    Backup:
    - Backing up 1000 small files is slower than 1 large file
    - File metadata overhead

Real-world consequences:

Issue 1 - Performance Death:
    1000-node list traversal:
    - In-memory: ~0.00001 seconds
    - This: ~1 second (on SSD)
    - This: ~10 seconds (on HDD)

    100,000x slower!

Issue 2 - File Descriptor Exhaustion:
    Traverse large list:
    - Opens many files rapidly
    - OS has limit on open files (~1024)
    - Hit limit = "Too many open files" error
    - Program crashes mid-operation

Issue 3 - Disk Wear:
    SSDs have limited write cycles.
    Every append:
    - Read entire chain
    - Write 2 files (new node + previous tail)

    1000 appends: ~3000 writes
    Your SSD's lifespan: Shortened

Issue 4 - Corruption Hell:
    Power loss during delete():
    - File deleted
    - But previous node still points to it
    - Next traversal: FileNotFoundError
    - Entire list beyond that point: Lost

    No atomic operations, no recovery.

Issue 5 - Production Scenario:
    Web server using this for session data:
    - Each request: Traverse list (1000 file ops)
    - 100 requests/second: 100,000 file ops/second
    - Disk I/O: 100%
    - Server: Unresponsive
    - Users: Gone

Performance comparison (1000-node list):

Operation: Traverse entire list

In-memory linked list:
    for node in list: ...

    Time: ~0.00001 seconds
    I/O: 0 disk operations

This filesystem abomination:
    current = head
    while current:
        read file...

    Time: ~1 second (SSD), ~10 seconds (HDD)
    I/O: 1000 file reads

    Slowdown: 100,000x - 1,000,000x

Operation: Append to end

In-memory:
    Traverse O(n) pointers
    Create node O(1)
    Assign pointer O(1)

    Time: Microseconds

This unholy thing:
    Traverse O(n) file reads
    Create file O(1)
    Rewrite previous file O(1)

    Time: Seconds

The overhead breakdown:

Single node access comparison:

In-memory:
    value = node.val
    next_node = node.next

    Operations:
    - 2 memory reads
    - Time: ~2 nanoseconds

This implementation:
    with open("node_5.txt") as f:
        content = f.read()
    lines = content.splitlines()
    value = int(lines[0].split("=")[1])

    Operations:
    - OS syscall to open file
    - Disk seek
    - Read file content
    - Close file
    - Parse text
    - Type conversion

    Time: ~100 microseconds (SSD)

    50,000x slower per node!

The file format overhead:

Storing value 42, next node is node_43.txt:

In-memory (Python object):
    class Node:
        val = 42
        next = <memory address>

    Size: ~56 bytes (Python object overhead)

This implementation:
    File: node_42.txt
    Content: "value=42\nnext=node_43.txt\n"

    Size: 28 bytes (content) + ~4KB (filesystem block)
    Plus: Filesystem metadata (inode, directory entry)

    Total: ~4KB per node (100x overhead!)

When filesystem persistence IS useful:

1. Actual persistence needs:
    Save entire linked list to file

    Then: Use pickle or JSON
    One file, not one-file-per-node

2. Large data that doesn't fit in RAM:
    Use a database with proper indexing

    Not: Individual text files

3. Distributed systems:
    Shared filesystem for coordination

    But: Use proper distributed data stores

When filesystem persistence is NOT useful:

1. Runtime data structure (this file!)
2. Frequent modifications
3. Performance-critical operations
4. When you have RAM available

The correct implementations:

Option 1 - In-memory (standard):
    class Node:
        def __init__(self, val):
            self.val = val
            self.next = None

    class LinkedList:
        def __init__(self):
            self.head = None

Option 2 - Persistent with pickle:
    import pickle

    # Save
    with open("list.pkl", "wb") as f:
        pickle.dump(linked_list, f)

    # Load
    with open("list.pkl", "rb") as f:
        linked_list = pickle.load(f)

    One file, O(1) save/load operations

Option 3 - Database (for large data):
    CREATE TABLE nodes (
        id INTEGER PRIMARY KEY,
        value INTEGER,
        next_id INTEGER
    );

    Proper indexing, transactions, atomic operations

All infinitely better than one-file-per-node.

The transaction problem:

This code has no atomic operations:

delete() steps:
1. Read previous node file
2. Parse it
3. Write previous node file (new next pointer)
4. Delete current node file

Failure scenarios:
- Crash after step 3: Dangling pointer to deleted file
- Crash after step 4: File exists but unreachable
- Concurrent delete: Race condition

In-memory with proper locking:
- Atomic pointer updates
- Thread-safe operations
- No corruption possible

The filesystem as database anti-pattern:

This is called "filesystem as database" anti-pattern.

Why databases exist:
- Atomic operations (ACID)
- Indexing for fast lookup
- Transaction support
- Concurrent access control
- Query optimization

Why filesystems exist:
- Storing files
- Hierarchical organization
- Not for node-by-node data structures

Using filesystem as database:
- Slow
- Unreliable
- No transactions
- No guarantees

Historical context:

Some old systems did store data as individual files.
Example: Unix mailbox (one file per message)

Problems encountered:
- Slow with many files
- Corruption issues
- Backup problems

Modern solution: Databases

This code recreates 1970s problems in 2025.

The disk I/O cost breakdown:

Traversing 1000-node list:

In-memory:
    1000 pointer dereferences
    Cost: 1000 * 1ns = 1 microsecond

SSD (this code):
    1000 file opens/reads/closes
    Cost: 1000 * 100μs = 100 milliseconds

HDD (this code):
    1000 file opens/reads/closes
    Cost: 1000 * 10ms = 10 seconds

The disk is not your RAM!

Cache nightmare:

CPUs cache memory.
Linked list traversal benefits from cache.

This code:
- Each node is a file
- Files not cached in CPU
- OS filesystem cache helps
- But still orders of magnitude slower

Result: Cache is useless

The directory pollution:

1000-node list creates (I will call this the 1000 node blood war):
- 1000 files in one directory
- Directory listing: Slow
- File search: Slow
- Backup: Slow
- Sync: Slow

Everything filesystem-related becomes slower.

Educational value:
- Shows why we don't use filesystem as RAM
- Demonstrates cost of disk I/O
- Illustrates importance of data structure design
- Proves that persistence ≠ use files for everything

The ultimate irony:

Goal: "Persistent linked list"
Result: Slow, unreliable, disk-eating monster

Better solution: In-memory + serialize to one file
- Fast in-memory operations
- Single file for persistence
- Atomic save operations
- No corruption risk
"""

import os
from typing import Optional

# Directory where we'll abuse the filesystem
NODE_DIR = "linked_list_nodes"


class FileNodeLinkedList:
    """
    A linked list where each node is stored as a separate text file.

    Structure: Each file contains:
        value=<int>
        next=<filename> or NONE

    Example filesystem state:
        linked_list_nodes/
        ├── node_1.txt   (value=1, next=node_2.txt)
        ├── node_2.txt   (value=2, next=node_3.txt)
        └── node_3.txt   (value=3, next=NONE)

    Why this is catastrophically bad:
    - Every node access = file I/O operation
    - Traversal = sequential file reads (extremely slow)
    - No transactions (corruption risk)
    - No atomic operations
    - Filesystem pollution
    - Disk wear

    Za Time Complexity:
    - append: O(n) file operations to find tail
    - traverse: O(n) file operations
    - delete: O(n) file operations

    Compare to in-memory: O(1) per node access

    Performance: 100,000x - 1,000,000x slower than in-memory

    Each node is a file. Each access is disk I/O. Each operation is pain.
    """

    def __init__(self) -> None:
        """
        Initialize the linked list.

        Creates directory for storing node files.
        Head pointer is a filename string instead of memory address.
        """
        os.makedirs(NODE_DIR, exist_ok=True)
        self.head: Optional[str] = None  # filename of head node, not memory pointer

    def _node_path(self, filename: str) -> str:
        """Get full path to node file."""
        return os.path.join(NODE_DIR, filename)

    def _write_node(self, filename: str, value: int, next_node: Optional[str]) -> None:
        """
        Write a node to filesystem.

        Creates a text file with format:
            value=<int>
            next=<filename or NONE>

        This is what we do instead of:
            node.val = value
            node.next = next_ptr

        Args:
            filename: Name of file to create/overwrite
            value: Integer value for this node
            next_node: Filename of next node, or None
        """
        with open(self._node_path(filename), "w") as f:
            f.write(f"value={value}\n")
            f.write(f"next={next_node if next_node else 'NONE'}\n")

    def _read_node(self, filename: str) -> tuple[int, Optional[str]]:
        """
        Read a node from filesystem.

        Opens file, reads content, parses text.

        Steps:
        1. Open file (OS syscall)
        2. Read content (disk I/O)
        3. Parse text (split, convert)
        4. Close file

        God this is exhausting
        In-memory equivalent: node.val, node.next (2 memory reads)

        Args:
            filename: Name of file to read

        Returns:
            tuple: (value, next_filename)
        """
        with open(self._node_path(filename), "r") as f:
            lines = f.read().splitlines()

        # Parse "value=42"
        value = int(lines[0].split("=", 1)[1])

        # Parse "next=node_5.txt" or "next=NONE"
        next_val = lines[1].split("=", 1)[1]

        return value, None if next_val == "NONE" else next_val

    def append(self, value: int) -> None:
        """
        Append a value to the linked list.

        Steps:
        - Create a new file for the node
        - Traverse entire list via file reads to find tail
        - Rewrite last node's file to point to new file

        With n nodes:
        - n file reads (traverse to tail)
        - 2 file writes (new node + update previous)

        Total: n reads + 2 writes

        In-memory: O(n) pointer traversals + O(1) pointer assignment
        This: O(n) disk operations

        Args:
            value: Integer value to append
        """
        filename = f"node_{value}.txt"

        # Empty list case
        if self.head is None:
            self.head = filename
            self._write_node(filename, value, None)
            return

        # Traverse to tail (reading files one by one)
        current = self.head
        while True:
            _, next_node = self._read_node(current)
            if next_node is None:
                break
            current = next_node

        # Write new node file
        self._write_node(filename, value, None)

        # Rewrite tail node to point to new file
        val, _ = self._read_node(current)
        self._write_node(current, val, filename)

    def traverse(self) -> list[int]:
        """
        Traverse the list by opening files one by one.

        For 1000-node list: (1000 NODE BLOOD WAR!!!)
        - Opens 1000 files
        - Reads 1000 files
        - Parses 1000 text files
        - Closes 1000 files

        Time: ~1 second (SSD), ~10 seconds (HDD)

        In-memory: ~0.00001 seconds

        Performance: filesystem-limited (extremely slow)

        Returns:
            list[int]: All values in order
        """
        values: list[int] = []
        current = self.head

        while current is not None:
            val, next_node = self._read_node(current)
            values.append(val)
            current = next_node

        return values

    def delete(self, value: int) -> None:
        """
        Delete the first node with the given value.

        This involves:
        - Reading files to find target
        - Rewriting previous node's file
        - Deleting target node's file
        - Praying nothing crashes mid-operation

        No transactions! Crash between operations = corrupted list.

        Steps:
        1. Find node to delete (read files)
        2. Rewrite previous node (file write)
        3. Delete node file (file delete)

        If crash after step 2:
        - Previous node points to deleted file
        - Traversal breaks on FileNotFoundError
        - List corrupted, no recovery

        Args:
            value: Value to delete

        Raises:
            ValueError: If value not found
        """
        current = self.head
        prev: Optional[str] = None

        while current is not None:
            val, next_node = self._read_node(current)

            if val == value:
                # Update head or previous node
                if prev is None:
                    self.head = next_node
                else:
                    prev_val, _ = self._read_node(prev)
                    self._write_node(prev, prev_val, next_node)

                # Delete the file
                # Like how maki slimed the Zenin Clan
                os.remove(self._node_path(current))
                return

            prev = current
            current = next_node

        raise ValueError("Value not found")


def main() -> None:
    """Demonstrate the filesystem-based linked list."""
    print("Linked List as Filesystem")
    print("=" * 50)

    ll = FileNodeLinkedList()

    print("\nAppending values: 1, 2, 3")
    print("(Each append: traverse files + write files)")
    ll.append(1)
    ll.append(2)
    ll.append(3)

    print(f"\nFiles created in {NODE_DIR}/:")
    for filename in sorted(os.listdir(NODE_DIR)):
        print(f"  {filename}")

    print("\nTraversing linked list (opening each file):")
    print(ll.traverse())

    print("\nDeleting value 2 (file operations + file deletion)")
    ll.delete(2)

    print("\nTraversing again:")
    print(ll.traverse())

    print(f"\nRemaining files in {NODE_DIR}/:")
    for filename in sorted(os.listdir(NODE_DIR)):
        print(f"  {filename}")

    print("\n" + "=" * 50)
    print("Comparison with correct implementation:")
    print("=" * 50)

    print("\nThis implementation:")
    print("  - Storage: Individual text files per node")
    print("  - Traverse: O(n) file operations")
    print("  - Append: O(n) file reads + 2 writes")
    print("  - Performance: Milliseconds to seconds")

    print("\nCorrect implementation:")
    print("  - Storage: Node objects in memory")
    print("  - Traverse: O(n) pointer dereferences")
    print("  - Append: O(n) pointer traversal")
    print("  - Performance: Microseconds")

    print("\n" + "=" * 50)
    print("Conclusion:")
    print("The filesystem is not your RAM.")
    print("Disk I/O is 100,000x slower than memory.")
    print("One file per node is a bad idea.")
    print("Use actual Node objects with pointers.")
    print("=" * 50)

# through heaven and hell... I alone am the Jobless one....

if __name__ == "__main__":
    main()