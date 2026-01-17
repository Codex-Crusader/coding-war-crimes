"""
FILE-BASED SINGLETON - PERSISTENCE THROUGH PAIN

WARNING: This "singleton" uses a text file as its backing store.

What this does:
Implements the Singleton pattern by storing all data in a text file.
Every get/set operation reads/writes the entire file from/to disk.

The correct way:
    class Singleton:
        _instance = None
        _data = {}

        def __new__(cls):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

        def set(self, key, value):
            self._data[key] = value

        def get(self, key):
            return self._data.get(key)

Or just use a module-level dict: data = {}

Time Complexity (per operation):
- set(): O(n) - reads entire file, writes entire file
- get(): O(n) - reads entire file
- In-memory dict: O(1) for both

Space Complexity: O(n disk space + n memory during read/write)
Disk Wear: O(your SSD's warranty voiding)

Why this is catastrophically bad:

1. NOT ACTUALLY A SINGLETON:
   You can create multiple FileSingleton instances:

   s1 = FileSingleton()
   s2 = FileSingleton()  # Nothing stops this

   They both access the same file, but they're separate objects.
   Real singletons enforce single instance at the class level.

2. DISK I/O FOR EVERY OPERATION:
   - set("key", "value") → read file, parse, modify, write file
   - get("key") → read file, parse, return value

   In-memory dict:
   - set: direct memory write
   - get: direct memory read

   Disk I/O is ~100,000x slower than memory access!

3. NO CONCURRENCY CONTROL:
   Thread A: reads file
   Thread B: reads file
   Thread A: writes file (with update)
   Thread B: writes file (overwrites A's update!)

   Result: Lost writes, data corruption, chaos

4. FILE AS DATABASE:
   - No transactions
   - No ACID properties
   - No indexing
   - No query capabilities
   - Just... pain

5. TYPE INFORMATION LOST:
   data[key] = str(value)  # Everything becomes a string

   set("count", 42)  # Stored as "42"
   get("count")      # Returns "42" (string), not 42 (int)

   Need to manually convert back every time.

6. NO ERROR HANDLING:
   - File deleted during operation? Crash
   - Disk full? Crash
   - Permissions changed? Crash
   - Invalid data in file? Silent corruption

7. FULL FILE REWRITE ON EVERY SET:
   Even changing one value rewrites the entire file.

   With 1000 keys, changing one key:
   - Reads 1000 lines
   - Writes 1000 lines
   - Just to update one value

8. MANUAL PARSING:
   Parsing "key=value" lines manually when Python has:
   - configparser (INI files)
   - json (structured data)
   - pickle (Python objects)
   - shelve (persistent dict)
   - sqlite (actual database)

9. NO VALIDATION:
   What if key contains "="? → key=val=ue (parsing breaks)
   What if value contains newline? → Multiline chaos
   What if file is corrupted? → Return partial data

10. PERSISTENCE AS A "FEATURE":
    Singletons are about single instance, not persistence!
    Using a file for persistence is fine.
    Calling it a "singleton" because of the file is wrong.

Performance comparison (1000 operations):

In-memory dict:
- Time: ~0.001 seconds
- Disk writes: 0

This "singleton":
- Time: ~1-5 seconds
- Disk writes: 1000
- File rewrites: 1000
- Your SSD: crying

Real-world consequences:

Scenario: High-traffic web app
- 1000 requests/second
- Each does one set() operation
- 1000 file rewrites/second
- Your disk: dead in a week

Race condition example:
    # Thread 1
    s = FileSingleton()
    s.set("counter", "1")  # Writes: counter=1

    # Thread 2 (simultaneously)
    s = FileSingleton()
    s.set("user", "bob")   # Writes: user=bob

    # Result: One of these writes is lost!

The correct approaches:

1. Actual Singleton (in-memory):
    class Singleton:
        _instance = None

        def __new__(cls):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

2. Module-level (Python's natural singleton):
    # config.py
    data = {}

    # anywhere.py
    import config
    config.data["key"] = "value"

3. Persistent storage (if actually needed):
    import shelve

    with shelve.open("data") as db:
        db["key"] = value

4. Database (proper solution):
    import sqlite3

    conn = sqlite3.connect("data.db")
    # Actual transactions, locking, queries

When to use file-based storage:
- Configuration files (but use configparser/JSON)
- Logs (but use logging module)
- Caching (but use proper cache with TTL)
- State persistence between runs (but use pickle/shelve)

When to NOT use file-based storage:
- In-memory singleton pattern
- High-frequency operations
- Concurrent access without locking
- Anything performance-critical
- This

Educational value:
- Shows difference between singleton pattern and persistence
- Demonstrates cost of disk I/O
- Illustrates race conditions
- Proves that "it works on my machine" ≠ "it's correct"

Historical note:
This is basically how early programs stored data.
Then we invented databases.
For good reasons.

Real-world analogy:
Using a text file as your singleton backing store is like:
- Writing your shopping list on paper
- Going to the store
- Buying one item
- Driving home to update the list
- Driving back to the store
- Repeat for each item

Author's note: I could have used a dict.
                I chose disk I/O instead.
                My SSD will never forgive me.
"""

import os

