from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from typing import Callable

import math
import random
import time

operations = 0


# TODO: implement the best ones in C
# TODO: add if k == 1 logic
# TODO: add cache check as a separate op than raw hit

def top_down(n, k):
    td_cache = defaultdict(dict)

    def go(n, k):
        global operations
        if (hit := td_cache[n].get(k)) is not None:
            return hit
        operations += 1
        if n <= 0 or k <= 0 or n < k:
            return 0
        if n == k:
            return 1
        td_cache[n][k] = go(n - 1, k - 1) + go(n - k, k)
        return td_cache[n][k]

    return go(n, k)

def top_down_stack(n, k):
    global operations
    td_cache = defaultdict(dict)

    stack = [(n, k)]

    while stack:
        n, k = stack.pop()
        if n <= 0 or k <= 0 or n < k:
            operations += 1
            td_cache[n][k] = 0
        elif n == k or k == 1:
            operations += 1
            td_cache[n][k] = 1
        else:
            repush = False
            stack.append((n, k))
            if k < n and (hit1 := td_cache[n - k].get(k)) is None:
                repush = True
                stack.append((n - k, k))
            if n > 1 and k > 1 and (hit2 := td_cache[n - 1].get(k - 1)) is None:
                repush = True
                stack.append((n - 1, k - 1))
            if repush:
                continue
            stack.pop()
            operations += 1
            td_cache[n][k] = hit1 + hit2

    return td_cache[n][k]

def top_down_stack_with_context(n, k):
    global operations
    td_cache = defaultdict(dict)

    INQUISITIVE = 0
    COLLAPSE_FRAME = 1

    stack = [(n, k, 0)]

    while stack:
        n, k, context  = stack.pop()
        if n <= 0 or k <= 0 or n < k:
            operations += 1
            td_cache[n][k] = 0
        elif n == k or k == 1:
            operations += 1
            td_cache[n][k] = 1
        else:
            if context == INQUISITIVE:
                left_trap = False
                right_trap = False

                if (left_hit := td_cache[n - 1].get(k - 1)) is None:
                    left_trap = True
                if (right_hit := td_cache[n - k].get(k)) is None:
                    right_trap = True

                if not left_trap and not right_trap:
                    operations += 1
                    td_cache[n][k] = left_hit + right_hit

                else:
                    stack.append((n, k, COLLAPSE_FRAME))
                    if left_trap:
                        stack.append((n - 1, k - 1, INQUISITIVE))
                    if right_trap:
                        stack.append((n - k, k, INQUISITIVE))
            else:
                operations += 1
                td_cache[n][k] = td_cache[n - 1].get(k - 1) + td_cache[n - k].get(k)

    return td_cache[n][k]

def top_down_array(n, k):
    td_cache = [] * (n + 1)
    for _ in range(n + 1):
        td_cache.append([-1] * (k + 1))

    def go(n, k):
        global operations
        if (hit := td_cache[n][k]) != -1:
            return hit
        operations += 1
        if n <= 0 or k <= 0 or n < k:
            return 0
        if n == k:
            return 1
        td_cache[n][k] = go(n - 1, k - 1) + go(n - k, k)
        return td_cache[n][k]

    return go(n, k)

def top_down_array_1d(n, k):
    rows = n + 1
    cols = n + 1

    td_cache = [-1] * ((rows + 1) * (cols + 1))

    def go(n, k):
        global operations
        if (hit := td_cache[(n + 1) * cols + k + 1]) != -1:
            return hit
        operations += 1
        if n <= 0 or k <= 0 or n < k:
            return 0
        if n == k:
            return 1
        td_cache[(n + 1) * cols + k + 1] = go(n - 1, k - 1) + go(n - k, k)
        return td_cache[(n + 1) * cols + k + 1]

    return go(n, k)

def top_down_array_stack(n, k):
    global operations
    td_cache = [] * (n + 1)
    for _ in range(n + 1):
        td_cache.append([-1] * (k + 1))

    stack = [(n, k)]

    while stack:
        n, k = stack.pop()
        if n <= 0 or k <= 0 or n < k:
            operations += 1
            td_cache[n][k] = 0
        elif n == k or k == 1:
            operations += 1
            td_cache[n][k] = 1
        else:
            repush = False
            stack.append((n, k))
            if k < n and (hit1 := td_cache[n - k][k]) == -1:
                repush = True
                stack.append((n - k, k))
            if n > 1 and k > 1 and (hit2 := td_cache[n - 1][k - 1]) == -1:
                repush = True
                stack.append((n - 1, k - 1))
            if repush:
                continue
            stack.pop()
            operations += 1
            td_cache[n][k] = hit1 + hit2

    return td_cache[n][k]

def top_down_array_stack_1d(n, k):
    global operations
    td_cache = [-1] * (n * k)

    rows = n
    cols = k

    stack = [(n, k)]

    while stack:
        n, k = stack.pop()
        if n <= 0 or k <= 0 or n < k:
            operations += 1
            td_cache[(n - 1) * cols + k - 1] = 0
        elif n == k or k == 1:
            operations += 1
            td_cache[(n - 1) * cols + k - 1] = 1
        else:
            repush = False
            stack.append((n, k))
            if k < n and (hit1 := td_cache[(n - k - 1) * cols + k - 1]) == -1:
                repush = True
                stack.append((n - k, k))
            if n > 1 and k > 1 and (hit2 := td_cache[(n - 1 - 1) * cols + k - 1 - 1]) == -1:
                repush = True
                stack.append((n - 1, k - 1))
            if repush:
                continue
            stack.pop()
            operations += 1
            td_cache[(n - 1) * cols + k - 1] = hit1 + hit2

    return td_cache[(n - 1) * cols + k - 1]

