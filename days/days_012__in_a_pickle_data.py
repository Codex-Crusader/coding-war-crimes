"""
PICKLE DATABASE - SERIALIZING YOUR WAY TO DISASTER

WARNING: This "database" pickles an entire dictionary on every operation.

What this does:
Uses Python's pickle module as a database by serializing a giant dictionary
to disk on every insert/delete, and deserializing it on every read.

The correct way:
    import sqlite3

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO table VALUES (?, ?)", (key, value))
    conn.commit()

Or for simple key-value: import shelve

Time Complexity:
- insert(key, value): O(n) - load entire db, add one item, save entire db
- get(key): O(n) - load entire db just to get one value
- delete(key): O(n) - load entire db, remove one item, save entire db
- SQLite equivalent: O(log n) with indexes, O(1) with primary keys

Space Complexity: O(n) in memory during every operation
Disk Space: O(n) but grows with every write (pickle overhead)

Why this is catastrophically bad:

1. PICKLE IS NOT A DATABASE FORMAT:
   Pickle is for serializing Python objects, not for databases.

   What pickle is good for:
   - Saving Python objects temporarily
   - Caching computation results
   - Passing data between Python processes

   What pickle is NOT good for:
   - Databases
   - Concurrent access
   - Long-term storage
   - Anything security-critical

2. SECURITY NIGHTMARE:
   Pickle can execute arbitrary code during unpickling!

   Malicious pickle file can:
   - Execute system commands
   - Delete files
   - Install malware
   - Steal data

   NEVER unpickle data from untrusted sources!

3. LOAD ENTIRE DATABASE FOR EVERY OPERATION:
   Want one value? Load the whole database.
   Insert one row? Load everything, add one item, save everything.

   With 1 million records:
   - get("user_123"): Loads 1 million records to return one
   - insert("user_new", data): Loads 1 million, adds one, saves 1 million + 1

4. NO CONCURRENCY CONTROL:
   Process A: reads database
   Process B: reads database
   Process A: writes database with new record
   Process B: writes database with different record (overwrites A!)

   Result: Lost writes, no isolation, chaos

5. NO TRANSACTIONS:
   What if Python crashes during pickle.dump()?
   - Partial write
   - Corrupted file
   - Entire database lost
   - No rollback capability

6. NO QUERIES:
   Want all users with age > 25?
   - Load entire database
   - Filter in Python
   - No indexes, no optimization

   SQL: SELECT * FROM users WHERE age > 25
   This: Load everything, manual filtering

7. NO SCHEMA:
   - No data validation
   - No type checking
   - No constraints
   - Store anything anywhere
   - Hope for the best

8. MEMORY USAGE:
   Entire database must fit in memory during every operation.

   1 GB database file:
   - Every insert: Load 1 GB into RAM
   - Every get: Load 1 GB into RAM
   - Every delete: Load 1 GB into RAM

   SQLite: Only loads needed pages into memory

9. NO INDEXING:
   Every lookup is O(n) - checks entire database.
   Real databases use B-trees, hash indexes, etc.

10. PERFORMANCE DEGRADATION:
    As database grows, EVERY operation gets slower.

    Database size vs operation time:
    - 100 records: ~0.001s per operation
    - 1,000 records: ~0.01s per operation
    - 10,000 records: ~0.1s per operation
    - 100,000 records: ~1s per operation
    - 1,000,000 records: ~10s+ per operation

    Gets exponentially worse over time!

Performance comparison (10,000 records):

This pickle "database":
- Insert: Load 10k records, add 1, save 10,001 (~0.1s)
- Get: Load 10k records, return 1 (~0.1s)
- Delete: Load 10k records, remove 1, save 9,999 (~0.1s)

SQLite with proper indexes:
- Insert: ~0.0001s (1000x faster)
- Get by primary key: ~0.00001s (10,000x faster)
- Delete: ~0.0001s (1000x faster)

Real-world consequences:

Scenario: Simple user database
- 50,000 users
- 10 operations/second
- Each operation: ~0.5 seconds
- Queue builds up
- System becomes unresponsive
- Users leave
- Business fails

All because you used pickle instead of a real database.

The file corruption scenario:
    db = PickleDatabase()
    db.insert("important_data", critical_value)
    # Python crashes here during pickle.dump()
    # File is now corrupted
    # All data lost
    # No backup, no recovery
    # Panic ensues

Better alternatives:

1. SQLite (proper embedded database):
    import sqlite3
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS data (key TEXT PRIMARY KEY, value TEXT)")
    cursor.execute("INSERT INTO data VALUES (?, ?)", (key, value))
    conn.commit()

2. shelve (Python's persistent dict):
    import shelve
    with shelve.open("database") as db:
        db[key] = value

3. TinyDB (document database):
    from tinydb import TinyDB
    db = TinyDB("database.json")
    db.insert({"key": key, "value": value})

4. Redis (for key-value with speed):
    import redis
    r = redis.Redis()
    r.set(key, value)

When pickle IS appropriate:
- Caching computation results temporarily
- Saving ML model weights
- Passing objects between trusted Python processes
- Short-term serialization of Python-specific data structures

When pickle is NOT appropriate:
- Production databases
- Long-term storage
- Concurrent access
- Untrusted data
- Cross-language compatibility
- This

Educational value:
- Shows difference between serialization and database
- Demonstrates cost of full reload/rewrite operations
- Illustrates why databases have specialized formats
- Proves that "it works" does not mean "it's good"

Historical note:
In the early days, some developers did use pickle/serialization
as databases. Then they learned about data loss, corruption,
and performance issues. Now we have SQLite. Use it.

Real-world analogy:
Using pickle as a database is like storing your bank's transaction
history by writing the entire account history on a whiteboard,
erasing it completely, and rewriting it from scratch every time
someone deposits a dollar.

The pickle format:
Binary format that includes Python opcodes.
Can reconstruct arbitrary Python objects.
Including ones that execute code.
Not a security model you want for a database.

Author's note: I could have used SQLite.
                It's literally built into Python.
                I chose to pickle a dict instead.
                My database will never forgive me.
"""

