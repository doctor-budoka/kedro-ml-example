import functools
import random
from sys import maxsize as sys_maxsize

import numpy as np

MAX_SEED = 2**32 - 1


def log_seed(logger):
    """A decorator for logging the ransom seed for an operation"""

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            seed = random.randrange(min(sys_maxsize, MAX_SEED))
            logger.info(f"Using random seed: {seed}")
            random.seed(seed)
            np.random.seed(seed)
            return fn(*args, **kwargs)

        return wrapper

    return decorator
