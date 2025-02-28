import time

import numpy as np
from loguru import logger

from et.utils.pretty_print import color


def timeit(f, trials=1):
    """
    Decorator to time a function. I stole these code snippets from some random Stack Overflow posts.

    Example usage:
    ```
    import functools as ft
    @ft.partial(timeit, trials=10)
    def foo():
        return sum([i for i in range(1000000)])
    ```

    Parameters
    ----------
    f : function
        Function to time.
    trials : int
        Number of trials to run the function.

    Returns
    -------
    timed : function
        Decorated
    """

    def timed(*args, **kw):
        result, times = None, []
        for _ in range(trials):
            ts = time.time()
            result = f(*args, **kw) if result is None else result
            te = time.time()
            times.append(te - ts)
        mean, var, median = np.mean(times), np.var(times), np.median(times)
        logger \
            .opt(colors=True) \
            .debug(f"{color.END}func: {color.BOLD + color.GREEN}{f.__name__}{color.END * 2} "
                   # f"| args: [{args}, {kw}]{'':<10}"  # Comment for now, it is unsafe. 
                   f"| trials: {color.BOLD}{trials}{color.END} "
                   f"| mean: {color.BOLD + color.RED}{mean:.3f}s {color.PLUSMINUS} {var:.2f}s{color.END * 2} "
                   f"| median: {color.BOLD + color.BLUE}{median:.3f}s{color.END * 2}")
        return result

    return timed