import os
import pickle

# The file that will be completely rewritten on every insert/delete
DATABASE_FILE = "database.pkl"


class PickleDatabase:
    """
    A "database" that pickles an entire dictionary on every operation.

    Operations:
    - insert(): Load entire db, add one item, save entire db
    - get(): Load entire db, return one value
    - delete(): Load entire db, remove one item, save entire db

    Problems:
    - O(n) for operations that should be O(1) or O(log n)
    - Entire database in memory during every operation
    - No concurrency control
    - No transactions (crash = corrupted file)
    - Security risk (pickle can execute code)
    - Performance degrades as data grows

    This is what databases looked like before databases existed.
    """

    def __init__(self):
        """
        Initialize the database by creating an empty pickle file if needed.

        Already doing unnecessary I/O in the constructor.
        Setting the tone early.
        """
        if not os.path.exists(DATABASE_FILE):
            self._write_database({})

    def insert(self, key, value):
        """
        Insert a key-value pair by:
        1. Unpickling entire database into memory
        2. Adding one item to the dict
        3. Pickling entire database back to disk

        Time Complexity: O(n) where n = total records
        SQLite equivalent: O(log n) with B-tree index

        With 100,000 records, adding one record:
        - Loads 100,000 records
        - Adds 1 record
        - Saves 100,001 records

        Just to insert one item.
        """
        data = self._read_database()
        data[key] = value
        self._write_database(data)

    def get(self, key):
        """
        Get a value by unpickling the entire database.

        Time Complexity: O(n)
        SQLite with index: O(log n)
        Hash table: O(1)

        Loads entire database to return one value.
        The rest of the data? Loaded and discarded.
        """
        return self._read_database().get(key)

    def delete(self, key):
        """
        Delete a key by loading everything, removing one item, saving everything.

        Time Complexity: O(n)

        The trifecta of inefficiency:
        - Load entire database
        - Remove one item
        - Save entire database
        """
        data = self._read_database()
        if key in data:
            del data[key]
            self._write_database(data)

    def all(self):
        """
        Return all data.

        At least this operation makes sense to load everything.
        First operation that's not obviously wasteful.
        """
        return self._read_database()

    def clear(self):
        """
        Clear the database by pickling an empty dict.

        The only operation that doesn't read first.
        Progress!
        """
        self._write_database({})

    @staticmethod
    def _read_database():
        """
        Unpickle the entire database file.

        Security warning: pickle.load() can execute arbitrary code!
        Never unpickle data from untrusted sources.

        If this file is corrupted or modified maliciously,
        unpickling it could execute system commands, delete files,
        or do anything Python can do.

        This is why databases don't use pickle.
        """
        if not os.path.exists(DATABASE_FILE):
            return {}

        with open(DATABASE_FILE, "rb") as file:
            return pickle.load(file)

    @staticmethod
    def _write_database(data):
        """
        Pickle the entire database to file.

        Every insert/delete calls this.
        Every call serializes the entire dictionary.

        With 50,000 records, each taking 100 bytes:
        - File size: ~5 MB
        - Time to pickle: ~0.5 seconds
        - Happens on EVERY insert/delete

        Your disk I/O: maxed out
        Your application: slow
        Your users: leaving
        """
        with open(DATABASE_FILE, "wb") as file:
            pickle.dump(data, file) # type: ignore[arg-type]
            # yeah, you just witnessed me tell the linter to shut the hell up


