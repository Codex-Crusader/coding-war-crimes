"""
NULL CHECKS VIA EXCEPTIONS - BECAUSE IF STATEMENTS ARE TOO SIMPLE

WARNING: This code uses try-except blocks to check for None values.

What this does:
Uses exception handling to detect None values instead of simple if statements.
Wraps null checks in try-except blocks for maximum inefficiency.

The correct way:
    def get_uppercase_name(user):
        if user is None:
            return "UNKNOWN"
        if user.name is None:
            return "UNKNOWN"
        return user.name.upper()

Clear, direct, efficient.

The cursed way:
    try:
        _ = user.name
        if user is None:
            raise ValueError("user_none")
    except (AttributeError, ValueError):
        return "UNKNOWN"

Convoluted, slow, confusing.

Why this is terrible:

1. EXCEPTIONS FOR NORMAL CONDITIONS:
   None is not an exceptional case - it's a normal, expected state.

   Good exception use: File doesn't exist, network timeout
   Bad exception use: Checking if variable is None

   Checking for None is a common operation, not an error.

2. PERFORMANCE OVERHEAD:
   Simple if check: ~0.00001 seconds
   Try-except with raise: ~0.0001 seconds

   10x slower for something Python does all the time!

   Performance comparison (1 million null checks):
   - if user is None: ~0.05 seconds
   - try-except pattern: ~0.5 seconds

3. LOGIC CONTRADICTION:
   Code flow:
   1. Access user.name (fails if user is None)
   2. Then check if user is None (but we already accessed it!)

   If user is None, step 1 raises AttributeError.
   Step 2 never executes.
   The if check is pointless.

4. MIXED EXCEPTION TYPES:
   Catches both AttributeError AND ValueError

   Why?
   - AttributeError: When user is None (step 1 fails)
   - ValueError: When we manually raise it (step 2)

   Two different exception types for one logical check.
   Confusing and fragile.

5. RAISING EXCEPTIONS MANUALLY FOR CHECKS:
   if user.name is None:
       raise ValueError("name_none")

   This is literally:
   - Check condition with if
   - Raise exception
   - Catch exception immediately
   - Return value

   Just use the if statement directly!

6. EXCEPTION MESSAGE AS SIGNAL:
   raise ValueError("name_none")

   The message "name_none" is meaningless to exception handler.
   We catch ValueError regardless of message.
   Just control flow theater.

7. REDUNDANT ASSIGNMENT:
   _ = user.name

   Accessing attribute just to trigger AttributeError.
   Not using the value, just checking if access works.

   Compare: if user is None (direct, clear)

8. HARDER TO DEBUG:
   With if statements:
   - Set breakpoint
   - Step through conditions
   - Clear flow

   With exceptions:
   - Exception raised
   - Jump to handler
   - Was it AttributeError or ValueError?
   - Which check failed?
   - Confusion ensues

9. READABILITY NIGHTMARE:
   Reading if statements: "If user is None, return UNKNOWN"
   Reading this: "Try accessing name, or if None raise error,
                  catch attribute or value errors, return unknown"

   Same logic, 5x more words to explain.

10. VIOLATES PYTHON'S "EXPLICIT IS BETTER THAN IMPLICIT":
    if user is None: return "UNKNOWN"

    Explicit: Checking if user is None

    try: _ = user.name
    except AttributeError: return "UNKNOWN"

    Implicit: Relying on AttributeError to detect None

Real-world consequences:

Issue 1 - Performance at Scale:
    Processing 1 million user objects
    With if checks: ~5 seconds total
    With exception checks: ~50 seconds total
    Users notice the lag

Issue 2 - Debugging Production:
    Error logs filled with "caught AttributeError"
    Are these expected (null checks) or bugs?
    Can't distinguish real errors from flow control
    Actual bugs hidden in noise

Issue 3 - Code Review:
    Reviewer: "Why are we catching exceptions for null checks?"
    Author: "Because..."
    Reviewer: "Just use if statements"
    PR rejected

Issue 4 - New Developer Onboarding:
    New dev: "Why try-except instead of if?"
    Senior dev: "Because... uh... someone thought it was clever?"
    New dev: Questions life choices

The logical flow breakdown:

Step 1: _ = user.name
- If user is None: AttributeError raised → caught → return "UNKNOWN"
- If user is not None: Access succeeds, continue

Step 2: if user is None: raise ValueError
- This NEVER executes when user is None
- Because step 1 already caught it
- This only checks redundantly when user is NOT None
- Then we raise ValueError anyway? No, we don't reach raise
- This entire check is dead code

Step 3: if user.name is None: raise ValueError
- Check if name is None
- If yes, raise exception
- Immediately catch it
- Could just: if user.name is None: return "UNKNOWN"

Performance comparison (checking 10,000 users):

Method 1 - If statements:
    if user is None:
        return "UNKNOWN"
    if user.name is None:
        return "UNKNOWN"
    return user.name.upper()

    Time: ~0.01 seconds
    Clear: Yes
    Debuggable: Yes

Method 2 - This cursed approach:
    Time: ~0.1 seconds (10x slower)
    Clear: No
    Debuggable: No

The correct approaches:

Option 1 - Guard clauses:
    def get_uppercase_name(user):
        if user is None:
            return "UNKNOWN"
        if user.name is None:
            return "UNKNOWN"
        return user.name.upper()

Option 2 - Early return:
    def get_uppercase_name(user):
        if user is None or user.name is None:
            return "UNKNOWN"
        return user.name.upper()

Option 3 - Ternary (if you like one-liners):
    def get_uppercase_name(user):
        return user.name.upper() if (user and user.name) else "UNKNOWN"

Option 4 - EAFP (when appropriate):
    def get_uppercase_name(user):
        try:
            return user.name.upper()
        except AttributeError:
            return "UNKNOWN"

    This is GOOD - tries operation, handles failure
    Different from checking for None with exceptions

When exceptions ARE appropriate:

1. Operation might fail (EAFP):
    try:
        return user.name.upper()
    except AttributeError:
        return "UNKNOWN"

    Good: Attempts operation, handles failure

2. External operations:
    try:
        data = file.read()
    except FileNotFoundError:
        data = default_data

3. Parsing operations:
    try:
        value = int(text)
    except ValueError:
        value = 0

When exceptions are NOT appropriate:

1. Checking for None (this file):
    Bad:  try: _ = user.name except AttributeError: return
    Good: if user is None: return

2. Checking empty strings:
    Bad:  try: if not text: raise ValueError except: return
    Good: if not text: return

3. Checking numeric ranges:
    Bad:  try: if x < 0: raise ValueError except: return
    Good: if x < 0: return

4. Any check you can do with if:
    Bad:  Using exceptions
    Good: Using if statements

The EAFP vs LBYL confusion:

EAFP (Easier to Ask Forgiveness than Permission):
    try:
        return dict[key]
    except KeyError:
        return default

    Good: Try operation, handle failure

LBYL (Look Before You Leap):
    if key in dict:
        return dict[key]
    else:
        return default

    Also good: Check first, then act

This code (WRONG):
    try:
        if user is None:
            raise ValueError
    except ValueError:
        return default

    Wrong: Check with if, THEN raise exception
    This is LBYL wrapped in exception handling

Historical context:
Some languages (like Java) use exceptions more liberally.
Python prefers explicit checks for expected conditions.
None is an expected, normal value in Python.

Educational value:
- Shows difference between control flow and error handling
- Demonstrates when NOT to use exceptions
- Illustrates performance cost of exceptions
- Proves that "it works" doesn't mean "it's right"

Real-world analogy:
Using exceptions for null checks is like:
- Throwing a ball at a wall to see if the wall exists
- Instead of just looking at the wall
- Then catching the ball and saying "yep, wall exists"

Both work. One is obviously stupid.

The cognitive load:
Reading if statement: "If user is None, return unknown"
Reading this: "Try accessing user's name, unless user is None which
              raises attribute error or we manually raise value error
              if name is None, then catch either error and return unknown"

Author's note: I could have used if statements.
                They're literally designed for this.
                I chose to wrap everything in try-except instead.
                Doof style.... FEAR ME!!
"""

