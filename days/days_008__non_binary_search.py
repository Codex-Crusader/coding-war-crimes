"""
PARANOID BINARY SEARCH - TRUST, BUT VERIFY (THE ENTIRE ARRAY)

WARNING: This defeats the entire purpose of binary search.

What this does:
1. Performs a correct O(log n) binary search
2. Then performs an O(n) linear search
3. "Just to be sure" the binary search was right

The result: O(n) complexity, same as linear search alone.

Why binary search exists:
To find elements in sorted arrays WITHOUT checking every element.
Binary search: O(log n) - checks ~10 elements in array of 1000
Linear search: O(n) - checks up to 1000 elements

What this does:
Binary search: checks ~10 elements ✓
Linear search: checks up to 1000 elements ✓✓
Total: checks ~1010 elements for no reason

Time Complexity: O(log n + n) = O(n)
Space Complexity: O(1)
Trust Issues: O(maximum)

Why this is absurd:

1. DEFEATS THE PURPOSE:
   Binary search is specifically designed to avoid checking every element.
   This checks every element anyway.

2. REDUNDANT VERIFICATION:
   If the data is sorted (required for binary search), both searches
   will ALWAYS find the same result. The verification is pointless.

3. WORSE PERFORMANCE:
   - Just binary search: O(log n)
   - Just linear search: O(n)
   - This "paranoid" version: O(n)

   We do MORE work to get the SAME result as the simpler approach!

4. THE OVERRIDE LOGIC:
   If binary search finds index 5 and linear search finds index 5,
   we "override" with... index 5. Completely pointless.

   The only way they differ is if:
   - Array is unsorted (binary search doesn't work anyway)
   - There's a bug in binary search (there isn't)
   - The universe is broken (possible, but unlikely)

5. TRUST ISSUES:
   This code doesn't trust its own binary search implementation.
   If you don't trust it, why write it?

When they might differ:

1. Unsorted array:
   data = [5, 2, 8, 1, 9]
   Binary search: undefined behavior (requires sorted array)
   Linear search: correct result

   But binary search REQUIRES sorted input, so this is misuse.

2. Duplicate elements:
   data = [1, 2, 3, 3, 3, 4, 5]
   target = 3
   Binary search: might find index 2, 3, or 4 (any is valid)
   Linear search: always finds index 2 (first occurrence)

   But both are correct answers!

Performance comparison (array of 1,000,000 elements):

Just binary search:
- Comparisons: ~20
- Time: microseconds

Just linear search:
- Comparisons: up to 1,000,000
- Time: milliseconds

Paranoid binary search:
- Comparisons: ~1,000,020
- Time: milliseconds (same as linear)
- Paranoia: priceless

The correct approaches:

Option 1 (trust binary search):
    left, right = 0, len(data) - 1
    while left <= right:
        mid = (left + right) // 2
        if data[mid] == target:
            return mid
        elif data[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return None

Option 2 (use linear search):
    for idx, value in enumerate(data):
        if value == target:
            return idx
    return None

Option 3 (use Python's built-in):
    import bisect
    idx = bisect.bisect_left(data, target)
    if idx < len(data) and data[idx] == target:
        return idx
    return None

Real-world analogy:
"I'll use GPS to navigate, but then I'll also walk the entire route
with a map to make sure GPS was right."

Why you might (wrongly) think this is a good idea:
- "What if binary search has a bug?"
  → Test it properly instead of checking every time
- "What if the array isn't sorted?"
  → That's a precondition violation, not a search problem
- "What if there are duplicates?"
  → Both approaches are correct, just return different valid indices

Educational value:
- Shows that combining two algorithms doesn't improve performance
- Demonstrates the difference between O(log n) and O(n)
- Proves that "verification" can be more expensive than the original work
- Illustrates that paranoia has a cost

Fun fact:
This is like having a spell-checker check your essay, then reading
every word yourself to make sure the spell-checker was right.

Author's note: Trust your algorithms. If you don't trust them,
                fix them, don't verify them every single time.
                This is like having trust issues with math.
"""


def paranoid_binary_search(data, target):
    """
    Binary search, but we check every element afterward because trust issues.

    Performs a binary search in O(log n) time, then immediately does
    a linear search in O(n) time "just to be sure."

    The result: O(n) performance with extra steps.

    Args:
        data: Sorted list of comparable elements
        target: Element to find

    Returns:
        Index of target if found, None otherwise

    Note: If binary search and linear search somehow disagree,
          we trust the linear search (the slower one, because paranoia)

    Performance:
        Best case: O(n) - still checks every element
        Average case: O(n) - still checks every element
        Worst case: O(n) - yep, checks every element

    The binary search part is just for show at this point.
    """
    left = 0
    right = len(data) - 1
    found_index = None

    # Step 1: Do a normal binary search (O(log n))
    while left <= right:
        mid = (left + right) // 2
        if data[mid] == target:
            found_index = mid
            break
        elif data[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    # Step 2: Check every element anyway (O(n)) just to be sure
    # because apparently we don't trust our own code
    for idx in range(len(data)):
        if data[idx] == target:
            # Override result if mismatch is found
            # (spoiler: there won't be a mismatch on sorted arrays)
            found_index = idx
            break

    return found_index


# Example usage and performance comparison
if __name__ == "__main__":
    import time

    print("Paranoid Binary Search - Trust Issues Edition")
    print("=" * 50)

    # Small example
    sample_data = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    search_value = 13

    result = paranoid_binary_search(sample_data, search_value)
    print(f"Found {search_value} at index: {result}")
    print(f"Verification (unnecessary): sample_data[{result}] = {sample_data[result]}")

    print("\n" + "=" * 50)
    print("Performance Comparison (1,000,000 elements)")
    print("=" * 50)

    # Large dataset
    large_data = list(range(0, 2000000, 2))  # 1 million even numbers
    search_target = 999998

    # Just binary search
    start = time.time()
    left_ptr, right_ptr = 0, len(large_data) - 1
    while left_ptr <= right_ptr:
        mid_ptr = (left_ptr + right_ptr) // 2
        if large_data[mid_ptr] == search_target:
            break
        elif large_data[mid_ptr] < search_target:
            left_ptr = mid_ptr + 1
        else:
            right_ptr = mid_ptr - 1
    binary_time = time.time() - start

    # Just linear search
    start = time.time()
    for position in range(len(large_data)):
        if large_data[position] == search_target:
            break
    linear_time = time.time() - start

    # Paranoid version
    start = time.time()
    paranoid_binary_search(large_data, search_target)
    paranoid_time = time.time() - start

    print(f"Binary search only: {binary_time * 1000:.4f} ms")
    print(f"Linear search only: {linear_time * 1000:.4f} ms")
    print(f"Paranoid (both):    {paranoid_time * 1000:.4f} ms")

    print(f"\nParanoid is {paranoid_time / binary_time:.1f}x slower than binary search")
    print(f"Paranoid is {paranoid_time / linear_time:.2f}x the time of linear search")

    print("\n" + "=" * 50)
    print("Moral: Trust your algorithms.")
    print("If you don't trust them, fix them.")
    print("Don't verify them on every single call.")
    print("=" * 50)