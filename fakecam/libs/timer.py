import time

IS_DEBUG = False

def time_func(func):
    def timer_wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        if IS_DEBUG:
            print(f"Exec of: {func.__name__}\n\tTook {(time.time() - start):.4f} seconds")
        return result
    return timer_wrapper
