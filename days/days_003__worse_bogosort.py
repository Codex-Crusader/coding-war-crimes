"""
CHAOS SORT v2.0 - NOW WITH FAKE PROGRESS TRACKING

IMPROVEMENTS OVER v1.0:
- Progress bar (lies to you)
- More chaos operations (reverse, shuffle segments)
- Reflection tracking (useless statistics)
- Artificial delays (so you can watch it fail in real-time)
- Even less deterministic behavior

New features:
- REVERSE: Flips entire list (often makes things worse)
- SHUFFLE_SEGMENT: Destroys a random portion of your data
- PROGRESS BAR: Goes backwards sometimes, hits 100% before sorting completes
- REFLECTIONS: Tracks how many times elements were "involved" in operations
  (as if this information helps anyone)

Time Complexity: O(????????)
Space Complexity: O(n) for the reflection dict
Sanity Loss: O(attempts * sleep_duration)

The progress bar is intentionally wrong:
- Can go backwards
- Changes randomly regardless of actual progress
- Will hit 100% while list is still unsorted
- Provides false hope

Why the sleep(0.05)?
So you can watch your CPU waste cycles in real-time.
It's not a bug, it's a feature for maximum psychological damage.

Run this on [5, 4, 3, 2, 1] if you hate yourself.
"""

import random
import time


def is_sorted(data):
    for i in range(len(data) - 1):
        if data[i] > data[i + 1]:
            return False
    return True


def print_progress(progress):
    bar_length = 30
    filled = int(bar_length * progress)
    empty = bar_length - filled
    bar = "[" + "#" * filled + "-" * empty + "]"
    print("\rProgress:", bar, f"{int(progress * 100)}%", end="", flush=True)


def chaos_sort(data):
    attempts = 0
    # track how many times each element reflects on its mistakes
    reflections = {item: 0 for item in data}
    progress = 0.0

    while not is_sorted(data):
        attempts += 1
        action = random.choice([
            "swap",
            "replace",
            "reverse",
            "shuffle_segment",
            "nothing"
        ])

        if action == "swap" and len(data) > 1:
            i = random.randint(0, len(data) - 1)
            j = random.randint(0, len(data) - 1)
            data[i], data[j] = data[j], data[i]
            reflections[data[i]] += 1
            reflections[data[j]] += 1

        elif action == "replace":
            i = random.randint(0, len(data) - 1)
            old_value = data[i]
            data[i] = random.choice(data)
            reflections[old_value] += 1

        elif action == "reverse":
            data.reverse()
            for element in data:
                reflections[element] += 1

        elif action == "shuffle_segment" and len(data) > 2:
            start = random.randint(0, len(data) - 2)
            end = random.randint(start + 1, len(data) - 1)
            segment = data[start:end + 1]
            random.shuffle(segment)
            data[start:end + 1] = segment
            for seg_item in segment:
                reflections[seg_item] += 1

        # optimization: sometimes doing nothing is the fastest operation
        # especially when the algorithm has no idea what it's doing
        elif action == "nothing":
            pass

        # progress calculation (wildly inaccurate on purpose)
        progress_change = random.uniform(-0.1, 0.15)
        progress = min(1.0, max(0.0, progress + progress_change))
        print_progress(progress)
        time.sleep(0.05)

    print()  # move to next line after progress bar
    return data, attempts, reflections


if __name__ == "__main__":
    numbers = [3, 1, 4, 2]
    sorted_numbers, tries, reflection_log = chaos_sort(numbers)
    print("Sorted list:", sorted_numbers)
    print("Attempts:", tries)
    print("Reflections per element:")
    for num, count in reflection_log.items():
        print(f"  {num}: {count}")