def bottom_up(n, k):
    global operations

    table = []
    for i in range(n + 1):
        table.append([0] * (k + 1))

    for i in range(1, n + 1):
        table[i][1] = 1

    for i in range(1, k + 1):
        table[i][i] = 1

    for i in range(3, n + 1):
        for j in range(2, k + 1):
            operations += 1
            table[i][j] = table[i - 1][j - 1] + table[i - j][j]

    return table[n][k]

def combinatorial(n, k):
    global operations
    target = n - k

    coefficients = {0: 1}
    for iteration in range(1, k + 1):
        result = defaultdict(int)
        for weight in coefficients.keys():
            if weight > target:
                break
            for term in range(n // iteration):
                if term * iteration + weight > target:
                    break
                operations += 1
                result[weight + iteration * term] += coefficients[weight]
        coefficients = result
    return coefficients[target]

def combinatorial_array(n, k):
    global operations
    target = n - k

    coefficients = [0] * n
    coefficients[0] = 1
    for iteration in range(1, k + 1):
        result = [0] * n
        for weight in range(len(coefficients)):
            if weight > target:
                break
            for term in range(n // iteration):
                if term * iteration + weight > target:
                    break
                operations += 1
                result[weight + iteration * term] += coefficients[weight]
        coefficients = result
    return coefficients[target]

from numpy import convolve

def numpy_convolution(n, k):
    global operations
    target = n - k

    coefficients = [0] * n
    coefficients[0] = 1

    for iteration in range(1, k + 1):
        terms = []
        for term_factor in range(n):
            terms.append(not int(term_factor % iteration))
        coefficients = convolve(coefficients, terms)
        operations += (len(coefficients) * len(terms))
    return coefficients[target]

from scipy import signal

def fft(n, k):
    global operations
    target = n - k

    coefficients = [0] * n
    coefficients[0] = 1

    for iteration in range(1, k + 1):
        terms = []
        for term_factor in range(n):
            terms.append(not int(term_factor % iteration))
        coefficients = signal.fftconvolve(coefficients, terms)
        operations += len(terms) * int(math.log(len(terms), 2))
    return int(coefficients[target])

tests = {
    (8, 4): 5,
    (6, 3): 3,
    (7, 3): 4,
    (5, 2): 2,
    (6, 2): 3,
    (7, 2): 3,
    (8, 2): 4,
    (9, 2): 4,
    (10, 3): 8,
    (8, 4): 5,
    (12, 4): 15,
    (11, 3): 10,
    (4, 2): 2,
    (9, 3): 7,
    (9, 4): 6,
    (20, 1): 1,
    (70, 70): 1,
    (25, 8): 230,
    (70, 15): 284054,
    (99, 42): 613646,
    (120, 20): 97132873,
    (250, 130): 1844349560,
}

def test_runner(name, p, iterations):
    global operations
    operations = 0
    start = time.time()
    for _ in range(iterations):
        for test, expected in tests.items():
            n, k = test
            actual = p(n, k)
#            print(f"{name}: test={test} expected={expected} actual={actual}")
            assert actual == expected
    end = time.time()
    return operations, end - start

@dataclass
class Trial:
    name: str
    runner: Callable[[int, int], int]
    time: int = 0
    operations: int = 0

def run_trials(trials, iterations):
    call_counts = defaultdict(int)
    times = defaultdict(float)

    for _ in range(iterations):
        random.shuffle(trials)
        for trial in trials:
            call_count, time = test_runner(trial.name, trial.runner, 1)
            call_counts[trial.name] += call_count
            times[trial.name] += time

    for trial in trials:
        trial.time = times[trial.name]
        trial.operations = call_counts[trial.name]
        trial.op_speed = call_counts[trial.name] / times[trial.name]

def generate_report(trials, sort_lambda):
    for trial in sorted(trials, key=sort_lambda):
        print(f"  {trial.name.ljust(25)} done in {trial.time:.3f}s using {trial.operations} operations (ops/s is {trial.op_speed})")

trials = [
    Trial(name="BU dp", runner=bottom_up),

    Trial(name="TD ddict", runner=top_down),
    Trial(name="TD ddict stack", runner=top_down_stack),
    Trial(name="TD array", runner=top_down_array),
    Trial(name="TD array 1D", runner=top_down_array_1d),
    Trial(name="TD array stack", runner=top_down_array_stack),
    Trial(name="TD array stack 1D", runner=top_down_array_stack_1d),
    Trial(name="TD ddict stack context", runner=top_down_stack_with_context),

    Trial(name="generator math", runner=combinatorial),
    Trial(name="generator math array", runner=combinatorial_array),
    Trial(name="numpy_convolution", runner=numpy_convolution),
#    Trial(name="fast fourier transform", runner=fft),
]

run_trials(trials, 10)

metrics = {
    "name": lambda trial: trial.name,
    "operations (lower is better)": lambda trial: trial.operations,
    "time (lower is better)": lambda trial: trial.time,
    "speed (higher is better)": lambda trial: -trial.op_speed,
}

for metric_name, metric_sort_key in metrics.items():
    print(f"Metric: {metric_name}")
    generate_report(trials, metric_sort_key)
    print()

