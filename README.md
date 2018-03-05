The repository contains a code that was presented on
[Kiwi.com](https://pythonvikend.kiwi.com/) Python weekend. It contains a simple
code to demonstrate performance differences between
[`asyncio`](https://docs.python.org/3/library/asyncio-task.html) and
[`ThreadPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor).
For the purpose of the testing I created a simple code that scrape bus ticket
prices for a date-range from RegioJet website.

#  Results

The script scrapes prices for 100 days in-front. Memory usage was measured by
[`memory_profiler`](https://pypi.python.org/pypi/memory_profiler). For the sake
of simplicity the script just loads HTML response from a server and looks for
ticket prices. There is no further processing of the scraped data.

## Synchronous

For a reference, I executed a single threaded version of the script. The memory
usage is pretty stable during the entire execution of the script. The obvious
drawback is an execution time. Without any parallelism the script took over 80
seconds.

![Synchronous](reports/sync.png?raw=true "Synchronous")

## ThreadPoolExecutor

For a long time, threading was the only way how to speed up an IO heavy
application. Threads come up with a drawback of a higher memory usage, but with
a great advantage of speed. Exection time is ~17sec. Compared to 80 seconds for
synchronous execution, this a huge difference.

![ThreadPoolExecutor](reports/thread.png?raw=true "ThreadPoolExecutor") Example
of Python `asyncio` module and difference between thread and sync approach.

## Gevent

Gevent brings coroutines to older versions of Python. It's a similar concept to
`asyncio`.

![Asyncio exection](reports/async.png?raw=true "Asyncio")

## Asyncio

Since Python 3.5, there is a preferred way how to parallelise IO operations.
With coroutines, the script takes the advantage of a parallel execution but
requires less memory then multithreading.

![Asyncio exection](reports/async.png?raw=true "Asyncio")

# Try it yourself

Use Python 3.5 version or higher and install dependencies:

```
bash pip install -r requirements.txt 
```

Then just execute each script with
the memory profiling tool.

```
bash mprof run student_agency_sync.py
```

After each run, the memory usage graphs can be generated with a following
command:

```bash mprof plot ```
