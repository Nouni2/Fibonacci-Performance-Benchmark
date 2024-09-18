import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np

mergeBool = False

if mergeBool:
    # List of CSV files to merge
    csv_files = [
        'bad_matlab.csv',
        'c.csv',
        'cpp.csv',
        'java.csv',
        'javascript.csv',
        'matlab.csv',
        'python(NotWSL).csv',
        'python.csv'
    ]

    # Initialize an empty list to hold DataFrames
    dfs = []

    # Read each CSV file and append to the list
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            dfs.append(df)
            print(f"Successfully read {file}")
        except Exception as e:
            print(f"Error reading {file}: {e}")

    # Concatenate all DataFrames
    combined_df = pd.concat(dfs, ignore_index=True)

    # Write the combined DataFrame to a new CSV file
    combined_df.to_csv('results.csv', index=False)
    print("All files have been merged into results.csv")

# Read the combined data
combined_df = pd.read_csv('results.csv')

# Group by Language and compute mean and standard deviation
grouped = combined_df.groupby('Language')['Number of Digits']
stats_df = grouped.agg(['mean', 'std']).reset_index()

# Plotting
languages = stats_df['Language']
means = stats_df['mean']
stds = stats_df['std']

x = np.arange(len(languages))  # the label locations
width = 0.4  # the width of the bars

fig, ax1 = plt.subplots(figsize=(12, 7))

# Plot the mean on ax1
rects1 = ax1.bar(x - width/2, means, width, label='Mean', color='blue')
ax1.set_xlabel('Language')
ax1.set_ylabel('Mean Number of Digits', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Create a twin Axes sharing the x-axis
ax2 = ax1.twinx()

# Plot the standard deviation on ax2
rects2 = ax2.bar(x + width/2, stds, width, label='Standard Deviation', color='red')
ax2.set_ylabel('Standard Deviation', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Adjust x-axis labels
ax1.set_xticks(x)
ax1.set_xticklabels(languages, rotation=45, ha='right')

# Add legends
lines_labels = [ax.get_legend_handles_labels() for ax in [ax1, ax2]]
handles, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=2)

fig.tight_layout()

plt.title('Mean and Standard Deviation of Number of Digits per Language')
plt.show()
