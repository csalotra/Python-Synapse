"""
ITERABLES & ITERATORS IN PYTHON

Key Concepts:

1. Iterable:
   - An object that can be looped over (e.g., list, tuple, string, dict, set, range).
   - Must implement the __iter__() method, which returns an iterator object.
   - Can also optionally implement __getitem__() for sequence-style access.
   - We can use it directly in a for loop or with functions like list(), sum(), etc.

2. Iterator:
   - An object that keeps track of its position in a sequence and produces the next value when asked.
   - Must implement BOTH:
     - __iter__() -> returns itself (so it's also iterable)
     - __next__() -> returns the next item or raises StopIteration when done
   - Represents a stream of data — we can only go forward, not reset or go backward.

Analogy:
   - Iterable = A music album (CD/playlist) — it contains songs in order.
   - Iterator = The CD player in play mode — it knows the current song and can play the next one.

Important:
   - Once an iterator is exhausted (StopIteration raised), it stays exhausted.
   - Most built-in iterables (like lists) return a fresh iterator each time you call iter().
   - Generators are a simple way to create iterators using 'yield'.

Python's for loop works like this under the hood:
    iterator = iter(iterable)          # Get iterator
    while True:
        try:
            item = next(iterator)      # Get next item
        except StopIteration:
            break                      # Done
        # do something with item
"""

print("=== PART 1: Built-in List as Iterable & Iterator ===\n")

nums = [1, 2, 3]

# Check what methods are available on a list
print("Methods/attributes of a list (nums):")
print([method for method in dir(nums) if "__iter__" in method])  # Check __iter__ method
print() # extra line for readability

# Lists are iterable because they have __iter__()
# Calling iter(nums) returns a list_iterator object
i_nums = iter(nums)

print("Iterator object created from list:")
print(i_nums)  # Example output: <list_iterator object ...>
print()

# Check methods on the iterator
print("Key special methods on the iterator:")
print([method for method in dir(i_nums) if method in {"__iter__", "__next__"}])
print()  # Both __iter__ and __next__ are present -> it's a proper iterator

# Manual iteration using next()
print("Manual iteration with next():")
print(next(i_nums))  # 1
print(next(i_nums))  # 2
print(next(i_nums))  # 3
# print(next(i_nums))  # Would raise StopIteration -> commented out

print("\nSafer way to manually exhaust an iterator:")
# Reset iterator because the previous one is exhausted
i_nums = iter(nums)

while True:
    try:
        item = next(i_nums)
        print(item)
    except StopIteration:
        print("-> Iterator exhausted!")
        break

print("\n" + "="*80)

print("=== PART 2: Custom Iterable Class (Iterator is the same object) ===\n")

class SquareRange:
    """
    A custom iterable that produces squares of integers from start up to (but not including) end.
    
    This class is both the iterable and the iterator (common pattern for simple cases).
    - __iter__ returns self -> makes the object iterable
    - __next__ produces the next square and updates internal state
    """
    def __init__(self, start, end):
        self.start = start      # Remember original start (useful for repr)
        self.end = end
        self.value = start      # Current value (state of iterator)

    def __iter__(self):
        """Required for iterable protocol. Returns the iterator object (itself)."""
        return self

    def __next__(self):
        """Produces next square. Raises StopIteration when done."""
        if self.value >= self.end:
            raise StopIteration
        current = self.value
        self.value += 1
        return current ** 2

    def __repr__(self):
        return f"SquareRange({self.start}, {self.end})"


# Create instance
squares_class = SquareRange(1, 11)

print("Custom iterable object:")
print(squares_class)
print()

print("Looping over custom iterable (uses for-loop):")
for num in squares_class:
    print(num)
print("-> End of custom class iteration")

# Note: After the loop above, the iterator is exhausted!
# If you try to loop again, you'll get nothing:
print("\nTrying to loop again on the same object (exhausted iterator):")
for num in squares_class:
    print(num)  # Nothing printed -> iterator remembers its position
print("-> Nothing printed because iterator is exhausted")

print("\n" + "="*80)

print("=== PART 3: Generator Function (Easiest way to create an iterator) ===\n")

def square_generator(start, end):
    """
    Generator function -> returns a generator iterator.
    Each 'yield' produces a value and pauses execution, preserving state.
    Much cleaner than writing a full class for simple sequences.
    """
    current = start
    while current < end:
        yield current ** 2   # Produces next value and pauses
        current += 1

# Create generator iterator
squares_gen = square_generator(1, 11)

print("Generator object:")
print(squares_gen)  # Output: <generator object...>
print()

print("Looping over generator:")
for num in squares_gen:
    print(num)
print("-> End of generator iteration")

# Generators are also one-time use
print("\nTrying to loop again on the same generator:")
for num in squares_gen:
    print(num)  # Nothing printed
print("-> Generator is exhausted after first use")

print("\n" + "="*80)

print("=== Summary ===\n")
print("-> Lists, tuples, strings, dicts, sets, range() -> Built-in iterables")
print("-> iter(obj) -> gets an iterator from an iterable")
print("-> next(it) -> gets next item, raises StopIteration at end")
print("-> for loop automatically handles StopIteration")
print("-> Custom iterables: implement __iter__()")
print("-> Custom iterators: implement __iter__() and __next__()")
print("-> Generators (with yield) -> simplest way to create iterators")
print("-> Iterators keep state and are usually one-time consumable")

print("\nImp: To re-iterate, call iter() again on the original iterable")
print("   Example: list(square_generator(1, 11)) -> [1, 4, 9, ..., 100]")