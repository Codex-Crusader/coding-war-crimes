"""
STRING-ONLY CALCULATOR - A CRIME AGAINST COMPUTER SCIENCE

WARNING: This code is intentionally terrible. Do NOT use this in production.
Do NOT use this for homework. Do NOT show this to your CS professor unless
you want them to cry.

PURPOSE:
This is an educational exercise in understanding WHY we have built-in
numeric types and operators. By reimplementing basic arithmetic using ONLY
string manipulation, we learn to appreciate abstraction and realize that
sometimes the "simple" way is simple for a very good reason.

WHAT MAKES THIS CURSED:
- All numbers are strings throughout the entire calculation
- Uses ord() and chr() to convert between characters and ASCII codes
- Manually implements elementary school arithmetic (carrying, borrowing)
- Division uses repeated string subtraction (extremely inefficient)
- Decimal handling involves manual string padding and alignment
- Every operation requires multiple string reversals and concatenations
- The entire thing converts strings → ASCII → math → ASCII → strings

WHY THIS IS A BAD IDEA:
1. Performance: O(n²) or worse for operations that should be O(1)
2. Precision: Fixed decimal precision with manual rounding errors
3. Complexity: 200+ lines for what `+` does in one character
4. Maintainability: Good luck debugging "chr(ord(a[i]) - 48)"
5. Memory: Creating/destroying strings constantly instead of using registers

WHAT YOU SHOULD ACTUALLY DO:
Just use Python's built-in int and float types. Seriously.
They're implemented in C, optimized, and actually correct.

THE PROPER WAY:
    def calculator(x, y, op):
        if op == "+": return x + y
        if op == "-": return x - y
        if op == "*": return x * y
        if op == "/": return x / y

That's it. Four lines. Don't be like this code.

EDUCATIONAL VALUE:
- Shows how arithmetic works at the digit level
- Demonstrates the cost of avoiding proper abstractions
- Makes you appreciate your programming language's type system
- Proves that "clever" code is usually just "bad" code

If you're reading this and thinking "this is horrible" - GOOD.
That means you understand why we don't do this in real code.

Author's Note: I wrote this to learn WHY it's wrong. Please don't
                use it for anything except laughing at how bad it is.
"""

PRECISION = 5


def strip_leading_zeros(s):
    return s.lstrip("0") or "0"


def normalize_decimal(s):
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


def add_strings(a, b):
    if "." in a or "." in b:
        a, b = align_decimals(a, b)
    carry = 0
    res = []
    a, b = a[::-1], b[::-1]

    for i in range(max(len(a), len(b))):
        da = ord(a[i]) - 48 if i < len(a) and a[i] != "." else 0
        db = ord(b[i]) - 48 if i < len(b) and b[i] != "." else 0
        if (i < len(a) and a[i] == ".") or (i < len(b) and b[i] == "."):
            res.append(".")
            continue
        total = da + db + carry
        carry = total // 10
        res.append(chr(total % 10 + 48))

    if carry:
        res.append(chr(carry + 48))

    return normalize_decimal("".join(res[::-1]))


def subtract_strings(a, b):
    if "." in a or "." in b:
        a, b = align_decimals(a, b)
    borrow = 0
    res = []
    a, b = a[::-1], b[::-1]

    for i in range(len(a)):
        if a[i] == ".":
            res.append(".")
            continue
        da = ord(a[i]) - 48 - borrow
        db = ord(b[i]) - 48 if i < len(b) and b[i] != "." else 0
        if da < db:
            da += 10
            borrow = 1
        else:
            borrow = 0
        res.append(chr(da - db + 48))

    return normalize_decimal(strip_leading_zeros("".join(res[::-1])))


def multiply_strings(a, b):
    decs = a.count(".") + b.count(".")
    a = a.replace(".", "")
    b = b.replace(".", "")

    res = "0"
    for i, db in enumerate(b[::-1]):
        carry = 0
        temp = ["0"] * i
        for da in a[::-1]:
            prod = (ord(da) - 48) * (ord(db) - 48) + carry
            carry = prod // 10
            temp.append(chr(prod % 10 + 48))
        if carry:
            temp.append(chr(carry + 48))
        res = add_strings(res, "".join(temp[::-1]))

    if decs:
        res = res[:-decs] + "." + res[-decs:]
    return normalize_decimal(res)


def divide_strings(a, b):
    if b == "0":
        raise ZeroDivisionError("division by zero")

    decs = 0
    if "." in a:
        decs += len(a) - a.index(".") - 1
        a = a.replace(".", "")
    if "." in b:
        decs -= len(b) - b.index(".") - 1
        b = b.replace(".", "")

    a += "0" * PRECISION
    quotient = []
    remainder = "0"

    for digit in a:
        remainder = strip_leading_zeros(remainder + digit)
        count = 0
        while subtract_strings(remainder, b)[0] != "-":
            remainder = subtract_strings(remainder, b)
            count += 1
        quotient.append(chr(count + 48))

    res = strip_leading_zeros("".join(quotient))
    if decs + PRECISION > 0:
        res = res[:- (decs + PRECISION)] + "." + res[- (decs + PRECISION):]
    return normalize_decimal(res)


def align_decimals(a, b):
    if "." not in a:
        a += ".0"
    if "." not in b:
        b += ".0"
    da = len(a) - a.index(".") - 1
    db = len(b) - b.index(".") - 1
    if da > db:
        b += "0" * (da - db)
    elif db > da:
        a += "0" * (db - da)
    return a, b


def string_calculator(x, y, op):
    x = str(x)
    y = str(y)
    return (
        add_strings(x, y) if op == "+" else
        subtract_strings(x, y) if op == "-" else
        multiply_strings(x, y) if op == "*" else
        divide_strings(x, y) if op == "/" else
        "ERR"
    )


# Examples
print(string_calculator("12.5", "3.4", "+"))
print(string_calculator("20", "7", "-"))
print(string_calculator("3.2", "1.5", "*"))
print(string_calculator("10", "4", "/"))