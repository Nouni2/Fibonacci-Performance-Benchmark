import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;
import java.io.PrintWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

class java {
    // Function to compute Fibonacci using the fast doubling method
    public static BigInteger fibonacciFastDoubling(BigInteger n) {
        return fib(n)[0];
    }

    private static BigInteger[] fib(BigInteger n) {
        if (n.equals(BigInteger.ZERO)) {
            return new BigInteger[]{BigInteger.ZERO, BigInteger.ONE};
        } else {
            BigInteger[] ab = fib(n.shiftRight(1));
            BigInteger a = ab[0];
            BigInteger b = ab[1];
            BigInteger c = a.multiply(b.shiftLeft(1).subtract(a));
            BigInteger d = a.multiply(a).add(b.multiply(b));
            if (n.testBit(0)) {
                return new BigInteger[]{d, c.add(d)};
            } else {
                return new BigInteger[]{c, d};
            }
        }
    }

    // Function to compute the largest Fibonacci number within a time limit and its digit count
    public static int largestFibonacciInTimeLimit(double timeLimitSeconds) {
        long startTime = System.nanoTime();
        BigInteger n = BigInteger.ONE;
        BigInteger largestFib = BigInteger.ZERO;

        while (true) {
            // Check if time limit is exceeded
            double elapsedTime = (System.nanoTime() - startTime) / 1e9;
            if (elapsedTime >= timeLimitSeconds) {
                break;
            }

            // Compute the nth Fibonacci number using fast doubling
            BigInteger fibN = fibonacciFastDoubling(n);

            // Check again after computation
            elapsedTime = (System.nanoTime() - startTime) / 1e9;
            if (elapsedTime >= timeLimitSeconds) {
                break;
            }

            largestFib = fibN;
            n = n.add(BigInteger.ONE);
        }

        // Calculate the number of digits
        if (largestFib.compareTo(BigInteger.ZERO) > 0) {
            int numberOfDigits = (int) (largestFib.bitLength() * Math.log10(2)) + 1;
            return numberOfDigits;
        } else {
            return 1;
        }
    }

    // Function to calculate mean
    public static double calculateMean(List<Integer> data) {
        double sum = 0.0;
        for (int val : data) {
            sum += val;
        }
        return sum / data.size();
    }

    // Function to calculate standard deviation
    public static double calculateStdDev(List<Integer> data, double mean) {
        double sum = 0.0;
        for (int val : data) {
            sum += Math.pow(val - mean, 2);
        }
        return Math.sqrt(sum / data.size());
    }

    public static void main(String[] args) {
        double timeLimit = 1.0; // Time limit in seconds
        int numTrials = 100;    // Number of times to run the experiment
        List<Integer> digitCounts = new ArrayList<>();
        String language = "Java"; // Language identifier

        String fileName = "java.csv";

        // Delete the file if it already exists
        try {
            Files.deleteIfExists(Paths.get(fileName));
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Open the CSV file to write the results
        try (PrintWriter writer = new PrintWriter(fileName)) {
            // Write the header
            writer.println("Language,Trial,Number of Digits");

            // Run the experiment multiple times
            for (int i = 1; i <= numTrials; i++) {
                int digitCount = largestFibonacciInTimeLimit(timeLimit);
                digitCounts.add(digitCount);
                writer.println(language + "," + i + "," + digitCount);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Calculate the mean and standard deviation
        double meanDigits = calculateMean(digitCounts);
        double stdDevDigits = calculateStdDev(digitCounts, meanDigits);

        // Print the results to the console
        System.out.println("Over " + numTrials + " trials with a " + timeLimit + "-second time limit in " + language + ":");
        System.out.println("Mean number of digits: " + meanDigits);
        System.out.println("Standard deviation: " + stdDevDigits);
    }
}
