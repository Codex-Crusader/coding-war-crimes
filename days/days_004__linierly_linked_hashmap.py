"""
HASHMAP AS A LINKED LIST - THE ULTIMATE BETRAYAL

WARNING: This is not a real HashMap. This is a LinkedList wearing a fake mustache.

What this should be:
A HashMap uses a hash function to map keys to bucket indices in an array,
giving O(1) average-case operations for get/put/remove.

What this actually is:
A single linked list that scans linearly for every operation.
No hashing. No buckets. No performance benefits whatsoever.

Time Complexity:
- put(key, value): O(n) - scans entire list to check for duplicates
- get(key): O(n) - linear search
- remove(key): O(n) - linear search
- contains(key): O(n) - linear search
- keys/values/items: O(n) - but at least this one makes sense

Space Complexity: O(n) for storing n items (same as real HashMap)

Why this is terrible:
1. Defeats the entire purpose of a HashMap
2. Gets slower as more items are added
3. Same performance as just using a list
4. The name "HashMap" is false advertising

The correct way:
Use Python's built-in dict, which is an actual hash table.
Or implement an actual hash map with:
- A hash function
- An array of buckets
- Collision handling (chaining or open addressing)

Educational value:
This demonstrates what HashMap is NOT. By removing all the hashing,
we're left with just a linked list, proving that the hash function
and bucket array are what make HashMaps fast.

Performance comparison:
This "HashMap": 1000 gets on 1000 items = ~500,000 comparisons
Real HashMap: 1000 gets on 1000 items = ~1,000 comparisons

Author's note: Every method is O(n). Every. Single. One.
"""

class Node:
    def __init__(self, key, value, next_node=None):
        self.key = key
        self.value = value
        self.next = next_node


class HashMap:
    def __init__(self):
        self.head = None

    def put(self, key, value):
        """
        Insert or update a key-value pair.
        This scans the entire linked list every time.
        Time Complexity: O(n)
        """
        if self.head is None:
            self.head = Node(key, value)
            return

        current = self.head

        while True:
            if current.key == key:
                current.value = value
                return

            if current.next is None:
                break

            current = current.next

        current.next = Node(key, value)

    def get(self, key):
        """
        Retrieve a value by key.
        This always searches linearly.
        Time Complexity: O(n)
        """
        current = self.head

        while current is not None:
            if current.key == key:
                return current.value
            current = current.next

        return None

    def remove(self, key):
        """
        Remove a key-value pair.
        Still a full linear scan.
        Time Complexity: O(n)
        """
        if self.head is None:
            return False

        if self.head.key == key:
            self.head = self.head.next
            return True

        previous = self.head
        current = self.head.next

        while current is not None:
            if current.key == key:
                previous.next = current.next
                return True

            previous = current
            current = current.next

        return False

    def contains(self, key):
        """
        Check if a key exists.
        Linear search again.
        """
        current = self.head

        while current is not None:
            if current.key == key:
                return True
            current = current.next

        return False

    def keys(self):
        """
        Return all keys in insertion order.
        """
        result = []
        current = self.head

        while current is not None:
            result.append(current.key)
            current = current.next

        return result

    def values(self):
        """
        Return all values in insertion order.
        """
        result = []
        current = self.head

        while current is not None:
            result.append(current.value)
            current = current.next

        return result

    def items(self):
        """
        Return all (key, value) pairs.
        """
        result = []
        current = self.head

        while current is not None:
            result.append((current.key, current.value))
            current = current.next

        return result
