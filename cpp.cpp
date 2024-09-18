#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <cmath>
#include <string>
#include <numeric>
#include <algorithm>
#include <boost/multiprecision/cpp_int.hpp>

using namespace std;
using namespace std::chrono;
using namespace boost::multiprecision;

// Function to compute Fibonacci using the fast doubling method
void fibonacci_fast_doubling(const cpp_int& n, cpp_int& result) {
    cpp_int a = 0;
    cpp_int b = 1;
    cpp_int c, d;

    vector<bool> bits;
    cpp_int temp_n = n;
    while (temp_n > 0) {
        bits.push_back(temp_n % 2 != 0);
        temp_n /= 2;
    }

    for (auto it = bits.rbegin(); it != bits.rend(); ++it) {
        c = a * (b * 2 - a);
        d = a * a + b * b;
        if (*it) {
            a = d;
            b = c + d;
        } else {
            a = c;
            b = d;
        }
    }

    result = a;
}

// Function to compute the largest Fibonacci number within a time limit and its digit count
int largest_fibonacci_in_time_limit(double time_limit) {
    auto start_time = high_resolution_clock::now();
    cpp_int n = 1;
    cpp_int largest_fib = 0;
    cpp_int fib_n;

    while (true) {
        // Check if time limit is exceeded
        auto current_time = high_resolution_clock::now();
        duration<double> elapsed = current_time - start_time;
        if (elapsed.count() >= time_limit) {
            break;
        }

        // Compute the nth Fibonacci number using fast doubling
        fibonacci_fast_doubling(n, fib_n);

        // Check again after computation
        current_time = high_resolution_clock::now();
        elapsed = current_time - start_time;
        if (elapsed.count() >= time_limit) {
            break;
        }

        largest_fib = fib_n;
        n += 1;
    }

    // Calculate the number of digits using bit length
    if (largest_fib == 0) {
        return 1;
    } else {
        int num_bits = msb(largest_fib) + 1; // msb returns 0-based index
        double number_of_digits = num_bits * log10(2);
        return static_cast<int>(floor(number_of_digits)) + 1;
    }
}

// Function to calculate mean
double calculate_mean(const vector<int>& data) {
    return accumulate(data.begin(), data.end(), 0.0) / data.size();
}

// Function to calculate standard deviation
double calculate_stddev(const vector<int>& data, double mean) {
    double sum = 0.0;
    for (const auto& val : data) {
        sum += (val - mean) * (val - mean);
    }
    return sqrt(sum / data.size());
}

int main() {
    double time_limit = 1.0;    // Time limit in seconds
    int num_trials = 100;       // Number of times to run the experiment
    vector<int> digit_counts;
    string language = "C++";    // Language identifier

    // Open a CSV file to write the results
    ofstream file("fibonacci_results.csv");
    if (!file.is_open()) {
        cerr << "Failed to open the file." << endl;
        return 1;
    }

    // Write the header
    file << "Language,Trial,Number of Digits\n";

    // Run the experiment multiple times
    for (int i = 1; i <= num_trials; ++i) {
        int digit_count = largest_fibonacci_in_time_limit(time_limit);
        digit_counts.push_back(digit_count);
        file << language << "," << i << "," << digit_count << "\n";
    }

    file.close();

    // Calculate the mean and standard deviation
    double mean_digits = calculate_mean(digit_counts);
    double stdev_digits = calculate_stddev(digit_counts, mean_digits);

    // Print the results to the console
    cout << "Over " << num_trials << " trials with a " << time_limit << "-second time limit in " << language << ":\n";
    cout << "Mean number of digits: " << mean_digits << endl;
    cout << "Standard deviation: " << stdev_digits << endl;

    return 0;
}
