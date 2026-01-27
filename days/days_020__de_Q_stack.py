r"""
STACK USING A QUEUE (BY USING THE WRONG END): A MASTERCLASS IN MISSING THE POINT

WARNING: This is the forbidden approach to implementing a stack with a queue.

What this does:
Implements a stack data structure using Python's deque (double-ended queue).
But instead of doing the actual challenge (making a queue behave like a stack),
it just... uses the queue as a stack by accessing the wrong end.

The actual challenge:
Implement a stack using a queue where you can ONLY use queue operations
(enqueue to back, dequeue from front). This forces you to rearrange elements
on every push or pop to maintain LIFO (Last In First Out) order.

What this code does instead:
Uses a deque and accesses BOTH ends, which is literally just... a stack.
Python's deque already supports stack operations natively. We're not
implementing anything; we're just renaming existing functionality.

Why this approach is cheating:

1. NOT A QUEUE IMPLEMENTATION:
   A proper queue has ONE input end and ONE output end (FIFO).
   This code uses BOTH ends of the deque, making it a deque, not a queue.
   It's like being asked to "make a bicycle from a car" and you just
   remove two wheels and call it done.

2. MISSES THE ENTIRE POINT:
   The interview question "implement a stack using a queue" is designed to
   test your understanding of:
   - How stacks work (LIFO: Last In First Out)
   - How queues work (FIFO: First In First Out)
   - How to transform one behavior into another
   - Algorithm design with constrained operations

   This implementation tests: Can you call deque.pop() instead of deque.popleft()?

3. USES A DEQUE, NOT A QUEUE:
   Python's deque (double-ended queue) is NOT a simple queue.
   It's a data structure that supports O(1) operations at BOTH ends.
   Using a deque for this problem is like bringing a Swiss Army knife
   to a "build tools from scratch" competition.

4. NO ALGORITHMIC CHALLENGE:
   The real challenge requires either:
   - O(n) push operations (rearrange queue on every push)
   - O(n) pop operations (rearrange queue on every pop)

   This implementation: O(1) for everything because it's not actually
   solving the problem. It's just using stack operations directly.

5. TECHNICALLY CORRECT, MORALLY WRONG:
   Yes, a deque IS a type of queue (it's in the name!).
   But it's a SPECIAL queue that defeats the purpose of the exercise.
   It's like answering "how do you get water from a well?" with
   "I turn on the tap" because technically the tap is connected to wells.

The actual correct implementation (with real constraints):

There are two proper approaches to implement a stack using a REAL queue
(where you can only append to the right and popleft from the left):

APPROACH 1: Make push() expensive - O(n)
When pushing a value:
1. Add the new value to the queue
2. Rotate all previous elements to the back
   (dequeue and re-enqueue n-1 times)
Result: The newest element is always at the front

APPROACH 2: Make pop() expensive - O(n)
When popping a value:
1. Move all elements except the last to a temporary queue
2. Remove and return the last element
3. Move everything back
Result: We simulate reaching the "top" of the stack

What this code does instead:
Just accesses the right end of the deque directly. No rotation,
no rearrangement, no challenge. It's the programming equivalent of
a participation trophy.

Things wrong with this implementation:

1. Not using queue operations:
   Real queue: append() and popleft()
   This code: append() and pop() (that's stack operations!)

2. No actual algorithm:
   There's no interesting logic here. It's just:
   - push() calls append()
   - pop() calls pop()
   - peek() accesses [-1]

   This is literally just wrapping deque methods with different names.

3. Interview disaster:
   Interviewer: "Implement a stack using a queue"
   Candidate: *submits this code*
   Interviewer: "But you're using both ends of the deque..."
   Candidate: "A deque is a queue!"
   Interviewer: "...we'll be in touch."

Comparison with proper implementation:

This implementation:
class StackUsingQueueWrongEnd:
    def push(self, value):
        self._queue.append(value)  # O(1)

    def pop(self):
        return self._queue.pop()  # O(1) - just using stack operations

Proper implementation (push expensive):
class StackUsingQueue:
    def push(self, value):
        self._queue.append(value)
        # Rotate: move all previous elements to the back
        for _ in range(len(self._queue) - 1):
            self._queue.append(self._queue.popleft())  # O(n)

    def pop(self):
        return self._queue.popleft()  # O(1) - front is the top

Proper implementation (pop expensive):
class StackUsingQueue:
    def push(self, value):
        self._queue.append(value)  # O(1)

    def pop(self):
        # Move all but last element to temp, return last
        for _ in range(len(self._queue) - 1):
            self._queue.append(self._queue.popleft())  # O(n)
        return self._queue.popleft()

Time Complexity Comparison:

This "solution":
- push(): O(1) - just append
- pop(): O(1) - just pop from right end
- peek(): O(1) - just access [-1]
Total: Too good to be true (because it's not solving the problem)

Proper solution:
- push(): O(n) or O(1) depending on approach
- pop(): O(1) or O(n) depending on approach
- peek(): O(1) always
Total: Actual algorithmic work being done

Space Complexity: O(n) for both (same, at least we got this right)

What the interviewer is testing:

1. UNDERSTANDING OF DATA STRUCTURES:
   Do you know the difference between stack (LIFO) and queue (FIFO)?

2. ALGORITHM DESIGN:
   Can you transform one behavior into another with constraints?

3. TRADE-OFF ANALYSIS:
   Which operation should be expensive - push or pop?

4. PROBLEM SOLVING:
   Can you work within limitations to achieve a goal?

This implementation tests:
Can you use a deque? (Not impressive for a technical interview)

Real-world analogies:

This solution is like:
- Being asked to "make coffee without a coffee maker" and using a Keurig
  (technically not a "coffee maker" but come on...)
- Asked to "get to the airport without a car" and taking an Uber
  (you're still in a car, you're just not driving)
- Asked to "build a bridge" and just finding a different bridge
  (problem avoided, not solved)
- Asked to "cook without an oven" and using a microwave
  (technically correct, spiritually wrong)

Why people write code like this:

1. MISUNDERSTANDING THE PROBLEM:
   "They said use a queue, deque has 'queue' in the name!"

2. TAKING THE PATH OF LEAST RESISTANCE:
   Why do hard algorithmic work when you can just use existing methods?

3. GETTING TOO CLEVER:
   "A deque IS a queue, so technically I'm right..."
   (Being technically right while missing the point)

4. NOT READING THE CONSTRAINTS:
   Skipped the part where it said "using only queue operations"

5. CARGO CULT PROGRAMMING:
   "I saw someone use deque for a queue problem once..."

Educational value:

This code teaches us:
- How NOT to approach algorithmic challenges
- The difference between solving a problem and avoiding it
- Why constraints matter in interview questions
- That "technically correct" can still be completely wrong
- The importance of understanding WHY you're being asked something

Interview red flags:

If a candidate submits this as their solution:
1. They didn't understand the problem constraints
2. They're trying to game the system
3. They lack fundamental understanding of data structures
4. They think being clever is better than being thorough

Proper interview follow-up:
"Interesting! Now implement it using ONLY append() and popleft() operations."
*watches candidate's face as they realize they need to actually solve it*

The Stack Overflow question this answers:
Q: "How do I implement a stack?"
A: "Just use a stack"
Comments: "That's not what they're asking..."

What this code is really doing:

Renaming operations:
- Stack.push() -> deque.append()
- Stack.pop() -> deque.pop()
- Stack.peek() -> deque[-1]

That's it. That's the whole implementation. It's a wrapper with
extra steps and a misleading name.

Moral of the story:
- Read problem constraints carefully
- Understand the SPIRIT of the problem, not just the letter
- Using the right data structure for the wrong reasons is still wrong
- Interview questions test understanding, not cleverness
- If your solution seems too easy, you're probably missing something
- A deque might have "queue" in the name, but using both ends makes it not a queue

When this approach is acceptable:
- Never in an interview context
- Never when learning algorithms
- Maybe for quick prototyping if you really don't care about the problem

When this approach is NEVER acceptable:
- Technical interviews
- Algorithm courses
- Anywhere the POINT is to learn the constraint-based solution
- When someone specifically asks for single-ended queue operations

Remember: The goal isn't just to make it work. The goal is to demonstrate
understanding of data structures, algorithm design, and problem-solving
within constraints. This code demonstrates none of that.

Don't be the candidate who thinks they're clever for avoiding the problem.
Be the candidate who solves it properly.
"""

