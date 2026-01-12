"""
CURSIVE FOR LOOP - RECURSION + GLOBAL STATE = CHAOS

The name "cursive" because:
- It's reCURSIVE
- It's CURSED
- Like cursive handwriting, everything flows together (into a mess)

What this does:
Replaces a simple for loop with recursive function calls and global state.
It's called "cursive" because the iterations flow into each other recursively,
and also because it's absolutely cursed.

The correct way:
    for i in range(start, end, step):
        action(i)

The cursive way:
    cursive_for(start, end, step, action)
    # (and pray you don't exceed the recursion limit)

How this monstrosity works:
1. Store loop counter in a GLOBAL variable
2. Check if we've reached the end
3. Execute the action callback
4. Increment the global counter
5. Recursively call ourselves
6. Hope we don't run out of stack space

Time Complexity: O(n) - same as a real loop
Space Complexity: O(n) - MUCH WORSE than a real loop due to call stack
Stack Depth: O(n) - will crash for large ranges
Bugs introduced: O(way too many)

Why this is catastrophically bad:

1. GLOBAL STATE:
   - current_index is shared across ALL calls
   - Not thread-safe
   - Not reentrant
   - Breaks if you nest loops or call twice

   Example of breakage:
   def action(x):
       cursive_for(0, 3, 1, print)  # Nested loop
   cursive_for(0, 5, 1, action)    # CHAOS ENSUES

2. RECURSION FOR ITERATION:
   - Each iteration adds a stack frame
   - Python's default recursion limit is ~1000
   - cursive_for(0, 10000, 1, action) → RecursionError
   - Regular for loop? No problem.

3. NO LOOP CONTROL:
   - Can't break early
   - Can't continue to next iteration
   - Can't use else clause
   - return/break/continue don't work as expected

4. MANUAL RESET:
   - Forgets to reset if exception occurs
   - Reset only happens at end
   - Calling with different ranges? Undefined behavior

5. CALLBACK HELL:
   - Have to wrap loop body in a function
   - Can't access outer scope naturally
   - No loop variable in scope

Real-world consequences:
- Stack overflow on large ranges
- Race conditions in multi-threaded code
- Impossible to debug
- Confuses every developer who reads it
- Makes code reviewers cry

Python recursion limit:
    import sys
    print(sys.getrecursionlimit())  # Usually 1000

    # This will crash:
    cursive_for(0, 2000, 1, lambda x: None)

    # This is fine:
    for i in range(2000):
        pass

Comparison:

Normal for loop:
    for i in range(1000000):
        print(i)
    # Works perfectly, O(1) space

This abomination:
    cursive_for(0, 1000000, 1, print)
    # RecursionError: maximum recursion depth exceeded

Performance overhead:
- Function call overhead on EVERY iteration
- Stack frame allocation for EVERY iteration
- Global variable lookup on EVERY iteration

When you might actually use recursion:
- Tree/graph traversal
- Divide and conquer algorithms
- Mathematical recurrence relations
- Functional programming patterns

When you should NEVER use recursion:
- Simple iteration (like this)
- Counting loops
- Array traversal
- Anything a for loop does better

Historical note:
Some languages (like Scheme) optimize tail recursion into loops.
Python does NOT. This will crash on large inputs.

Educational value:
- Shows that iteration and recursion are related concepts
- Demonstrates why we have loops
- Proves that "clever" solutions are often just "bad" solutions
- Teaches you about call stacks the hard way

The only acceptable use case:
Trolling your coworkers during code review.

Author's note: I could have typed 'for i in range(...)'.
                Instead I chose to make the call stack suffer.
                I have learned nothing.
"""

# Global loop counter (breaks everything if used concurrently)
current_index = 0


def cursive_for(start, end, step, action):
    """
    A cursive for loop - where iterations flow recursively into each other.

    Named "cursive" because:
    1. It's recursive
    2. It's cursed
    3. Like cursive writing, everything connects (badly)

    Args:
        start: Starting value (like range's start)
        end: Ending value (exclusive, like range's end)
        step: Increment per iteration
        action: Callback function that receives the current index

    Returns:
        None, but leaves global state modified as a gift

    Side effects:
        - Modifies global current_index
        - Calls action(i) for each iteration
        - Consumes call stack like it's going out of style

    Raises:
        RecursionError: If (end - start) / step exceeds recursion limit

    Example of what goes wrong:
        def print_range(idx):
            print(f"Outer: {idx}")
            # Nested loop - uses same global counter!
            cursive_for(0, 3, 1, lambda j: print(f"  Inner: {j}"))

        cursive_for(0, 5, 1, print_range)
        # Output: Complete chaos because global state is shared
    """
    global current_index

    # Initialize on first call (fragile assumption)
    if current_index == 0:
        current_index = start

    # Loop termination condition
    if current_index >= end:
        current_index = 0  # reset for reuse (doesn't help with nesting)
        return

    # Execute the loop body
    action(current_index)

    # Move to next iteration
    current_index += step

    # Recursive call replaces the next loop cycle
    # (and adds another frame to the call stack)
    cursive_for(start, end, step, action)


# Example usage
def print_number(idx):
    """Loop body as a callback function because why make things easy?"""
    print("Value:", idx)


if __name__ == "__main__":
    print("Cursive for loop demonstration:")
    print("=" * 50)
    cursive_for(start=0, end=5, step=1, action=print_number)

    print("\n" + "=" * 50)
    print("The correct way:")
    print("=" * 50)
    for counter in range(0, 5, 1):
        print("Value:", counter)

    print("\n" + "=" * 50)
    print("What happens with large ranges:")
    print("=" * 50)

    import sys

    print(f"Python recursion limit: {sys.getrecursionlimit()}")
    print(f"Trying to loop 2000 times...")

    try:
        cursive_for(0, 2000, 1, lambda x: None)
        print("Success! (somehow)")
    except RecursionError as e:
        print(f"RecursionError: {e}")
        print("A normal for loop would handle this just fine.")

    print("\n" + "=" * 50)
    print("What happens with nested loops:")
    print("=" * 50)


    def outer_action(outer_idx):
        print(f"Outer: {outer_idx}")
        # This will break because both loops share current_index
        cursive_for(0, 2, 1, lambda inner_idx: print(f"  Inner: {inner_idx}"))


    print("Attempting nested cursive_for...")
    try:
        cursive_for(0, 3, 1, outer_action)
    except Exception as e:
        print(f"Broke (as expected): {e}")

    print("\n" + "=" * 50)
    print("Remember: for loops exist for a reason.")
    print("Don't do this in real code.")
    print("=" * 50)