class User:
    """Simple user class for demonstration."""
    def __init__(self, name: str | None = None):
        self.name = name

def get_uppercase_name(user):
    """
    Using exceptions to check for None instead of 'if user is None'.

    This function demonstrates the anti-pattern of using exception handling
    for normal null checks instead of simple if statements.

    Time Complexity: O(1) but with exception overhead
    Space Complexity: O(1)
    Readability: O(why)

    Returns:
        str: Uppercase name or "UNKNOWN"
    """

    # Null check #1: Check if user is None (WRONG APPROACH)
    try:
        # Force AttributeError if user is None
        # This line exists ONLY to trigger an exception
        _ = user.name

        # This check happens AFTER we already accessed .name
        # If user was None, AttributeError was already raised above
        # So this check NEVER executes when user is None
        # This is dead code when user is None!
        if user is None:
            raise ValueError("user_none")

    except (AttributeError, ValueError):
        # Catches two different exception types for one logical check:
        # - AttributeError: from accessing user.name when user is None
        # - ValueError: from manually raising it (which never happens)
        return "UNKNOWN"

    # Null check #2: Check if name is None (STILL WRONG)
    try:
        # Check if name is None using if statement
        if user.name is None:
            # Then raise an exception
            raise ValueError("name_none")
    except ValueError:
        # Then immediately catch the exception we just raised
        # Why not just: if user.name is None: return "UNKNOWN" ?
        return "UNKNOWN"

    # Finally do the actual thing (after all that ceremony)
    return user.name.upper()


