r"""
JSON PARSER USING ONLY REGEX AND STRING MANIPULATION

WARNING: This is the forbidden approach to parsing JSON.

What this does:
Parses JSON without using json.loads() or any proper parser library.
Instead, it uses:
- Regular expressions (the wrong tool for nested structures)
- String manipulation
- Manual tokenization
- eval() (security nightmare)
- Hope and prayers

The correct way:
    import json
    data = json.loads(text)

That's it. One line. Battle-tested, handles edge cases, doesn't explode.

Why this approach is terrible:

1. REGEX FOR NESTED STRUCTURES:
   JSON has nested objects/arrays. Regex is fundamentally bad at this.
   You can't properly parse recursive structures with regex alone.

2. USING eval():
   eval(value) for True/False/None is a SECURITY VULNERABILITY.
   If someone passes malicious input, eval() will execute it.
   Example: {"key": "__import__('os').system('rm -rf /')"}

3. STRING REPLACEMENT GOTCHAS:
   text.replace("true", "True") will also replace "true" inside strings!
   Example: {"name": "truth"} becomes {"name": "Truth"} (wrong!)

4. FRAGILE WHITESPACE HANDLING:
   The regex r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)' tries to remove whitespace
   outside strings, but this breaks on escaped quotes or complex nesting.

5. NO ERROR HANDLING:
   Invalid JSON will cause cryptic errors or silent failures.
   Real parsers give helpful error messages with line numbers.

6. DOESN'T HANDLE EDGE CASES:
   - Escaped characters in strings (\n, \t, \", \\)
   - Unicode escape sequences (\u0041)
   - Scientific notation (1e10)
   - Whitespace variations
   - Comments (some JSON parsers support them)

7. MANUAL BRACKET MATCHING:
   split_top_level() manually tracks depth with a counter.
   This breaks with malformed JSON or escaped brackets in strings.

Things that will break this parser:

1. Escaped quotes in strings:
   {"key": "He said \"hello\""}
   The split logic doesn't handle \" properly

2. True/false in string values:
   {"status": "true story"}
   Becomes {"status": "True story"} (wrong!)

3. Nested quotes:
   {"key": "It's \"true\" that this breaks"}

4. Unicode:
   {"emoji": "\u2764"}
   No handling for escape sequences

5. Numbers in scientific notation:
   {"big": 1e10}
   Not recognized by the int/float regex

6. Trailing commas:
   {"key": "value",}
   Will include empty string in split

7. Malicious input:
   {"evil": "__import__('os').system('ls')"}
   eval() will execute this!

Comparison with real JSON parser:

This parser:
- ~70 lines of fragile code
- Breaks on edge cases
- Security vulnerabilities
- No proper error messages
- Doesn't follow JSON spec

json.loads():
- One function call
- Handles all edge cases
- Battle-tested on millions of inputs
- Clear error messages
- Follows JSON RFC 8259 spec

Time Complexity: O(n²) - splits strings repeatedly
Space Complexity: O(n) - creates many intermediate strings
Security: O(please no)

Real JSON parsers use:
- Proper lexers/tokenizers
- Recursive descent parsing
- State machines
- AST (Abstract Syntax Tree) construction

This uses:
- String replacement
- Regex pattern matching
- eval() (forbidden in production)
- Manual character iteration

Why regex fails for JSON:
JSON is a Context-Free Grammar (CFG).
Regular expressions can only parse Regular Grammars.
CFG requires a pushdown automaton (stack-based).
Regex has no concept of a stack for nested structures.

Educational value:
- Shows why we use proper parsers
- Demonstrates regex limitations
- Illustrates security risks of eval()
- Proves that "it works on my test case" ≠ "it's correct"

Historical note:
The infamous Stack Overflow answer "You can't parse HTML with regex"
applies equally to JSON. Nested structures need proper parsers.

When this might be acceptable:
- Learning exercise (like this)
- Parsing trivial, trusted JSON (still not recommended)
- Job interview question (to test parsing knowledge)

When this is NEVER acceptable:
- Production code
- Parsing untrusted input
- Any system that needs reliability
- Anywhere security matters

Author's note: I used AI to help write this because proper parsing
                is complex. That's the point - use existing libraries
                that smart people have already debugged.
                Don't roll your own JSON parser.
"""

import re


def parse_json(text):
    """
    Parse JSON text into Python objects using string manipulation.

    This is the "quick and dirty" approach that seems to work until
    it spectacularly doesn't.

    Security Warning: Uses eval() which can execute arbitrary code!

    Args:
        text: JSON string to parse

    Returns:
        Python object (dict, list, str, int, float, bool, None)

    Raises:
        ValueError: On invalid JSON (maybe, if you're lucky)

    Things this doesn't handle:
    - Escaped quotes in strings
    - Unicode escape sequences
    - Scientific notation numbers
    - True/false/null inside string values
    - Pretty much any real-world JSON
    """
    text = text.strip()

    # Normalize JSON keywords (BREAKS if these appear in strings!)
    text = text.replace("true", "True")
    text = text.replace("false", "False")
    text = text.replace("null", "None")

    # Remove whitespace outside strings (fragile regex magic)
    # This regex tries to match whitespace not inside quotes
    # It breaks on escaped quotes and complex nesting
    text = re.sub(r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)', '', text)

    return parse_value(text)


