import time
import math
import statistics
import csv

# Optimized Fibonacci using the fast doubling method
def fibonacci_fast_doubling(n):
    def fib(n):
        if n == 0:
            return (0, 1)
        else:
            a, b = fib(n >> 1)
            c = a * (2 * b - a)
            d = a * a + b * b
            if n & 1:
                return (d, c + d)
            else:
                return (c, d)
    return fib(n)[0]

# Function to compute the largest Fibonacci number within a time limit and its digit count
def largest_fibonacci_in_time_limit(time_limit):
    start_time = time.perf_counter()
    n = 1
    largest_fib = 0

    while True:
        # Check if time limit is exceeded
        if time.perf_counter() - start_time >= time_limit:
            break

        # Compute the nth Fibonacci number using fast doubling
        fib_n = fibonacci_fast_doubling(n)

        # Check again after computation
        if time.perf_counter() - start_time >= time_limit:
            break

        largest_fib = fib_n
        n += 1

    # Calculate the number of digits without converting to a string for performance
    if largest_fib > 0:
        number_of_digits = largest_fib.bit_length() * math.log10(2)
        number_of_digits = int(number_of_digits) + 1
    else:
        number_of_digits = 1

    return number_of_digits

# Parameters for the experiment
time_limit = 1  # Time limit in seconds
num_trials = 100  # Number of times to run the experiment
digit_counts = []
language = 'Python'  # Language identifier

# Open a CSV file to write the results
with open('fibonacci_results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header with Language, Trial, and Number of Digits
    writer.writerow(['Language', 'Trial', 'Number of Digits'])

    # Run the experiment multiple times
    for i in range(1, num_trials + 1):
        digit_count = largest_fibonacci_in_time_limit(time_limit)
        digit_counts.append(digit_count)
        writer.writerow([language, i, digit_count])

# Calculate the mean and standard deviation
mean_digits = statistics.mean(digit_counts)
stdev_digits = statistics.stdev(digit_counts)

# Print the results to the console
print(f"Over {num_trials} trials with a {time_limit}-second time limit in {language}:")
print(f"Mean number of digits: {mean_digits}")
print(f"Standard deviation: {stdev_digits}")
