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
    a = java.math.BigInteger('0');
    b = java.math.BigInteger('1');
    n = 1;

    while true
        % Check if time limit is exceeded
        elapsed_time = toc;
        if elapsed_time >= time_limit
            break;
        end

        % Compute the next Fibonacci number iteratively
        c = a.add(b);
        a = b;
        b = c;
        n = n + 1;

        % Check time after computation
        elapsed_time = toc;
        if elapsed_time >= time_limit
            break;
        end
    end

    % Calculate the number of digits
    number_of_digits = b.toString.length();
end
