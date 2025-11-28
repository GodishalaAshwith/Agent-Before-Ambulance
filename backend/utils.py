import time
import functools
from google.api_core import exceptions
import random

def retry_with_backoff(retries=3, initial_delay=1, backoff_factor=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            for i in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions.ResourceExhausted as e:
                    last_exception = e
                    if i == retries:
                        break
                    sleep_time = delay + random.uniform(0, 0.1)
                    print(f"Rate limit hit. Retrying in {sleep_time:.2f}s...")
                    time.sleep(sleep_time)
                    delay *= backoff_factor
            raise last_exception
        return wrapper
    return decorator
