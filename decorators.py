import time

def measureTime(func):
    def wrapper(*args, **kwargs):
        starttime = time.perf_counter()
        temp = func(*args, **kwargs)
        endtime = time.perf_counter()
        print(f"Time needed to run {func.__name__}: {endtime - starttime} seconds")
        return(temp)
    return wrapper