from timeit import default_timer as timer


def benchmark(function):
    start = timer()
    function()
    end = timer()
    print("Time elapsed = {0:.2f} secs".format(end - start))
