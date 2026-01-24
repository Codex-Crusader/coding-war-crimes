"""
HELLO WORLD WITH THREAD POOL - USING A SLEDGEHAMMER TO CRACK A NUT

WARNING: This code uses a thread pool to print "Hello, world".

What this does:
Spins up a ThreadPoolExecutor with 10 worker threads to execute
a single function that returns a string, then waits for the result,
then prints it.

The correct way:
    print("Hello, world")

That's it. One line. No threads. No overhead. Done.

The cursed way:
    - Import concurrent.futures
    - Create ThreadPoolExecutor with 10 workers
    - Submit one task
    - Wait for result
    - Print result
    - Tear down thread pool

Six steps and massive overhead for what should be one line.

Why this is catastrophically bad:

1. MASSIVE OVERKILL FOR TRIVIAL TASK:
   Threading is for:
   - I/O-bound operations (network requests, file operations)
   - Running multiple tasks concurrently
   - Long-running background work

   NOT for:
   - Returning a string literal
   - Single print statement
   - This

2. THREAD POOL WITH 10 WORKERS FOR 1 TASK:
   max_workers=10 means:
   - Python creates 10 threads
   - 9 threads sit idle doing nothing
   - 1 thread returns "Hello, world"
   - All 10 threads are torn down

   We pay the cost of 10 threads to do 1 simple task.

3. SYNCHRONOUS WAIT ON ASYNC INFRASTRUCTURE:
   future.result() blocks until the thread finishes.

   Flow:
   1. Create thread pool (slow)
   2. Submit task to thread (overhead)
   3. Wait for thread to finish (blocking!)
   4. Get result
   5. Tear down pool (cleanup overhead)

   We built async infrastructure then made it synchronous!

4. THREAD CREATION OVERHEAD:
   Creating a thread:
   - Allocates stack space (typically 1-8 MB per thread)
   - OS kernel involvement
   - Context switching overhead
   - Thread management structures

   For 10 threads: ~10-80 MB of stack allocation
   To return a 13-character string.

5. NO PARALLELISM BENEFIT:
   Threading helps when you have:
   - Multiple independent tasks
   - I/O-bound work
   - Tasks that can run concurrently

   This has:
   - One task
   - Returns immediately
   - No I/O
   - No benefit from parallelism

6. CONTEXT SWITCHING WASTE:
   When thread executes:
   - OS switches context from main thread to worker
   - Worker returns "Hello, world"
   - OS switches context back to main thread

   Two context switches to return a string literal.
   Each context switch costs microseconds.

7. GLOBAL INTERPRETER LOCK (GIL):
   Python's GIL means:
   - Only one thread executes Python code at a time
   - Threading doesn't give CPU parallelism in Python
   - Only helps with I/O-bound work

   This function:
   - Is CPU-bound (returns string)
   - Doesn't do I/O
   - Gets NO benefit from threading

8. RESOURCE WASTE:
   Resources consumed:
   - 10 threads worth of stack space
   - Thread pool management overhead
   - Synchronization primitives
   - OS scheduler involvement

   Resources needed:
   - None. It's a string literal.

9. CLEANUP OVERHEAD:
   The context manager (with statement):
   - Ensures threads are cleaned up
   - Waits for all workers to finish
   - Tears down thread pool

   Cleanup costs more than the actual work!

10. MAKES SIMPLE CODE COMPLEX:
    One-line task becomes:
    - Import statement
    - Function definition
    - Thread pool creation
    - Task submission
    - Result waiting
    - Error handling (implicit in context manager)

Real-world consequences:

Issue 1 - Performance:
    Direct print: ~0.00001 seconds
    Thread pool version: ~0.001 seconds

    100x slower for "Hello, world"!

Issue 2 - Memory:
    Direct print: ~0 additional memory
    Thread pool: 10-80 MB of thread stacks

    For a 13-byte string.

Issue 3 - Resource Limits:
    System has limited threads (typically 1000s)
    Each unnecessary thread pool consumes resources
    Scale this pattern: quickly hit OS limits

Issue 4 - Production Bug:
    3 AM, server running slow
    Profiler shows: Thread pool creation everywhere
    Why? Someone thought threading makes things faster
    Reality: Made everything slower

    Rollback required, users angry

Issue 5 - Code Review:
    Reviewer: "Why are we using a thread pool?"
    Author: "To print Hello World"
    Reviewer: "..."
    PR rejected with prejudice

Performance comparison (printing 1,000 times):

Method 1 - Direct print:
    for _ in range(1000):
        print("Hello, world")

    Time: ~0.01 seconds
    Memory: Negligible

Method 2 - Thread pool per print:
    for _ in range(1000):
        with ThreadPoolExecutor(max_workers=10) as executor:
            future = executor.submit(lambda: "Hello, world")
            result = future.result()
            print(result)

    Time: ~5 seconds (500x slower!)
    Memory: Creating/destroying 10,000 threads
    Your OS: Crying

The overhead breakdown:

Thread pool creation: ~1ms
Task submission: ~0.01ms
Context switch to worker: ~0.001ms
Return string literal: ~0.000001ms (the actual work!)
Context switch back: ~0.001ms
Getting result: ~0.01ms
Thread pool cleanup: ~1ms

Total: ~2ms to do 0.000001ms of work
Overhead is 2,000,000x the actual work!

When threading IS appropriate:

1. I/O-bound tasks:
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_url, url) for url in urls]
        results = [f.result() for f in futures]

    Good: Concurrent network requests

2. Multiple independent tasks:
    with ThreadPoolExecutor() as executor:
        executor.submit(process_logs)
        executor.submit(send_emails)
        executor.submit(backup_database)

    Good: Running background jobs concurrently

3. Long-running operations:
    with ThreadPoolExecutor() as executor:
        future = executor.submit(expensive_computation)
        # Do other work while it runs
        result = future.result()

When threading is NOT appropriate:

1. Returning string literals (this file)
2. Simple calculations
3. Single print statements
4. CPU-bound work in Python (use multiprocessing instead)
5. Anything that finishes in microseconds

The correct approaches:

Option 1 (best):
    print("Hello, world")

Option 2 (if you must have a function):
    def hello():
        return "Hello, world"

    print(hello())

Option 3 (showing off unnecessarily):
    message = "Hello, world"
    print(message)

All better than spawning 10 threads.

Python's GIL (Global Interpreter Lock):

The GIL means:
- Only one thread executes Python bytecode at a time
- Threading in Python is for I/O concurrency, not CPU parallelism
- CPU-bound work needs multiprocessing, not threading

This code:
- Uses threading for CPU-bound work (returning string)
- Gets no parallelism benefit
- Only adds overhead

If you want actual parallelism for CPU work:
    from multiprocessing import Pool

    # But please don't use this for "Hello, world"

Threading vs Multiprocessing:

Threading (this file):
- Shares memory
- Good for I/O-bound work
- Limited by GIL
- Lower overhead than multiprocessing
- Still massive overkill for print statements

Multiprocessing:
- Separate processes
- Good for CPU-bound work
- No GIL limitation
- Higher overhead
- Even more overkill for print statements

Neither:
- Best for print statements
- Just print directly

Historical context:

Threading was added to Python to handle:
- Network servers
- GUI applications
- I/O-bound operations

Not to handle:
- "Hello, world"
- String literals
- This

Educational value:
- Shows how to use ThreadPoolExecutor
- Demonstrates massive overkill
- Illustrates overhead of thread creation
- Proves that parallelism ≠ faster for everything

Real-world analogy:
This is like:
- Hiring 10 people
- Giving them matching uniforms
- Assigning them shifts
- Setting up payroll
- Just to have one person say "Hello"
- Then firing everyone

Instead of: Just saying "Hello" yourself.

The resource comparison:

Creating 10 threads:
    - Stack allocation: ~10-80 MB
    - Thread structures: ~10 KB per thread
    - OS kernel objects: 10 handles
    - Context switching: Multiple times

Printing "Hello, world":
    - Memory: 13 bytes
    - CPU: One syscall
    - Time: Microseconds

The ratio is absurd.

Common misconceptions:

Myth: "Threading makes code faster"
Reality: Threading helps with I/O concurrency, adds overhead

Myth: "More threads = more speed"
Reality: GIL limits Python threads, overhead increases

Myth: "I should use threading for everything"
Reality: Use threading only when it actually helps

This code demonstrates all three myths.

Author's note: I could have typed print("Hello, world")
                That's literally all that was needed.
                I chose to create a thread pool with 10 workers instead.
                My computer's resource manager is filing a formal complaint.
                The OS scheduler is considering a restraining order.
                Even the threads are embarrassed.
"""

