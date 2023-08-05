"""
    Timeit decorator.
    This decorator will run n_times a function and output the execution times.

    More info about decorators at: https://develop.villoro.com/post/decorators

    It uses 'perf_counter' instead of 'time' since it has more precission
"""

import functools
from time import perf_counter


def timeit(func):
    """
        Decorator that prints the execution time of a function. Example:

        from time import sleep

        @timeit
        def sleep_one_sec():
            sleep(1)
    """

    @functools.wraps(func)
    def timed(*args, **kwa):
        """ Prints the execution time of the decorated function """
        time0 = perf_counter()
        result = func(*args, **kwa)
        total_time = round((perf_counter() - time0) / 60, 2)

        print("timeit: '{}' in {:.2f} min".format(func.__name__, total_time))

        return result

    return timed


def stimeit(output_func=print):
    """
        Decorator that displays the execution time of a function.
        Allows to use custom output functions (like print, log.info...)

        Example:

        from time import sleep

        @stimeit(log.info)
        def sleep_one_sec():
            sleep(1)
    """

    def timeit_decorator(func):
        """ Decorator to time the execution of a function """

        @functools.wraps(func)
        def timed_execution(*args, **kwa):
            """ Prints the execution time of the decorated function """
            time0 = perf_counter()
            result = func(*args, **kwa)
            total_time = perf_counter() - time0

            output_func("stimeit: '{}' in {:.2f}".format(func.__name__, round(total_time / 60, 2)))

            return result

        return timed_execution

    return timeit_decorator


def mesure(func, *args, n_iterations=10, **kwargs):
    """ Allows to time a function n times """

    out = []
    for _ in range(n_iterations):
        time0 = perf_counter()
        func(*args, **kwargs)
        out.append(perf_counter() - time0)

    return out
