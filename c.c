#include <stdio.h>
#include <stdlib.h>
#include <gmp.h>
#include <time.h>
#include <math.h>
#include <string.h>

// Function to compute Fibonacci using the fast doubling method
void fibonacci_fast_doubling(mpz_t result, const mpz_t n) {
    if (mpz_cmp_ui(n, 0) == 0) {
        mpz_set_ui(result, 0);
        return;
    }
    mpz_t a, b, c, d, temp_n;
    mpz_inits(a, b, c, d, temp_n, NULL);
    mpz_set_ui(a, 0);
    mpz_set_ui(b, 1);
    mpz_set(temp_n, n);

    size_t size = mpz_sizeinbase(temp_n, 2);
    char *binary = (char *)malloc(size + 1);
    mpz_get_str(binary, 2, temp_n);

    for (size_t i = 0; i < strlen(binary); ++i) {
        // Square
        mpz_mul(c, a, b);
        mpz_mul_ui(c, c, 2);        // c = 2ab
        mpz_mul(d, a, a);           // d = a^2
        mpz_mul(a, b, b);           // a = b^2
        mpz_add(b, d, a);           // b = a^2 + b^2
        mpz_set(a, d);              // a = d

        if (binary[i] == '1') {
            mpz_add(d, a, c);       // d = a + c
            mpz_set(a, b);          // a = b
            mpz_set(b, d);          // b = d
        }
    }

    mpz_set(result, a);
    mpz_clears(a, b, c, d, temp_n, NULL);
    free(binary);
}

// Function to compute the largest Fibonacci number within a time limit and its digit count
int largest_fibonacci_in_time_limit(double time_limit) {
    clock_t start_time = clock();
    mpz_t n, largest_fib, fib_n;
    mpz_inits(n, largest_fib, fib_n, NULL);
    mpz_set_ui(n, 1);
    mpz_set_ui(largest_fib, 0);

    while (1) {
        // Check if time limit is exceeded
        double elapsed = (double)(clock() - start_time) / CLOCKS_PER_SEC;
        if (elapsed >= time_limit) {
            break;
        }

        // Compute the nth Fibonacci number using fast doubling
        fibonacci_fast_doubling(fib_n, n);

        // Check again after computation
        elapsed = (double)(clock() - start_time) / CLOCKS_PER_SEC;
        if (elapsed >= time_limit) {
            break;
        }

        mpz_set(largest_fib, fib_n);
        mpz_add_ui(n, n, 1);
    }

    // Calculate the number of digits using logarithms
    if (mpz_cmp_ui(largest_fib, 0) > 0) {
        size_t num_bits = mpz_sizeinbase(largest_fib, 2);
        double number_of_digits = num_bits * log10(2);
        int digits = (int)floor(number_of_digits) + 1;
        mpz_clears(n, largest_fib, fib_n, NULL);
        return digits;
    } else {
        mpz_clears(n, largest_fib, fib_n, NULL);
        return 1;
    }
}

// Function to calculate mean
double calculate_mean(int *data, int size) {
    double sum = 0.0;
    for(int i = 0; i < size; ++i) {
        sum += data[i];
    }
    return sum / size;
}

// Function to calculate standard deviation
double calculate_stddev(int *data, int size, double mean) {
    double sum = 0.0;
    for(int i = 0; i < size; ++i) {
        sum += (data[i] - mean) * (data[i] - mean);
    }
    return sqrt(sum / size);
}

int main() {
    double time_limit = 1.0;    // Time limit in seconds
    int num_trials = 100;       // Number of times to run the experiment
    int *digit_counts = malloc(num_trials * sizeof(int));
    const char *language = "C"; // Language identifier

    // Open a CSV file to write the results
    FILE *file = fopen("c.csv", "w");
    if (file == NULL) {
        fprintf(stderr, "Failed to open the file.\n");
        free(digit_counts);
        return 1;
    }

    // Write the header
    fprintf(file, "Language,Trial,Number of Digits\n");

    // Run the experiment multiple times
    for (int i = 0; i < num_trials; ++i) {
        int digit_count = largest_fibonacci_in_time_limit(time_limit);
        digit_counts[i] = digit_count;
        fprintf(file, "%s,%d,%d\n", language, i + 1, digit_count);
    }

    fclose(file);

    // Calculate the mean and standard deviation
    double mean_digits = calculate_mean(digit_counts, num_trials);
    double stdev_digits = calculate_stddev(digit_counts, num_trials, mean_digits);

    // Print the results to the console
    printf("Over %d trials with a %.1f-second time limit in %s:\n", num_trials, time_limit, language);
    printf("Mean number of digits: %.2f\n", mean_digits);
    printf("Standard deviation: %.2f\n", stdev_digits);

    free(digit_counts);
    return 0;
}