from concurrent.futures import ThreadPoolExecutor


def hello() -> str:
    """
    Return "Hello, world".

    This function is so simple it doesn't need to exist.
    It definitely doesn't need its own thread.
    And it CERTAINLY doesn't need a thread pool.

    Returns:
        str: A greeting that could have been a literal
    """
    return "Hello, world"


def hello_with_thread_pool() -> None:
    """
    Print Hello World using a thread pool.

    Creates a ThreadPoolExecutor with 10 worker threads
    to execute a single task that returns a string literal.

    Time Complexity: O(thread pool overhead)
    Space Complexity: O(10 thread stacks)
    Efficiency: O(absolutely not)

    Steps:
    1. Create thread pool with 10 workers (expensive)
    2. Submit one task (overhead)
    3. Wait for result (blocking)
    4. Get the string (finally!)
    5. Print it
    6. Clean up thread pool (more overhead)

    Could be: print("Hello, world")
    """
    # Spin up thread pool with 10 workers for one task
    # 9 workers will sit idle, wondering why they exist
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit the incredibly complex task of returning a string
        future = executor.submit(hello)

        # Wait for the thread to finish (blocking!)
        # We made it async then immediately made it sync
        result = future.result()

        # Finally, after all that ceremony, print the string
        print(result)

    # Thread pool cleanup happens here (context manager)
    # Tearing down 10 threads costs more than the print


