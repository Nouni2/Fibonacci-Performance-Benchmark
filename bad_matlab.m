% matlab.m

% Parameters for the experiment
time_limit = 1;      % Time limit in seconds
num_trials = 100;    % Number of trials
digit_counts = zeros(num_trials, 1);
language = 'MATLAB'; % Language identifier

% Open a CSV file to write the results
fileID = fopen('matlab.csv', 'w');
fprintf(fileID, 'Language,Trial,Number of Digits\n');

% Run the experiment multiple times
for i = 1:num_trials
    digit_count = largest_fibonacci_in_time_limit(time_limit);
    digit_counts(i) = digit_count;
    fprintf(fileID, '%s,%d,%d\n', language, i, digit_count);
end

fclose(fileID);

% Calculate the mean and standard deviation
mean_digits = mean(digit_counts);
stdev_digits = std(digit_counts);

% Display the results
fprintf('Over %d trials with a %.1f-second time limit in %s:\n', num_trials, time_limit, language);
fprintf('Mean number of digits: %.2f\n', mean_digits);
fprintf('Standard deviation: %.2f\n', stdev_digits);

% Function definitions
function number_of_digits = largest_fibonacci_in_time_limit(time_limit)
    tic;  % Start timing
    n = 1;
    largest_fib = java.math.BigInteger('0');
    
    while true
        elapsed_time = toc;
        if elapsed_time >= time_limit
            break;
        end

        % Compute the nth Fibonacci number using iterative fast doubling
        fib_n = fibonacci_fast_doubling(n);

        % Check time after computation
        elapsed_time = toc;
        if elapsed_time >= time_limit
            break;
        end

        largest_fib = fib_n;
        n = n + 1;
    end

    % Calculate the number of digits
    number_of_digits = length(char(largest_fib.toString));
end

% Iterative fast doubling Fibonacci function using Java BigInteger
function F = fibonacci_fast_doubling(n)
    a = java.math.BigInteger('0');
    b = java.math.BigInteger('1');
    m = n;
    binary_n = dec2bin(n);
    for k = 1:length(binary_n)
        c = a.multiply(b.shiftLeft(1).subtract(a)); % c = a*(2b - a)
        d = a.multiply(a).add(b.multiply(b));       % d = a^2 + b^2
        if binary_n(k) == '0'
            a = c;
            b = d;
        else
            a = d;
            b = c.add(d);
        end
    end
    F = a;
end
