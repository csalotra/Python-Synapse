"""
GENERATORS

This module explores the lifecycle of generators, from lazy evaluation 
to bidirectional communication and delegation protocols

Generators automatically implement the iterator protocol, instead of requiring
manual implementation of __iter__ and __next__ methods.

Key concepts:

- A generator is a lazy iterator factory. Unlike standard functions that return a full result set at once, generators produce values on-demand, maintaining a near-zero memory footprint regardless of dataset size.

- yield is a "pause-and-resume" button. Calling the function returns a generator object without executing code. Each next() call runs the function until it hits a yield, emits the value, and freezes the entire state (variables and instruction pointer) until the next request.

"""

import time
import tracemalloc # For memory tracking


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

# Example of generator expression (similar to list comprehensions but for generators)

count_gen = (x for x in range(1, 6))

print(count_gen)

# Convert generator object to list to see all values at once
print(list(count_gen))


#### COMPARISON OF PERFORMANCE OF LISTS VS GENERATORS ####

# 1. Standard function to return a list of squares
def square_list(n):
    result = []
    for i in range(n):
      result.append(i*i)
    return result

# 2. Genrator function
def square_gen(n):
  for i in range (n):
    yield i*i

# 3. Performance profiling function
def profile_performance(n):
  print(f"---- Profiling for {n:,} items ---")

  # Profiling for list
  tracemalloc.start() # start memory tracking
  start_time = time.time()

  squares_list = square_list(n)
  sum_squares_list = sum(squares_list) # Force evaluation of all items

  end_time = time.time()
  current, peak = tracemalloc.get_traced_memory()
  tracemalloc.stop()  
  print(f"List - Time taken: {end_time - start_time:.4f} seconds")
  print(f"List - Current memory usage: {current / 10**6:.4f} MB; Peak: {peak / 10**6:.4f} MB")

  # Profiling for generator
  tracemalloc.start() # start memory tracking
  start_time = time.time()

  squares_gen = square_gen(n)
  sum_squares_gen = sum(squares_gen) # Force evaluation of all items

  end_time = time.time()
  current, peak = tracemalloc.get_traced_memory()
  tracemalloc.stop()  
  print(f"Generator - Time taken: {end_time - start_time:.4f} seconds")
  print(f"Generator - Current memory usage: {current / 10**6:.4f} MB; Peak: {peak / 10**6:.4f} MB")



# Calling performance profiling function with 10 million numbers
# profile_performance(10000000)  #-> uncomment to test the performance

# Code to see the functioning of the generatoe
def loud_generator():
    print("--- Generator Started ---")
    yield 1
    yield 2
    print("--- Generator Finished ---")

# 1. Just calling the function
print("Calling the function...")
g = loud_generator() 
# (Note: Nothing prints from inside the generator)

# 2. Consuming it
print("Now consuming with sum()...")
print(next(g)) # This will trigger the first yield
print(next(g)) # This will trigger the second yield

# Trying to get next value after generator is exhausted
try:
    print(next(g)) # This will trigger the "Finished" print, then raise an error
except StopIteration:
    print("Iteration stopped!")



#### .send() IN GENERATORS ####

"""
The .send() method is a built-in generator method that resumes the execution of a generator and "sends" a value into it, which becomes the result of the current yield expression.

How it works (The Mechanics)
----------------------------

It transforms a one-way data producer into a two-way coroutine, allowing the generator to receive external data and update its internal state dynamically while it is paused.

The Pause: When a generator reaches a yield statement, it emits a value and pauses.

The Injection: When .send(value) is called from the outside, the generator "wakes up."

The Assignment: The value passed into .send() is "injected" exactly where the yield was. It is assigned to whatever variable is on the left side of the yield expression (e.g., x = yield output).

The Resume: The generator continues running until it hits the next yield statement, at which point it pauses again and returns a new value.


=> We cannot send a non-None value to a generator that has just been created but not yet started.

Reason: The generator hasn't reached its first yield yet, so there is no "receiver" waiting for the data.

Requirement: first call next(gen) or gen.send(None) to "prime" it (advance it to the first yield)
"""

def chef_bot():
    print("Chef is in the kitchen!")
    while True:
        ingredient = yield "Waiting for ingredient..."
        print(f"Chef is cooking with: {ingredient}")

# --- Using it ---
c = chef_bot()

# 1. We MUST "Prime" the generator first
# This gets the chef into the kitchen and waiting at the first 'yield'
print(next(c)) 
print(next(c)) 

#2. Now we can talk to him
c.send("Tomato")
c.send("Cheese")


#### yield from ####

# yield from delegates control to other iterator or generator

print("======= yield from ======\n")
def sub():
    yield 1
    yield 2

def main():
    yield from sub()
    yield 3


yield_frm = main()
print(yield_frm)

for i in yield_frm:
   print(i)


# yield from with normal iterables
print("======= yield from with normal iterables ======\n")
def gen_yf():
    yield from [10, 20, 30] #It works with any iterable, not just generators.

# The above function is same as 

def without_gen_yf():
   for x in [10, 20, 30]:
      yield x


print(gen_yf())
print(without_gen_yf())


# Sending values through yield from
print("======= Sending values through yield from ======\n")
def sub_task():
   while True:
      value = yield
      print("Sub recieved: ", value)

def main_task():
   yield from sub_task()

# --- Using it ---
m = main_task()

next(m) #start
m.send("Hello")

# Exception handling using yield from
print("======= Exception handling using yield from ======\n")
def sub_eh():
    try:
        yield 1
        yield 2
    except ValueError:
        yield "Handled error"

def main_eh():
    yield from sub_eh()


# --- Using it ---
eh = main_eh()

print(next(eh)) #start
print(eh.throw(ValueError))


# Returning values from generators
print("======= Returning values from generators ======\n")
def retval():
    yield 1
    yield 2
    return "Done"

def main_retval():
    result = yield from retval()
    print(result)

# --- Using it ---
rv = main_retval()

for value in rv:
    print(value)


# .close() and .throw() in Python generators

"""
When we call gen.close(), Python injects a special exception called GeneratorExit at the exact line where the generator is currently paused.

The Mechanic: This forces the generator to trigger any finally blocks, ensuring you don't leave files or database connections open.

The Rule: A generator must stop after a GeneratorExit. If it tries to yield another value after being closed, Python will raise a RuntimeError.
"""
print("======= .close() in generators ======\n")
def database_reader():
    try:
        print("Connected to DB")
        yield "Row 1"
        yield "Row 2"
    finally:
        print("Disconnected safely") # Runs even if we close early

reader = database_reader()
print(next(reader))
# print(next(reader))
reader.close() # Forces the 'finally' block to run immediately


# .throw() — inject an exception into a generator

# .throw() raises an exception at the current yield point inside the generator.

def thrower():
    try:
        yield 1
        yield 2
    except ValueError as e:
        print(e)
        yield "ValueError handled"

t = thrower()
print(next(t))
print(t.throw(ValueError("Bad data")))













