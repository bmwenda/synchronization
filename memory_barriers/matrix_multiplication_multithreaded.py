"""Matrix multiplation using multithreading and barriers
This introduces multithreading to the same problem from ./matrix_multiplication_single.py
The strategy is to find the result for each row in a separate thread
Note that since this is a CPU bound operation, python's Global Interprator Lock
blocks threads and the gain in using a multithreading approach is not dramatic
See shared_memory_in_processes/matrix_multiplication.py.py for multiprocessing solution
"""

import time
from random import randint
from threading import Barrier, Thread

N = 200 # reasonable number to observe run time
matrix_a = [[0] * N for a in range(N)]
matrix_b = [[0] * N for b in range(N)]
result = [[0] * N for r in range(N)]

work_start = Barrier(N + 1) # +1 accounts for parent thread
work_complete = Barrier(N + 1)

def initiliaze_matrices():
    for matrix in [matrix_a, matrix_b]:
        for row in range(N):
            for col in range(N):
                matrix[row][col] = randint(-10, 10)

def row_multiplication(row):
    while True:
        work_start.wait()
        for col in range(N):
            for i in range(N):
                result[row][col] += matrix_a[row][i] * matrix_b[i][col]
        work_complete.wait() # each thread waits at second barrier after completion

def create_threads():
    """Create N threads
    Threads have a small memory footprint which makes this possible
    """
    for row in range(N):
        Thread(target=row_multiplication, args=(row,)).start()

if __name__ == "__main__":
    create_threads() # create N threads for each row and have them wait at first barrier
    start_time = time.time()
    for i in range(10):
        initiliaze_matrices()
        result = [[0] * N for r in range(N)]
        work_start.wait() # main thread calls wait and this unlocks the other threads to do calculation
        work_complete.wait() # main thread waits at second barrier. When the other N threads reach here, lock is released and next iteration can run
    end_time = time.time()
    print("Finished in", end_time - start_time)