# The file that will be rewritten constantly
SINGLETON_FILE = "singleton.txt"


class FileSingleton:
    """
    A "singleton" that stores all data in a text file.

    Spoiler: This is not actually a singleton pattern.
    This is a poorly implemented file-based key-value store
    that happens to share one file across all instances.

    Problems:
    - Not actually enforcing single instance
    - Disk I/O on every operation (slow)
    - No concurrency control (race conditions)
    - Type information lost (everything is a string)
    - Full file rewrite on every change (inefficient)
    - No error handling (crashes on file issues)

    The "singleton" file format:
        key1=value1
        key2=value2
        key3=value3

    Parsed by splitting on "=" which breaks if keys contain "=".
    """

    def __init__(self):
        """
        Initialize the "singleton" by creating an empty file if needed.

        Note: This doesn't enforce single instance.
        You can create unlimited FileSingleton objects.
        They just all share the same file.
        """
        if not os.path.exists(SINGLETON_FILE):
            self._write_file({})

    def set(self, key, value):
        """
        Set a key-value pair by:
        1. Reading entire file into memory
        2. Parsing all lines
        3. Modifying one value
        4. Writing entire file back to disk

        Time Complexity: O(n) where n = number of keys
        An in-memory dict would be O(1)

        Race condition: Two simultaneous sets will lose one write
        """
        data = self._read_file()
        data[key] = str(value)  # Type information lost!
        self._write_file(data)

    def get(self, key):
        """
        Get a value by reading and parsing the entire file.

        Time Complexity: O(n)
        An in-memory dict would be O(1)

        Returns string, even if you stored an int/float/bool.
        Hope you remember to convert back!
        """
        return self._read_file().get(key)

    def all(self):
        """
        Return all data by reading and parsing the entire file.

        At least this operation makes sense to read the whole file.
        """
        return self._read_file()

    def clear(self):
        """
        Clear all data by writing an empty file.

        This is the only operation that doesn't read first.
        Small victories.
        """
        self._write_file({})

    @staticmethod
    def _read_file():
        """
        Read and parse the singleton file.

        Format: key=value (one per line)

        Issues:
        - Splits on first "=" only (maxsplit=1 helps)
        - Keys with "=" will break parsing
        - Values with newlines will break format
        - No escaping or quoting
        - Corrupted file returns partial data silently
        """
        if not os.path.exists(SINGLETON_FILE):
            return {}

        data = {}
        with open(SINGLETON_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if "=" in line:
                    key, value = line.split("=", 1)  # At least we use maxsplit
                    data[key] = value
        return data

    @staticmethod
    def _write_file(data):
        """
        Write all data to file by recreating it from scratch.

        Every set() operation calls this.
        Every call overwrites the entire file.

        With 1000 keys, changing one key:
        - Writes 1000 lines
        - Just to change one value
        - Disk goes brrrrr
        """
        with open(SINGLETON_FILE, "w") as file:
            for key, value in data.items():
                file.write(key + "=" + value + "\n")


# Example usage demonstrating the problems
if __name__ == "__main__":
    import time

    print("File-Based Singleton - Persistence Through Pain")
    print("=" * 50)

    # "Problem" 1: Not actually a singleton
    print("\n1. Creating multiple 'singletons':")
    s1 = FileSingleton()
    s2 = FileSingleton()
    print(f"   s1 is s2: {s1 is s2}")  # False - not a real singleton!
    print("   [insert police siren here] Not enforcing single instance")

    # Problem 2: Disk I/O overhead
    print("\n2. Performance comparison:")

    # File-based version
    s = FileSingleton()
    s.clear()

    start = time.time()
    for iteration in range(100):
        s.set(f"key_{iteration}", iteration)
    file_time = time.time() - start

    # In-memory version
    memory_dict = {}
    start = time.time()
    for iteration in range(100):
        memory_dict[f"key_{iteration}"] = iteration
    memory_time = time.time() - start

    print(f"   File-based: {file_time:.4f}s (100 sets)")
    print(f"   In-memory:  {memory_time:.6f}s (100 sets)")
    print(f"   Slowdown:   {file_time / memory_time:.0f}x slower")

    # Problem 3: Type loss
    print("\n3. Type information lost:")
    s.clear()
    s.set("number", 42)
    s.set("float", 3.14)
    s.set("bool", True)

    print(f"   Stored int 42, got: {s.get('number')} (type: {type(s.get('number')).__name__})")
    print(f"   Stored float 3.14, got: {s.get('float')} (type: {type(s.get('float')).__name__})")
    print(f"   Stored bool True, got: {s.get('bool')} (type: {type(s.get('bool')).__name__})")
    print("   [thanos snap] Everything became a string")

    # Problem 4: File rewrites
    print("\n4. File operations:")
    print(f"   100 set() operations = 100 file rewrites")
    print(f"   1 get() operation = 1 file read")
    print(f"   Your SSD: crying")

    # Cleanup
    s.clear()
    if os.path.exists(SINGLETON_FILE):
        os.remove(SINGLETON_FILE)

    print("\n" + "=" * 50)
    print("The correct way: Just use a dict")
    print("data = {} # That's it. That's the solution.")
    print("=" * 50)