import timeit

code_to_test = """
# Your code here
"""

time_taken = timeit.timeit(code_to_test, number=100000)
print(f"Time taken: {time_taken} seconds")