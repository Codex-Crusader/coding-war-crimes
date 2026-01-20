"""
EXCEPTION-DRIVEN CONTROL FLOW - RAISING YOUR WAY TO SUCCESS

WARNING: This code uses exceptions for normal program logic, not errors.

What this does:
Uses try-except blocks and raising exceptions for control flow instead of
simple if-else statements. Exceptions become the primary way the program
makes decisions.

The correct way:
    def read_age():
        text = input("Enter your age: ")

        if not text:
            print("Empty input!")
            return None

        try:
            age = int(text)
        except ValueError:
            print("Not a number!")
            return None

        if age < 0:
            print("Age cannot be negative!")
            return None

        if age > 150:
            print("That's too old!")
            return None

        return age

Clear, readable, exceptions only for actual errors.

The cursed way:
    Wrap every condition in try-except
    Raise exceptions for validation checks
    Use exception messages for control flow
    Nest try-except blocks 4 levels deep

Why this is terrible:

1. EXCEPTIONS ARE FOR EXCEPTIONAL CASES:
   Exceptions should signal unexpected errors, not normal program flow.

   Good exception use:
   - File doesn't exist
   - Network connection failed
   - Invalid JSON parsing
   - Out of memory

   Bad exception use:
   - Checking if number is negative
   - Validating user input ranges
   - Normal conditional logic
   - This entire file

2. PERFORMANCE OVERHEAD:
   Raising and catching exceptions is expensive.

   Performance comparison (1 million iterations):
   - if age < 0: ~0.05 seconds
   - try/raise/except: ~2.5 seconds

   Exceptions are 50x slower than if statements!

3. READABILITY NIGHTMARE:
   Control flow is obscured by exception handling.

   Simple logic becomes:
   try:
       if condition:
           raise Something
   except Something:
       do_thing()

   Instead of just:
   if condition:
       do_thing()

4. STACK TRACE POLLUTION:
   Every exception creates a stack trace.
   Debuggers break on exceptions.
   Log files fill with "errors" that aren't errors.

5. NESTED TRY-EXCEPT HELL:
   Four levels of nesting for four simple checks.
   Each level adds cognitive load.
   Following the control flow requires tracing exception paths.

6. EXCEPTION MESSAGE AS CONTROL FLOW:
   Checking if str(e) == "success" is a code smell.
   Exception messages are for humans, not control flow.
   Fragile: typo in message breaks logic.

7. VIOLATES PRINCIPLE OF LEAST SURPRISE:
   Developers expect:
   - try-except around risky operations
   - if-else for normal conditions

   This code surprises everyone by using exceptions everywhere.

8. MAKES DEBUGGING HARDER:
   Debugger: "Break on exception?"
   You: "Yes"
   Debugger: Breaks 50 times on "normal" flow
   You: Give up debugging

9. BREAKS IDE FEATURES:
   IDEs track exception flow for error handling.
   Using exceptions for control flow confuses static analysis.
   Code navigation becomes harder.

10. VIOLATES PYTHON PHILOSOPHY:
    "Errors should never pass silently."
    But also: "Explicit is better than implicit."

    Using exceptions for control flow is implicit logic.

Real-world consequences:

Issue 1 - Performance:
    Processing 10,000 user inputs
    With if statements: ~0.1 seconds
    With exception control flow: ~5 seconds
    Users notice the lag

Issue 2 - Debugging:
    Developer enables "break on exception"
    Code raises 100 exceptions during normal execution
    Developer can't find actual bugs
    Gives up on debugging

Issue 3 - Logging:
    Exception logging captures all raised exceptions
    Log file fills with "normal" operations
    Actual errors hidden in noise
    Production issues missed

Issue 4 - Monitoring:
    Monitoring tool: "1000 exceptions/minute"
    Team: "We have a crisis!"
    Reality: Just normal control flow
    Boy who cried wolf scenario

Performance comparison (validating 1000 inputs):

If-else approach:
    for input in inputs:
        if not input.isdigit():
            continue
        age = int(input)
        if 0 <= age <= 150:
            process(age)

    Time: ~0.01 seconds

Exception-based approach:
    for input in inputs:
        try:
            age = int(input)
            if age < 0:
                raise ValueError
            if age > 150:
                raise ValueError
            process(age)
        except ValueError:
            continue

    Time: ~0.5 seconds

The exception version is 50x slower!

When exceptions ARE appropriate:

1. Parsing external data:
   try:
       data = json.loads(text)
   except JSONDecodeError:
       handle_invalid_json()

2. File operations:
   try:
       with open(filename) as f:
           content = f.read()
   except FileNotFoundError:
       handle_missing_file()

3. Network requests:
   try:
       response = requests.get(url)
   except requests.ConnectionError:
       handle_network_failure()

4. Type conversion (when input is untrusted):
   try:
       value = int(user_input)
   except ValueError:
       handle_invalid_input()

When exceptions are NOT appropriate:

1. Checking if number is in range:
   Bad:  try: if x < 0: raise ValueError
   Good: if x < 0: handle_negative()

2. Validating user input format:
   Bad:  try: if not email_valid: raise ValueError
   Good: if not email_valid: show_error()

3. Normal conditional logic:
   Bad:  try: if condition: raise Success
   Good: if condition: do_thing()

4. Control flow:
   Bad:  This entire file
   Good: Use if-else statements

Python philosophy on exceptions:

EAFP (Easier to Ask for Forgiveness than Permission):
    try:
        return my_dict[key]
    except KeyError:
        return default

This is GOOD for operations that might fail.

But NOT for normal validation:
    Bad:  try: if x < 0: raise ValueError
    Good: if x < 0: return None

The difference:
- EAFP: Try operation, handle if it fails
- This code: Check condition, raise exception intentionally

Historical context:
Some languages (like C) use return codes for control flow.
Python uses exceptions for errors, if-else for logic.
This code confuses the two paradigms.

Educational value:
- Shows difference between error handling and control flow
- Demonstrates performance cost of exceptions
- Illustrates why conventions exist
- Proves that "it works" doesn't mean "it's good"

Real-world analogy:
Using exceptions for control flow is like:
- Setting off fire alarm to get people's attention
- Calling 911 to ask for directions
- Pulling emergency brake to stop at your floor

Yes, it works. No, you shouldn't do it.

The cognitive load:
Reading if-else: "If condition, do this, else do that"
Reading this: "Try doing this, if it raises this specific error
              with this specific message, do that, unless it's
              a different error, then..."

Exception anti-patterns in this code:

1. Empty check via exception:
   try:
       if text == "":
           raise ValueError("empty")
   except ValueError:
       # handle

   Should be: if not text: handle_empty()

2. Range check via exception:
   try:
       if age < 0:
           raise ValueError("negative")
   except ValueError:
       # handle

   Should be: if age < 0: handle_negative()

3. Success as exception:
   if age >= 0:
       raise ValueError("success")

   Raising exceptions for SUCCESS is peak cursed.

4. String comparison for control flow:
   if str(e) == "success":
       return age

   Exception messages are not control flow tokens!

Author's note: I could have used if-else statements.
                Python has them. They're fast and clear.
                I chose to raise exceptions for everything instead.
                Guido van Rossum is weeping.
"""