# Example usage demonstrating the problems
if __name__ == "__main__":
    import time

    print("Pickle Database - Serializing Your Way to Disaster")
    print("=" * 50)

    db = PickleDatabase()
    db.clear()

    # Problem 1: Performance degradation
    print("\n1. Performance with growing database:")

    for size in [100, 500, 1000]:
        # Populate database
        db.clear()
        for idx in range(size):
            db.insert(f"key_{idx}", f"value_{idx}")

        # Time a single insert
        start = time.time()
        db.insert("new_key", "new_value")
        elapsed = time.time() - start

        print(f"   Database size: {size:4d} records")
        print(f"   Single insert: {elapsed * 1000:6.2f}ms")

    print("   Notice: Gets slower as database grows")

    # Problem 2: Every operation loads everything
    print("\n2. Memory usage per operation:")
    db.clear()

    # Insert 1000 records
    for idx in range(1000):
        db.insert(f"key_{idx}", "x" * 100)  # 100 bytes per value

    print("   Database: 1000 records, ~100 KB")
    print("   get() one key: Loads entire 100 KB")
    print("   insert() one key: Loads 100 KB, saves 100 KB")
    print("   delete() one key: Loads 100 KB, saves 100 KB")

    # Problem 3: No concurrency
    print("\n3. Concurrency problems:")
    print("   Process A: reads database")
    print("   Process B: reads database")
    print("   Process A: writes update")
    print("   Process B: writes update (overwrites A!)")
    print("   Result: Lost writes, no isolation")

    # Comparison with better approach
    print("\n4. Better alternatives:")
    print("   SQLite: Built into Python, proper database")
    print("   shelve: Like this, but with better internals")
    print("   TinyDB: JSON-based document database")
    print("   Redis: In-memory key-value store")

    # Cleanup
    db.clear()
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)

    print("\n" + "=" * 50)
    print("The correct way:")
    print("  import sqlite3")
    print("  conn = sqlite3.connect('database.db')")
    print("  # Actual database with indexes, transactions, ACID")
    print("=" * 50)
    # why oh why? why oh why? don't you want to stay with me? (get the reference? if not it's AOT "under the tree")