def get_uppercase_name_correct(user):
    """
    The correct way: Simple if statements.

    Clear, fast, debuggable, maintainable.
    """
    if user is None:
        return "UNKNOWN"
    if user.name is None:
        return "UNKNOWN"
    return user.name.upper()


def get_uppercase_name_eafp(user):
    """
    EAFP approach (also correct).

    Tries the operation, handles failure.
    This is actually good Python style when appropriate.
    """
    try:
        return user.name.upper()
    except AttributeError:
        return "UNKNOWN"


# Example usage and comparison
if __name__ == "__main__":
    import time

    print("Null Checks via Exceptions - Performance Comparison")
    print("=" * 50)

    # Test data
    user1 = User("bhargavaram")
    user2 = User(None)
    user3 = None

    print("\nTesting exception-based approach:")
    print(f"User with name: {get_uppercase_name(user1)}")
    print(f"User with None name: {get_uppercase_name(user2)}")
    print(f"None user: {get_uppercase_name(user3)}")

    print("\nTesting correct if-based approach:")
    print(f"User with name: {get_uppercase_name_correct(user1)}")
    print(f"User with None name: {get_uppercase_name_correct(user2)}")
    print(f"None user: {get_uppercase_name_correct(user3)}")

    print("\nTesting EAFP approach:")
    print(f"User with name: {get_uppercase_name_eafp(user1)}")
    print(f"User with None name: {get_uppercase_name_eafp(user2)}")
    print(f"None user: {get_uppercase_name_eafp(user3)}") # Just ignore the warning. the code works fine.
    # Just the Type checker trying to be helpful.... but I hate the yellow line

    print("\n" + "=" * 50)
    print("Performance Comparison (100,000 iterations)")
    print("=" * 50)

    test_users = [User("test"), User(None), None] * 10000

    # Exception-based approach
    start = time.time()
    for test_user in test_users:
        get_uppercase_name(test_user)
    exception_time = time.time() - start

    # If-based approach
    start = time.time()
    for test_user in test_users:
        get_uppercase_name_correct(test_user)
    if_time = time.time() - start

    # EAFP approach
    start = time.time()
    for test_user in test_users:
        get_uppercase_name_eafp(test_user)
    eafp_time = time.time() - start

    print(f"\nException-based null checks: {exception_time:.4f}s")
    print(f"If-statement null checks:    {if_time:.4f}s")
    print(f"EAFP approach:               {eafp_time:.4f}s")

    print(f"\nException approach is {exception_time / if_time:.1f}x slower than if statements")
    print(f"EAFP approach is {eafp_time / if_time:.1f}x the speed of if statements")

    print("\n" + "=" * 50)
    print("The correct way:")
    print("=" * 50)
    print("""
def get_uppercase_name(user):
    if user is None:
        return "UNKNOWN"
    if user.name is None:
        return "UNKNOWN"
    return user.name.upper()

Or use EAFP when appropriate:

def get_uppercase_name(user):
    try:
        return user.name.upper()
    except AttributeError:
        return "UNKNOWN"
    """)
    print("=" * 50)

# it is a bird? it's a plane? i am in a lot of pain!!!!