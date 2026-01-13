import concurrent.futures
import threading
import time 

start = time.perf_counter()

def do_something(seconds):
  print(f'Sleeping {seconds} second....')
  time.sleep(seconds)
  print('Done Sleeping...')

def do_wait(seconds):
  print(f'Waiting {seconds} second....')
  time.sleep(seconds)
  return f'Done Waiting {seconds}...'

# do_something()
# do_something()

### Using Threading to run tasks concurrently
# t1 = threading.Thread(target=do_something)
# t2 = threading.Thread(target=do_something)

# t1.start()
# t2.start()

# ### Join methods are used to wait for threads to complete
# t1.join()
# t2.join()

### For loop to create multiple threads
# We can not use join in the same loop as starting threads because it will wait for each thread to complete before starting the next one
# threads = []
# for _ in range(10):
#   t = threading.Thread(target=do_something, args=[1.5])
#   threads.append(t)
#   t.start()
#   threads.append(t)

# for thread in threads:
#   thread.join()

"""
executor.submit() returns a Future → a promise of a result that will be ready later.
You control when and how to wait, cancel, or inspect it.

executor.map() returns actual results (as an iterator).
Python waits for each task and gives you the values directly.

Think of it like this:

submit() → gives you a job handle (Future)

map() → gives you the job output
"""

# Using ThreadPoolExecutor to run tasks concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
  seconds_list = [1, 3, 6, 3, 2, 2, 8]
  results = [executor.submit(do_wait, sec) for sec in seconds_list ] #submit method returns a Future object
  for f in concurrent.futures.as_completed(results):
    print(f.result())

"""
Results are returned in the same order as input.

So if:
Task 1 takes 10s
Task 2 takes 1s
Even if task 2 finishes first, map() will wait 10s to yield result #1.
"""

with concurrent.futures.ThreadPoolExecutor() as executor:
  seconds_list = [9, 7, 4]
  results = executor.map(do_wait, seconds_list)  #map method returns the results
  for f in results:
    print(f)


finish = time.perf_counter()

print(f'Finished in {round(finish -start, 2)} second(s)')