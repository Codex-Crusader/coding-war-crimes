"""
HASH TABLE USING STRING LENGTH AS HASH - AN EXERCISE IN COMPUTATIONAL MASOCHISM

WARNING: This implementation violates every principle of good hash table design.
         Performance degrades to O(n) for any real-world dataset.
         Collisions are not a bug, they are the primary feature.

What this does:
Implements a hash table that uses len(key) as the hash function, ensuring
maximum collision rates and minimum performance for any practical use case.

The correct way:
    Use Python's built-in dict, which uses a proper hash function that
    distributes keys evenly across buckets with minimal collisions.

The cursed way:
- Hash function considers ONLY the length of the key
- All keys with the same length collide into the same bucket
- English words cluster around 5-9 characters
- Variable names cluster around 4-15 characters
- Every insert/lookup degrades to linear search within buckets
- Bucket utilization is catastrophically uneven

Time Complexity:
    Best case: O(1) - when all keys have unique lengths (never happens)
    Average case: O(n/k) where k is the number of distinct key lengths
    Worst case: O(n) - when all keys have the same length (always happens)
    Reality: Worse than a linked list because we pretend it's a hash table

Space Complexity:
    O(n) - same as a proper hash table, but with none of the benefits

Collision Rate:
    Approximately 100% for any dataset with more than 16 distinct items

Why this exists:
This is a teaching tool disguised as a functioning data structure. It
demonstrates what happens when you choose a hash function that:
- Ignores the actual content of the key
- Has extremely poor distribution properties
- Maps vast input domains to tiny output ranges
- Violates the fundamental principle of hash functions: different inputs
  should produce different outputs with high probability

Performance Characteristics by Use Case:

English Dictionary (50,000 words):
- Most words are 5-9 letters long
- Buckets 5-9 contain 80% of all words
- Buckets 0-4 and 10-15 are nearly empty
- Lookup performance: O(6,000) average case
- A linked list would be faster

Variable Names from Code:
- Most identifiers are 4-15 characters
- Bucket distribution: catastrophically uneven
- Common patterns: get_user, set_value, calculate_total
- All 9-letter identifiers collide (thousands of them)
- Lookup performance: O(hundreds) for common lengths

User Database:
- Username requirements: 3-20 characters
- Most users choose 6-10 character names
- Buckets 6-10 become megabuckets of doom
- 1,000,000 users might have 900,000 in 5 buckets
- Lookup performance: O(180,000) average case

URLs:
- Domain names: 5-15 characters typically
- Full URLs: 20-100+ characters
- Path segments: 3-20 characters
- Every URL with the same total length collides
- Query parameters make it even worse

Failure Modes:

1. Pathological Input
   All keys with length 5:
   - 100% collision rate
   - Degrades to unsorted linked list
   - O(n) for everything
   - Why did we even make buckets?

2. Natural Language
   English word frequency distribution:
   - 3 letters: common (the, and, for)
   - 4 letters: very common (that, with, have)
   - 5-9 letters: most common
   - Result: 90% of words in 7 buckets

3. Generated Identifiers
   UUIDs with hyphens: 36 characters
   - Every UUID hashes to the same bucket
   - Millions of UUIDs, one bucket
   - This is no longer a hash table
   - This is a linked list with extra steps

4. Mixed Length Data
   Best case scenario for this implementation:
   - Still terrible
   - Uneven distribution guaranteed
   - Some buckets empty, others overflowing
   - Load factor becomes meaningless

Comparison to Proper Hash Functions:

Python's hash():
    - Considers entire key content
    - Uses sophisticated mixing operations
    - Produces uniformly distributed outputs
    - Collision rate: ~1/2^64 for good data
    - Lookup: O(1) expected

This Implementation:
    - Considers only key length
    - Uses modulo operation on length
    - Produces clustered outputs
    - Collision rate: ~100% for real data
    - Lookup: O(n) expected

Mathematical Analysis:

For bucket_count = 16 and n random strings:
- Expected keys per bucket with good hash: n/16
- Expected keys per bucket with this hash: depends entirely on length distribution
- For English words: buckets 5-9 have ~n/6 each, others nearly empty
- Variance in bucket sizes: catastrophically high
- Load factor: meaningless metric

Birthday Paradox Application: (I had to research what it is)
- With a good hash function: need ~sqrt(2^64) items for 50% collision
- With this hash function: need 2 items of the same length for 100% collision
- For 16 buckets and natural language: collision guaranteed after 17 items

Real World Impact:

If you used this in production:
- Dictionary lookups slow to a crawl
- Cache performance degrades to O(n)
- Database indices become useless
- Users complain about lag
- Monitoring shows CPU at 100%
- Profiler points to hash table operations
- You realize length-based hashing was a mistake
- You rewrite everything
- You never speak of this again


Anti-Patterns Demonstrated:

1. Ignoring key content
2. Poor distribution properties
3. Predictable collision patterns
4. Length-based assumptions
5. Oversimplified hash logic

Author's Confession:

I could have used len(key) * 31 + ord(key[0]) for slightly better distribution.
Instead I chose pure length-based hashing to maximize suffering.
This is not a bug. This is performance anti-art.

Usage Warning:
If you use this code in production and it causes problems, that's on you.
You were warned. Multiple times. In detail.

Final Thoughts:

The hash table is a beautiful data structure when implemented correctly.
It provides O(1) average-case performance through careful design and
proper hash function selection.

This implementation is what happens when you ignore all of that and
decide that string length is a good proxy for string content.

Spoiler alert: it isn't.
Author Note: AAAAAAAAAAAAAAAAAAAAAAAAA!
"""