def hello_correct() -> None:
    """
    The correct way to print Hello World.

    No threads. No overhead. Just works.
    """
    print("Hello, world")


# Example usage and performance comparison
# Example usage and performance comparison
if __name__ == "__main__":
    import time

    print("Hello World with Thread Pool - Performance Analysis")
    print("=" * 50)

    print("\nMethod 1: Thread pool with 10 workers")
    start = time.perf_counter()
    hello_with_thread_pool()
    thread_pool_time = time.perf_counter() - start
    print(f"Time: {thread_pool_time * 1000:.4f}ms")

    print("\nMethod 2: Direct print")
    start = time.perf_counter()
    hello_correct()
    direct_time = time.perf_counter() - start
    print(f"Time: {direct_time * 1000:.4f}ms")

    print("\n" + "=" * 50)
    print("Performance Comparison")
    print("=" * 50)

    if direct_time > 0:
        slowdown = thread_pool_time / direct_time
        print(f"Thread pool is {slowdown:.1f}x slower than direct print")

    print("\nResource usage:")
    print(f"  Thread pool: 10 threads, ~10-80 MB stack space")
    print(f"  Direct print: 0 threads, ~0 MB overhead")

    print("\n" + "=" * 50)
    print("Benchmark: 100 iterations")
    print("=" * 50)

    iterations = 100

    # Thread pool approach
    start = time.perf_counter()
    for _ in range(iterations):
        with ThreadPoolExecutor(max_workers=10) as pool:  # Changed from 'executor' to 'pool'
            task = pool.submit(hello)
            _ = task.result()
    thread_pool_total = time.perf_counter() - start

    # Direct approach
    start = time.perf_counter()
    for _ in range(iterations):
        _ = hello()
    direct_total = time.perf_counter() - start

    print(f"Thread pool (100x): {thread_pool_total:.4f}s")
    print(f"Direct (100x):      {direct_total:.6f}s")
    print(f"Slowdown factor:    {thread_pool_total / direct_total:.1f}x")

    print("\n" + "=" * 50)
    print("Conclusion:")
    print("=" * 50)
    print("Don't use thread pools for trivial tasks.")
    print("Threading overhead >> actual work")
    print("Just use: print('Hello, world')")
    print("=" * 50)