def parse_value(value):
    """
    Determine the type of a JSON value and parse it accordingly.

    Uses a series of if statements and pattern matching.
    Real parsers use proper tokenization and lookahead.
    """
    if value.startswith("{"):
        return parse_object(value)
    if value.startswith("["):
        return parse_array(value)
    if value.startswith('"'):
        # Assumes no escaped quotes inside
        return value[1:-1]
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if value in ("True", "False", "None"):
        # SECURITY RISK: Using eval() on untrusted input
        # If someone passes "__import__('os').system('rm -rf /')"
        # this will execute it!
        return eval(value)

    raise ValueError("Unsupported JSON value: " + value)


def parse_object(text):
    """
    Parse a JSON object (dictionary).

    Assumes brackets are balanced and no escaped characters exist.
    Real parsers handle nesting and escaping properly.
    """
    obj = {}
    inner = text[1:-1]  # Remove { and }

    if not inner:
        return obj

    # Split by commas at the top level (not inside nested structures)
    pairs = split_top_level(inner, ",")

    for pair in pairs:
        # Split key:value (only the first colon)
        key, value = split_top_level(pair, ":", maxsplit=1)
        key = key.strip()[1:-1]  # remove quotes (assumes no escaping)
        obj[key] = parse_value(value)

    return obj


def parse_array(text):
    """
    Parse a JSON array (list).

    Uses the same fragile splitting logic as objects.
    """
    arr = []
    inner = text[1:-1]  # Remove [ and ]

    if not inner:
        return arr

    values = split_top_level(inner, ",")

    for value in values:
        arr.append(parse_value(value))

    return arr


def split_top_level(text, delimiter, maxsplit=-1):
    """
    Split a string by delimiter, but only at the top nesting level.

    How it works:
    - Track depth with a counter (increments on {[, decrements on }])
    - Only split when depth is 0 (not inside nested structure)

    Why this is fragile:
    - Doesn't handle escaped brackets in strings
    - Doesn't handle quotes properly
    - Breaks on malformed input

    Example that breaks:
        text = '{"key": "value with } bracket"}'
        # Will incorrectly split at the } inside the string

    Real parsers:
    - Use proper tokenization
    - Track string context separately
    - Handle escape sequences
    """
    parts = []
    depth = 0
    current = ""
    splits = 0

    for char in text:
        # Track nesting depth (assumes no strings contain brackets)
        if char in "{[":
            depth += 1
        elif char in "}]":
            depth -= 1

        # Split if we're at top level and haven't exceeded maxsplit
        if char == delimiter and depth == 0 and (maxsplit < 0 or splits < maxsplit):
            parts.append(current)
            current = ""
            splits += 1
        else:
            current += char

    parts.append(current)
    return parts


# Example usage and tests
if __name__ == "__main__":
    print("JSON Parser using Regex (The Forbidden Way)")
    print("=" * 50)

    # Simple cases that work
    simple = '{"name": "Alice", "age": 30, "active": true}'
    print("Simple object:", parse_json(simple))

    array = '[1, 2, 3, "four", null]'
    print("Array:", parse_json(array))

    nested = '{"person": {"name": "Bob", "scores": [85, 90, 95]}}'
    print("Nested:", parse_json(nested))

    print("\n" + "=" * 50)
    print("The correct way:")
    print("=" * 50)

    import json

    print("Simple:", json.loads(simple))
    print("Array:", json.loads(array))
    print("Nested:", json.loads(nested))

    print("\n" + "=" * 50)
    print("Cases that break this parser:")
    print("=" * 50)

    # Case 1: Escaped quotes
    escaped = '{"key": "He said \\"hello\\""}'
    print("\n1. Escaped quotes:", escaped)
    try:
        print("   Our parser:", parse_json(escaped))
    except Exception as e:
        print(f"   Our parser failed: {e}")
    print("   Real parser:", json.loads(escaped))

    # Case 2: True/false in strings
    true_in_string = '{"status": "true story"}'
    print("\n2. 'true' in string:", true_in_string)
    print("   Our parser:", parse_json(true_in_string))
    print("   Real parser:", json.loads(true_in_string))
    print("   (Notice they don't match!)")

    print("\n" + "=" * 50)
    print("Moral of the story: Use json.loads()")
    print("Don't parse JSON with regex.")
    print("=" * 50)