from typing import Any


class LengthHashTable:
    """
    A hash table implementation that uses string length as the hash function.

    This is the worst possible design choice for a hash function, guaranteeing:
    - Maximum collisions for real-world data
    - Uneven bucket distribution
    - O(n) worst-case performance for common operations
    - The transformation of a hash table into an expensive linked list

    Attributes:
        _buckets: List of buckets, each containing a list of key-value pairs
        _size: Current number of items in the hash table
        _collision_count: Number of collisions encountered (for debugging)
        _bucket_count: Total number of buckets available

    Design Decisions (all bad):
        - Hash function: len(key) mod bucket_count
        - Collision resolution: Chaining (required due to guaranteed collisions)
        - Resize strategy: None (we don't deserve dynamic resizing)
        - Distribution: Catastrophically poor by design
    """

    def __init__(self, bucket_count: int = 16) -> None:
        """
        Initialize the hash table with a fixed number of buckets.

        Args:
            bucket_count: Number of buckets to create. More buckets won't help
                         because the hash function is fundamentally broken.

        Notes:
            Even with 1000 buckets, all 5-letter words still collide.
            The problem is not bucket count, it's the hash function.
            But we're not fixing that because this is intentionally cursed.
        """
        self._bucket_count: int = bucket_count
        self._buckets: list[list[tuple[str, Any]]] = [[] for _ in range(self._bucket_count)]
        self._size: int = 0
        self._collision_count: int = 0

    def _hash(self, key: str) -> int:
        """
        The forbidden hash function that guarantees collisions.

        This function:
        - Ignores the actual content of the key
        - Only considers the length
        - Maps all same-length strings to the same bucket
        - Violates every principle of good hash function design

        Args:
            key: The string to hash

        Returns:
            An integer between 0 and bucket_count - 1, based solely on key length

        Examples:
            _hash("cat") == _hash("dog") == _hash("sun")  # All length 3
            _hash("hello") == _hash("world") == _hash("12345")  # All length 5
            _hash("a") != _hash("aa")  # Only time we get different hashes

        Why this is terrible:
            For any real dataset, keys cluster around common lengths.
            English words: 5-9 letters
            Variable names: 4-15 letters
            URLs: 20-100+ characters
            Result: Most keys hash to the same few buckets.

        Alternatives that would be better (but we won't use):
            - sum(ord(c) for c in key) - at least considers content
            - hash(key) - Python's built-in (actually good)
            - len(key) * 31 + ord(key[0]) - slightly less terrible
            - Anything that looks at the actual characters

        Performance impact:
            This function is O(1), which is good.
            But it causes O(n) behavior everywhere else, which is bad.
            Very bad.
            This is not very skibidi of me....
        """
        return len(key) % self._bucket_count

    def set(self, key: str, value: Any) -> None:
        """
        Insert or update a key-value pair in the hash table.

        Process:
        1. Hash the key (badly) to find the bucket
        2. Search the entire bucket for existing key (linear search)
        3. Update if found, append if not
        4. Watch performance degrade as bucket grows

        Args:
            key: String key to insert or update
            value: Associated value (can be anything)

        Time Complexity:
            Best case: O(1) - empty bucket (only happens once per length)
            Average case: O(n/k) where k is number of distinct lengths
            Worst case: O(n) - all keys have same length

        Space Complexity:
            O(1) - just adding one tuple to a list

        Collision behavior:
            Every same-length key collides into the same bucket.
            For English text: most keys are 5-9 letters.
            Result: 80% of your data in 5 buckets.

        Real-world impact:
            Inserting 1,000,000 usernames (average length 8):
            - ~800,000 end up in bucket for length 8
            - Each insertion searches through all previous collisions
            - Total comparisons: O(n^2) for the whole dataset
            - A sorted array would be faster
        """
        index = self._hash(key)
        bucket = self._buckets[index]

        # Linear search through bucket (because we have no choice)
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                # Found it - update value
                bucket[i] = (key, value)
                return

        # Key not found - append to bucket
        # If bucket is already large, this is where we cry
        # Don't worry... I cried too
        if len(bucket) > 0:
            self._collision_count += 1

        bucket.append((key, value))
        self._size += 1

    def get(self, key: str) -> Any:
        """
        Retrieve a value by key from the hash table.

        Process:
        1. Hash the key (badly) to find the bucket
        2. Linear search through all colliding keys
        3. Return value if found, raise KeyError if not
        4. Pray the bucket isn't too large

        Args:
            key: String key to look up

        Returns:
            The value associated with the key

        Raises:
            KeyError: If the key is not in the hash table

        Time Complexity:
            Best case: O(1) - key is first in bucket
            Average case: O(bucket_size) - scan half the bucket
            Worst case: O(n) - key is last or missing, scan entire bucket

        Performance examples:
            Dataset: 100,000 English words
            Query: "hello" (5 letters)
            Bucket 5 contains: ~15,000 words
            Comparisons needed: ~7,500 average
            A binary search tree: ~17 comparisons
            Python's dict: ~1 comparison

            Dataset: 1,000,000 user IDs (all 8 chars)
            Query: Any user ID
            Bucket 8 contains: 1,000,000 items
            Comparisons needed: ~500,000 average
            This is no longer O(1)
            This is not even O(log n)
            This is just O(n) with extra steps

        Why this is slower than alternatives:
            - Linked list: O(n) but simpler
            - Binary search tree: O(log n) guaranteed
            - Proper hash table: O(1) expected
            - This abomination: O(n) disguised as O(1)
        """
        index = self._hash(key)
        bucket = self._buckets[index]

        # Linear search through potentially massive bucket
        for existing_key, value in bucket:
            if existing_key == key:
                return value

        # Key not found after checking entire bucket
        raise KeyError(key)

    def delete(self, key: str) -> None:
        """
        Remove a key-value pair from the hash table.

        Process:
        1. Hash the key (badly)
        2. Linear search through bucket
        3. Remove if found
        4. Suffer through O(n) list removal

        Args:
            key: String key to remove

        Raises:
            KeyError: If key doesn't exist

        Time Complexity:
            Search: O(bucket_size)
            Removal: O(bucket_size) - list.remove() is also O(n)
            Total: O(bucket_size) which approaches O(n)

        Notes:
            We're doing O(n) work to remove from what should be an O(1) structure.
            This is like using a forklift to move a single box, then
            realizing the forklift is actually a guy carrying things slowly.
        """
        index = self._hash(key)
        bucket = self._buckets[index]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                del bucket[i]
                self._size -= 1
                return

        raise KeyError(key)

    def contains(self, key: str) -> bool:
        """
        Check if a key exists in the hash table.

        This is get() but without returning the value.
        Still O(bucket_size) because we have to search the bucket.

        Args:
            key: String key to check

        Returns:
            True if key exists, False otherwise

        Time Complexity:
            Same as get(): O(bucket_size) approaching O(n)
        """
        index = self._hash(key)
        bucket = self._buckets[index]

        for existing_key, _ in bucket:
            if existing_key == key:
                return True

        return False

    def get_statistics(self) -> dict[str, Any]:
        """
        Return statistics about the hash table's pathological state.

        This reveals the horror of our design choices:
        - How many buckets are empty (many)
        - How many buckets are overloaded (few but catastrophic)
        - Maximum bucket size (terrifying)
        - Collision rate (approaches 100%)

        Returns:
            Dictionary containing various metrics of failure

        Example output for 10,000 English words:
            {
                'total_items': 10000,
                'bucket_count': 16,
                'filled_buckets': 8,
                'empty_buckets': 8,
                'max_bucket_size': 2341,  # All 7-letter words
                'min_bucket_size': 0,
                'avg_bucket_size': 625.0,
                'collision_rate': 0.9992,
                'load_factor': 625.0,  # Meaningless with this distribution
            }
        """
        bucket_sizes = [len(bucket) for bucket in self._buckets]
        non_empty_buckets = [size for size in bucket_sizes if size > 0]

        return {
            'total_items': self._size,
            'bucket_count': self._bucket_count,
            'filled_buckets': len(non_empty_buckets),
            'empty_buckets': self._bucket_count - len(non_empty_buckets),
            'max_bucket_size': max(bucket_sizes) if bucket_sizes else 0,
            'min_bucket_size': min(bucket_sizes) if bucket_sizes else 0,
            'avg_bucket_size': self._size / self._bucket_count if self._bucket_count > 0 else 0,
            'collision_count': self._collision_count,
            'collision_rate': self._collision_count / self._size if self._size > 0 else 0,
        }

    def __len__(self) -> int:
        """Return the number of items in the hash table."""
        return self._size

    def __contains__(self, key: str) -> bool:
        """Support 'in' operator."""
        return self.contains(key)

    def __getitem__(self, key: str) -> Any:
        """Support bracket notation for getting values."""
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """Support bracket notation for setting values."""
        self.set(key, value)

    def __delitem__(self, key: str) -> None:
        """Support del operator."""
        self.delete(key)

    def __str__(self) -> str:
        """
        Return a string representation showing bucket distribution.

        This visualization reveals the clustering problem:
        - Some buckets empty
        - Some buckets with thousands of items
        - The uneven distribution of doom

        Example output:
            Bucket 0 (length % 16 = 0): []
            Bucket 1 (length % 16 = 1): []
            Bucket 2 (length % 16 = 2): []
            Bucket 3 (length % 16 = 3): [('cat', 1), ('dog', 2), ('sun', 3), ...]
            Bucket 4 (length % 16 = 4): [('bear', 4), ('lion', 5), ...]
            Bucket 5 (length % 16 = 5): [2,341 items - TOO MANY TO DISPLAY]
            ...
        """
        lines = ["Hash Table Bucket Distribution:"]
        lines.append("=" * 50)

        for i, bucket in enumerate(self._buckets):
            if len(bucket) == 0:
                lines.append(f"Bucket {i:2d} (length % {self._bucket_count} = {i:2d}): []")
            elif len(bucket) <= 5:
                lines.append(f"Bucket {i:2d} (length % {self._bucket_count} = {i:2d}): {bucket}")
            else:
                lines.append(
                    f"Bucket {i:2d} (length % {self._bucket_count} = {i:2d}): "
                    f"[{len(bucket)} items - first 3: {bucket[:3]}...]"
                )

        return "\n".join(lines)

    def compute_hash_for_demo(self, key: str) -> int:
        """
        Public wrapper for the hash function for demonstration purposes.

        This exists so external code can see which bucket a key hashes to
        without accessing the protected _hash method directly.

        Args:
            key: The string to hash

        Returns:
            The bucket index this key would hash to
        """
        return self._hash(key)


