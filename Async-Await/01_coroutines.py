"""
COROUTINES

Coroutines in Python are specialized functions that allow execution to be paused and resumed, enabling cooperative multitasking and asynchronous programming. They generalize subroutines by supporting multiple entry/exit points, making them ideal for handling I/O-bound operations without blocking the main thread.

"""

#### CLASSIC COROUTINES ####

"""
Generators primarily produce data, while these coroutines can both produce and consume it. 
"""

def grep(pattern):
  print(f"Searching for the pattern : {pattern}")
  while True:
    value = yield
    if pattern in value:
      print(value)


# --- Using it ---
searcher = grep("coroutine")
next(searcher) # Prime the coroutine
searcher.send("I love coding")
searcher.send("I love coroutine") #Outputs the matching line
searcher.close()


#### Modern Coroutines: Native Coroutines with async/await ####

"""
native coroutines use async def to define them and await to pause execution while waiting for another awaitable (like another coroutine).
Calling an async def function returns a coroutine object, which must be scheduled with an event loop (typically via asyncio) to run.

"""

import asyncio
import time

# 1. Defining a Native Coroutine
async def network_request(name, delay):
    """
    The 'async' keyword flags this as a Native Coroutine.
    It returns a coroutine object without executing the body.
    """
    print(f"  [Task {name}] Starting (will take {delay}s)...")
    
    # The 'await' keyword is a "Yield to the Loop" signal.
    # It pauses this task and lets the Event Loop run other things.
    await asyncio.sleep(delay) 
    
    print(f"  [Task {name}] Finished!")
    return f"Data from {name}"

# 2. Orchestrating Concurrency
async def main():
    """
    This is the entry point of the asynchronous program.
    """
    start_time = time.time()
    print("--- Execution Start ---")

    # Creating Coroutine Objects (They haven't started running yet!)
    task1 = network_request("API_A", 3)
    task2 = network_request("API_B", 2)
    task3 = network_request("Database", 1)

    # MECHANICS: asyncio.gather
    # It schedules all coroutines on the event loop simultaneously.
    print("Scheduling tasks concurrently...")
    results = await asyncio.gather(task1, task2, task3)

    end_time = time.time()
    print(f"--- Executive Finish ---")
    print(f"Results: {results}")
    print(f"Total time elapsed: {end_time - start_time:.2f} seconds")

# The Event Loop: The 'engine' that drives the coroutines.
asyncio.run(main())


# Without async /await

def blocking_task(name, delay):
    """
    A standard function that executes immediately upon being called.
    The stack frame is created, used, and destroyed in one continuous block.
    """
    print(f"  [Stack {name}] Thread Captured. Blocking for {delay}s...")

    # time.sleep() does NOT yield. It tells the OS to put the entire 
    # process to sleep. No other code in this script can run.
    time.sleep(delay) 
    
    print(f"  [Stack {name}] Task Complete. Releasing Thread.")
    return f"Result_{name}"

def main_sequencer():
    """
    Executes tasks in a strict linear order.
    """
    start_time = time.time()
    print("--- Synchronous Tasks Started ---")

    # Each line must finish completely before the next line begins.
    # There is no "Scheduling" here, only "Ordering".
    
    res1 = blocking_task("Task_1", 3)
    res2 = blocking_task("Task_2", 2)
    res3 = blocking_task("Task_3", 1)

    results = [res1, res2, res3]

    end_time = time.time()
    print("--- Synchronous Tasks Stop ---")
    print(f"Final States: {results}")
    
    # Total time
    print(f"Execution Time for synchronous tasks: {end_time - start_time:.2f}s")


main_sequencer()