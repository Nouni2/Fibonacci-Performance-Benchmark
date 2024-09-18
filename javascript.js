// javascript.js

const fs = require('fs');

// Parameters for the experiment
const timeLimit = 1;    // Time limit in seconds
const numTrials = 100;  // Number of times to run the experiment
const digitCounts = [];
const language = 'JavaScript';  // Language identifier

// Open a CSV file to write the results
const csvFileName = 'javascript.csv';
const header = 'Language,Trial,Number of Digits\n';
fs.writeFileSync(csvFileName, header);

// Run the experiment multiple times
for (let i = 1; i <= numTrials; i++) {
    const digitCount = largestFibonacciInTimeLimit(timeLimit);
    digitCounts.push(digitCount);
    const dataLine = `${language},${i},${digitCount}\n`;
    fs.appendFileSync(csvFileName, dataLine);
}

// Calculate the mean and standard deviation
const meanDigits = calculateMean(digitCounts);
const stdDevDigits = calculateStdDev(digitCounts, meanDigits);

// Print the results to the console
console.log(`Over ${numTrials} trials with a ${timeLimit}-second time limit in ${language}:`);
console.log(`Mean number of digits: ${meanDigits.toFixed(2)}`);
console.log(`Standard deviation: ${stdDevDigits.toFixed(2)}`);

// Function to compute the largest Fibonacci number within a time limit and its digit count
function largestFibonacciInTimeLimit(timeLimitSeconds) {
    const startTime = process.hrtime.bigint();
    let n = 1n;
    let largestFib = 0n;

    while (true) {
        // Check if time limit is exceeded
        const elapsedTime = Number(process.hrtime.bigint() - startTime) / 1e9;
        if (elapsedTime >= timeLimitSeconds) {
            break;
        }

        // Compute the nth Fibonacci number using fast doubling
        const fibN = fibonacciFastDoubling(n);

        // Check again after computation
        const elapsedTimeAfter = Number(process.hrtime.bigint() - startTime) / 1e9;
        if (elapsedTimeAfter >= timeLimitSeconds) {
            break;
        }

        largestFib = fibN;
        n += 1n;
    }

    // Calculate the number of digits
    if (largestFib > 0n) {
        const numberOfDigits = largestFib.toString().length;
        return numberOfDigits;
    } else {
        return 1;
    }
}

// Optimized Fibonacci using the fast doubling method
function fibonacciFastDoubling(n) {
    return fib(n)[0];

    function fib(n) {
        if (n === 0n) {
            return [0n, 1n];
        } else {
            const [a, b] = fib(n >> 1n);
            const c = a * ((b << 1n) - a);
            const d = a * a + b * b;
            if (n & 1n) {
                return [d, c + d];
            } else {
                return [c, d];
            }
        }
    }
}

// Function to calculate mean
function calculateMean(data) {
    const sum = data.reduce((acc, val) => acc + val, 0);
    return sum / data.length;
}

// Function to calculate standard deviation
function calculateStdDev(data, mean) {
    const sum = data.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0);
    return Math.sqrt(sum / data.length);
}