def demonstrate_pathological_behavior() -> None:
    """
    Demonstrate how this hash table fails spectacularly with real data.

    This function shows:
    1. Natural language clustering (all 3-letter words collide)
    2. Performance degradation
    3. Bucket distribution horror
    4. Why this design is cursed
    """
    print("DEMONSTRATION OF PATHOLOGICAL HASH TABLE BEHAVIOR")
    print()

    # Test 1: Same-length keys (worst case)
    print("Test 1: All keys have the same length (3 characters)")
    table = LengthHashTable(bucket_count=8)

    three_letter_words = [
        "cat", "dog", "sun", "bat", "hat", "man",
        "car", "bus", "pen", "cup", "box", "key",
        "fox", "ant", "bee", "owl", "rat", "pig"
    ]

    for i, word in enumerate(three_letter_words):
        table.set(word, i)

    print(f"Inserted {len(three_letter_words)} words")
    print(f"All words are 3 letters long")
    print(f"All words hash to bucket: {table.compute_hash_for_demo('cat')}")
    print(f"Collision rate: {table.get_statistics()['collision_rate']:.2%}")
    print(table)
    print("Analysis: Every single word collided into the same bucket.")
    print("This is no longer a hash table. This is a linked list.")

    # Test 2: Natural language distribution
    print("Test 2: Mix of common English words (realistic scenario)")
    print("-" * 70)
    table2 = LengthHashTable(bucket_count=16)

    mixed_words = [
        # 3 letters
        "the", "and", "for", "are", "but", "not", "you", "all",
        # 4 letters
        "that", "with", "have", "this", "will", "your", "from", "they",
        # 5 letters
        "which", "their", "would", "there", "could", "other", "about", "great",
        # 6 letters
        "people", "should", "before", "really", "little", "number", "public",
        # 7 letters
        "because", "through", "another", "between", "without", "however",
        # 8 letters
        "anything", "somebody", "everything", "something",
    ]

    for i, word in enumerate(mixed_words):
        table2.set(word, i)

    stats = table2.get_statistics()
    print(f"Inserted {stats['total_items']} words")
    print(f"Bucket count: {stats['bucket_count']}")
    print(f"Filled buckets: {stats['filled_buckets']}")
    print(f"Empty buckets: {stats['empty_buckets']}")
    print(f"Largest bucket: {stats['max_bucket_size']} items")
    print(f"Collision rate: {stats['collision_rate']:.2%}")
    print(table2)
    print("Analysis: Words cluster around common lengths (3-8 letters).")
    print("Most buckets are empty. A few buckets are overloaded.")
    print("Buckets 0, 1, 2, 9-15 are wasted space.")

    # Test 3: Performance comparison
    print("Test 3: Performance comparison with Python's dict")

    import time

    # Create large dataset
    test_keys = [f"test_key_{i:05d}" for i in range(1000)]

    # Test our cursed hash table
    # I lost track of myself here. Don't touch it. it works somehow
    cursed_table = LengthHashTable(bucket_count=16)
    start = time.perf_counter()
    for i, key in enumerate(test_keys):
        cursed_table.set(key, i)
    cursed_insert_time = time.perf_counter() - start

    start = time.perf_counter()
    for key in test_keys:
        _ = cursed_table.get(key)
    cursed_lookup_time = time.perf_counter() - start

    # Test Python's dict
    proper_dict = {}
    start = time.perf_counter()
    for i, key in enumerate(test_keys):
        proper_dict[key] = i
    dict_insert_time = time.perf_counter() - start

    start = time.perf_counter()
    for key in test_keys:
        _ = proper_dict[key]
    dict_lookup_time = time.perf_counter() - start

    print(f"Dataset: {len(test_keys)} keys")
    print(f"Key pattern: 'test_key_XXXXX' (all same length)")
    print()
    print(f"Cursed Hash Table:")
    print(f"  Insert time: {cursed_insert_time * 1000:.2f}ms")
    print(f"  Lookup time: {cursed_lookup_time * 1000:.2f}ms")
    print()
    print(f"Python's dict:")
    print(f"  Insert time: {dict_insert_time * 1000:.2f}ms")
    print(f"  Lookup time: {dict_lookup_time * 1000:.2f}ms")
    print()
    print(f"Performance degradation:")
    print(f"  Insert: {cursed_insert_time / dict_insert_time:.1f}x slower")
    print(f"  Lookup: {cursed_lookup_time / dict_lookup_time:.1f}x slower")

    stats = cursed_table.get_statistics()
    print(f"Why it's slow:")
    print(f"  All {len(test_keys)} keys have the same length")
    print(f"  They all hash to bucket {cursed_table.compute_hash_for_demo(test_keys[0])}")
    print(f"  Largest bucket has {stats['max_bucket_size']} items")
    print(f"  Every operation requires linear search through {stats['max_bucket_size']} items")
    # God this code works like a shitty reddit Mod.


if __name__ == "__main__":
    demonstrate_pathological_behavior()