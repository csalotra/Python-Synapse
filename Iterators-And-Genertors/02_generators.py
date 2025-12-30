"""
GENERATORS

Generators automatically implement the iterator protocol, instead of requiring
manual implementation of __iter__ and __next__ methods.

Key concepts:

- Generator is a special type of function that returns an iterator object. Unlike a regular function that computes a result and returns it all at once, a generator produces a sequence of values lazily—meaning it calculates each item only when you actually ask for it.

- Yield statement: Instead of using return to send a value back, a generator uses yield. When the generator function is called, it doesn't execute the function body immediately. Instead, it returns a generator object. Each time next() is called on this object, the function runs until it hits a yield statement, which produces a value and pauses the function's state. The next time next() is called, execution resumes right after the last yield.

"""

#### Manual vs Generator Approach ####

print("=== Generator Function (Easiest way to create an iterator) ===\n")

# Manual addition of '__iter__' and '__next__' methods in the class
class Count:
  def __init__(self, start, end):
    self.current = start
    self.end = end

  def __iter__(self):
    return self
  
  def __next__(self):
    if self.current > self.end:
      raise StopIteration
    else:
      self.current += 1
      return self.current -1
    
# Create instance
counter = Count(1, 10)

print("Iterator ", counter) # Custom interator object

print("Looping over custom iterable (uses for-loop):")
for num in counter:
  print(num)

print("-> End of custom class iteration")



#### USING GENERATOR APPROACH ####

def count_generator(start, end):
    """
    Generator function -> returns a generator iterator.
    Each 'yield' produces a value and pauses execution, preserving state.
    Easy and cleaner than writing a full class for simple sequences.
    """
    current = start
    while current < end:
        yield current # Produces next value and pauses
        current += 1
    
# Create generator iterator
counter_gen = count_generator(1, 11)

print("Generator object:")
print(counter_gen)  # Output: <generator object...>
print()

print("Looping over generator:")
for num in counter_gen:
    print(num)
print("-> End of generator iteration")

# Generators are also one-time use, if looped over again on the same generator, it will print nothing