from collections import deque


class StackUsingQueueWrongEnd:
    """
    A "Stack" Implementation Using a Queue (by completely missing the point).

    Problem: Implement a stack using a queue with only queue operations.
    Solution: Use a deque and access the wrong end.
    Result: We've implemented a stack using... stack operations.

    This is the algorithmic equivalent of:
    - Being asked to "make a sandwich without bread" and using a tortilla
      (technically not bread, but you know what they meant)
    - Being asked to "run a marathon" and taking an Uber
      (you got to the finish line, but...)

    What we should be doing:
    Using ONLY enqueue (append) and dequeue (popleft) operations from
    one end, forcing us to rotate elements to maintain LIFO behavior.

    What we're actually doing:
    Using append() and pop() which are literally just stack operations.

    Interview performance: F
    Technical correctness: D (a deque IS a queue, technically...)
    Understanding of the problem: F-
    """

    def __init__(self) -> None:
        # Initialize a deque (double-ended queue)
        # This data structure supports O(1) operations at BOTH ends
        # Which is exactly what makes this solution cheating
        #
        # A real queue for this problem should only allow:
        # - append() to add to the right
        # - popleft() to remove from the left
        #
        # But deque also allows:
        # - appendleft() to add to the left
        # - pop() to remove from the right
        #
        # We're about to use that second set of operations,
        # which defeats the entire purpose of the exercise.
        self._queue = deque()

    def push(self, value: int) -> None:
        """
        Push a value onto the stack.

        What we do: Call deque.append() - a queue operation (so far so good!)
        Time complexity: O(1)

        What we SHOULD do if solving this properly:
        Either:
        1. Append the value, then rotate all previous elements
           to the back so the new value ends up at the front
           (makes push O(n) but pop O(1))
        2. Just append normally and deal with the complexity in pop()
           (makes push O(1) but pop O(n))

        What we actually do:
        Just append. No rotation. No rearrangement. We're counting on
        pop() to access the wrong end later.
        """
        # Enqueue normally (this part is actually correct queue behavior)
        self._queue.append(value)

    def pop(self) -> int:
        """
        Pop a value from the stack.

        THIS IS WHERE THE CHEATING HAPPENS.

        What we do: Call deque.pop() - removes from RIGHT end
        What a queue does: popleft() - removes from LEFT end
        What we should do: Use popleft() and handle the rearrangement

        By using pop() instead of popleft(), we're accessing the "wrong"
        end of the queue, which conveniently gives us stack behavior
        without any actual algorithmic work.

        This is like being asked "How do you reverse a string?" and
        answering "I call the reverse() method". Technically works,
        but you've learned nothing.

        Time complexity: O(1) - suspiciously efficient for a constrained problem
        """
        if not self._queue:
            raise IndexError("pop from empty stack")

        # WRONG END DEQUEUE
        # A queue should pop from the LEFT (FIFO - First In First Out)
        # We pop from the RIGHT (LIFO - Last In First Out)
        #
        # This is literally just... stack behavior. We're not converting
        # anything. We're just using the deque as a stack.
        return self._queue.pop()

    def peek(self) -> int:
        """
        Peek at the top of the stack without removing it.

        More wrong-end access. We check the RIGHT end (stack top)
        instead of the LEFT end (queue front).

        If we were doing this properly, the "top" of our stack would be
        at the front of the queue (left end), and we'd access it with
        self._queue[0].

        But we're not doing it properly. We're just using stack operations.
        """
        if not self._queue:
            raise IndexError("peek from empty stack")

        # Access the right end (stack behavior)
        # Should access the left end if we were using queue operations
        return self._queue[-1]

    def is_empty(self) -> bool:
        """
        Check if the stack is empty.

        At least we can't mess this one up. Empty is empty regardless
        of which end you're looking at.
        """
        return not self._queue


def main() -> None:
    """
    Demonstration of our "stack" that's really just a deque pretending
    to solve an algorithmic challenge.

    Watch as it works perfectly because we're not actually solving
    the constrained problem - we're just using a data structure that
    already does what we need.
    """
    # Create our "stack" (it's really just a deque with renamed methods)
    stack = StackUsingQueueWrongEnd()

    print("Pushing values: 1, 2, 3")
    stack.push(1)  # deque: [1]
    stack.push(2)  # deque: [1, 2]
    stack.push(3)  # deque: [1, 2, 3]

    print("Popping values:")
    print(stack.pop())  # Returns 3 (from right end) - deque: [1, 2]
    print(stack.pop())  # Returns 2 (from right end) - deque: [1]
    print(stack.pop())  # Returns 1 (from right end) - deque: []

    # It works! But only because we're cheating by using both ends.
    # If we were forced to use only append() and popleft(), this
    # wouldn't work without significant refactoring.


if __name__ == "__main__":
    main()