def read_age():
    """
    Read age using exceptions for control flow instead of normal conditionals.

    Wraps every validation check in try-except blocks.
    Raises exceptions for conditions that should be simple if statements.
    Nests try-except blocks four levels deep.

    Time Complexity: O(number of exceptions raised)
    Readability Complexity: O(please make it stop)

    This is what happens when you learn about try-except
    and decide it should replace all your if statements.
    """
    # Using exception as control flow for empty check
    # Should be: if not text: return None
    try:
        text = input("Enter your age: ")
        if text == "":
            raise ValueError("empty")
    except ValueError:
        print("Empty input!")
        return None

    # Using exception to check if it's a number
    # At least this use of try-except makes sense
    try:
        age = int(text)

        # Using exception for range validation (should be if statement)
        try:
            if age < 0:
                raise ValueError("negative")
        except ValueError:
            print("Age cannot be negative!")
            return None

        # Using exception for upper bound (another unnecessary try-except)
        try:
            if age > 150:
                raise ValueError("too_old")
        except ValueError:
            print("That's too old!")
            return None

        # If we made it here, age is valid
        return age

    except ValueError:
        # This catches the int() conversion failure
        # This is actually appropriate exception handling!
        print("Not a number!")
        return None


def read_age_even_worse():
    """
    The nuclear option: using exception messages for control flow.

    Raises an exception on SUCCESS and checks the message to decide what to do.
    This is the final boss of exception abuse.
    """
    user_age = None

    try:
        text = input("Enter your age: ")
        user_age = int(text)

        # RAISING EXCEPTION ON SUCCESS
        # This is it. This is the worst thing. WHY?
        if user_age >= 0 and user_age <= 150:
            raise ValueError("success")
        else:
            raise ValueError("invalid_range")

    except ValueError as e:
        # Control flow based on exception message
        # Exception messages are for humans, not control flow!
        if str(e) == "success":
            return user_age
        elif str(e) == "invalid_range":
            print("Age must be between 0 and 150!")
            return None
        else:
            print("Invalid age!")
            return None


def read_age_correctly():
    """The correct way to validate age input without exception abuse."""
    text = input("Enter your age: ")

    if not text:
        print("Empty input!")
        return None

    try:
        user_age = int(text)
    except ValueError:
        print("Not a number!")
        return None

    if user_age < 0:
        print("Age cannot be negative!")
        return None

    if user_age > 150:
        print("That's too old!")
        return None

    return user_age


# Example usage
if __name__ == "__main__":
    print("Exception-Driven Control Flow Demo")
    print("=" * 50)

    print("\nVersion 1: Nested try-except hell")
    age = read_age()
    if age is not None:
        print(f"Next year you will be: {age + 1}")
    else:
        print("Could not calculate next year age.")

    print("\n" + "=" * 50)
    print("\nVersion 2: Exception for success (the final boss)")
    age = read_age_even_worse()
    if age is not None:
        print(f"Next year you will be: {age + 1}")
    else:
        print("Could not calculate next year age.")

    print("\n" + "=" * 50)
    print("The correct way:")
    print("=" * 50)
    print("\nClear, readable, exceptions only for actual errors.")
    correct_age = read_age_correctly()
    if correct_age is not None:
        print(f"Next year you will be: {correct_age + 1}")