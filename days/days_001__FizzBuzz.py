def fizzbuzz(n: int = 100) -> None:
    """
    Print FizzBuzz for 1..n using nested ternary (conditional) expressions only.
    """
    for i in range(1, n + 1):
        s = ("FizzBuzz" if i % 15 == 0
             else ("Fizz" if i % 3 == 0
                   else ("Buzz" if i % 5 == 0
                         else str(i))))
        print(s)

if __name__ == "__main__":
    fizzbuzz(30)  # example: prints FizzBuzz results for 1..30
