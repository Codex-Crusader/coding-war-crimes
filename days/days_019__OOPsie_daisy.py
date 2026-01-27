r"""
ENTERPRISE ADDITION ENGINE: OBJECT-ORIENTED ARITHMETIC AT ITS FINEST
NOW WITH ZERO INSTANCES AND EVEN LESS PURPOSE

WARNING:
This is the forbidden approach to adding two numbers.
All methods are static.
No objects are ever instantiated.
Classes exist purely as ceremonial namespaces.

We have successfully removed the LAST remaining excuse for OOP.

What this does:
Calculates 2 + 3 and prints the result (spoiler: it's still 5).

Instead of using normal arithmetic, it uses:
- Four separate classes for a single operation
- Static methods everywhere (because state is for cowards)
- No instances (but still classes, for vibes)
- Maximum ceremony
- Enterprise-grade architectural cosplay

The correct way:
    print(2 + 3)

The cursed way:
    Call static methods across multiple classes
    Pass values between them
    Pretend this is scalable

Why this approach is even worse now:

1. CLASSES WITHOUT OBJECTS:
   We are using classes
   Without instantiating them
   Without storing state
   Without polymorphism

   These are not objects.
   These are glorified folders.

2. STATIC METHODS FOR CONSTANTS:
   InputProvider.get() returns 2.
   SecondInputProvider.get() returns 3.

   This is the long way of writing:
       a = 2
       b = 3

   But with more steps.
   And more regret.

3. ZERO BENEFITS OF OOP:
   - No encapsulation
   - No state
   - No inheritance
   - No polymorphism

   Just namespaced functions pretending to be architecture.

4. COMMAND PATTERN IN NAME ONLY:
   We kept the shape of the pattern.
   We removed the reason for the pattern.

   This is architectural tax fraud.

5. FLEXIBILITY IS STILL WORSE THAN A FUNCTION:
   Want different numbers?
   Edit the class.
   Redeploy the system.
   Notify stakeholders.

   Meanwhile:
       print(x + y)
   Just works.

6. TESTING NIGHTMARE:
   Each static method needs its own test.
   For constants.
   For addition.
   For printing.

   Congratulations, your test suite is now larger than the problem.

Educational value:
- Demonstrates static methods
- Demonstrates misuse of classes
- Demonstrates how OOP can be reduced to ceremony
- Demonstrates why “enterprise” is sometimes a warning label

Author’s note:
We removed object instantiation.
We did not improve the code.
This is an achievement.
"""


class InputProvider:
    """
    Provider of the Sacred Number Two.
    Now static, because instances were unnecessary.
    """

    @staticmethod
    def execute() -> int:
        return 2


class SecondInputProvider:
    """
    Provider of the Even More Sacred Number Three.
    Entirely separate class, because reuse is overrated.
    """

    @staticmethod
    def execute() -> int:
        return 3


class AddOperation:
    """
    The '+' operator, wrapped in a class, exposed as a static method.

    This is not abstraction.
    This is pageantry.
    """

    @staticmethod
    def execute(a: int, b: int) -> int:
        return a + b


class PrintOperation:
    """
    A static wrapper around print().

    Because calling print() directly would be unprofessional.
    """

    @staticmethod
    def execute(value: int) -> None:
        print(value)


def main() -> None:
    """
    The Grand Static Orchestration.

    No objects.
    No state.
    No reason.
    """

    a = InputProvider.execute()
    b = SecondInputProvider.execute()
    result = AddOperation.execute(a, b)
    PrintOperation.execute(result)


if __name__ == "__main__":
    main()
