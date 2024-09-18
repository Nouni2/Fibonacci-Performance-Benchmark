import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Create 'results' folder if it doesn't exist
if not os.path.exists('results'):
    os.makedirs('results')

# Read the combined data
combined_df = pd.read_csv('results.csv')

# Ensure that 'Language' is treated as a categorical variable
combined_df['Language'] = combined_df['Language'].astype('category')

# 1. Box Plot
plt.figure(figsize=(12, 7))
combined_df.boxplot(column='Number of Digits', by='Language', grid=False)
plt.title('Distribution of Number of Digits per Language')
plt.suptitle('')
plt.xlabel('Language')
plt.ylabel('Number of Digits')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('results/box_plot.png')
plt.close()

# 2. Violin Plot
plt.figure(figsize=(12, 7))
sns.violinplot(x='Language', y='Number of Digits', data=combined_df, inner='quartile')
plt.title('Distribution of Number of Digits per Language')
plt.xlabel('Language')
plt.ylabel('Number of Digits')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('results/violin_plot.png')
plt.close()

# 3. Box Plot with Data Points Overlayed
plt.figure(figsize=(12, 7))
sns.boxplot(x='Language', y='Number of Digits', data=combined_df, showfliers=False)
sns.stripplot(x='Language', y='Number of Digits', data=combined_df, color='black', alpha=0.5)
plt.title('Distribution of Number of Digits per Language with Data Points')
plt.xlabel('Language')
plt.ylabel('Number of Digits')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('results/box_plot_with_data_points.png')
plt.close()

# 4. Bar Plot with Error Bars
# Group by Language and compute mean and standard deviation
stats_df = combined_df.groupby('Language')['Number of Digits'].agg(['mean', 'std']).reset_index()
languages = stats_df['Language']
means = stats_df['mean']
stds = stats_df['std']
x_pos = np.arange(len(languages))

fig, ax = plt.subplots(figsize=(12, 7))
ax.bar(x_pos, means, yerr=stds, align='center', alpha=0.7, capsize=10, color='blue')
ax.set_ylabel('Mean Number of Digits')
ax.set_xlabel('Language')
ax.set_xticks(x_pos)
ax.set_xticklabels(languages, rotation=45, ha='right')
ax.set_title('Mean Number of Digits per Language with Standard Deviation')
plt.tight_layout()
plt.savefig('results/bar_plot_with_error_bars.png')
plt.close()

# 5. ECDF Plot
plt.figure(figsize=(12, 7))
for language in combined_df['Language'].unique():
    subset = combined_df[combined_df['Language'] == language]
    sns.ecdfplot(subset['Number of Digits'], label=language)
plt.title('ECDF of Number of Digits per Language')
plt.xlabel('Number of Digits')
plt.ylabel('Proportion')
plt.legend()
plt.tight_layout()
plt.savefig('results/ecdf_plot.png')
plt.close()

# 6. Faceted Histograms
g = sns.FacetGrid(combined_df, col='Language', col_wrap=4, height=4)
g.map(sns.histplot, 'Number of Digits', bins=20)
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Distribution of Number of Digits per Language')
plt.savefig('results/faceted_histograms.png')
plt.close()

# 7. Combined Bar Plot and Box Plot
fig, ax = plt.subplots(figsize=(12, 7))
ax.bar(x_pos, means, yerr=stds, align='center', alpha=0.7, capsize=10, color='skyblue')
ax.set_xlabel('Language')
ax.set_ylabel('Mean Number of Digits')
ax.set_xticks(x_pos)
ax.set_xticklabels(languages, rotation=45, ha='right')
ax.set_title('Mean Number of Digits per Language with Standard Deviation')

# Add box plots below the bar plot
for i, language in enumerate(languages):
    data = combined_df[combined_df['Language'] == language]['Number of Digits']
    ax.boxplot(data, positions=[x_pos[i]], widths=0.3, patch_artist=True,
               boxprops=dict(facecolor='lightgreen', color='green'),
               medianprops=dict(color='red'), showfliers=False)

plt.tight_layout()
plt.savefig('results/combined_bar_box_plot.png')
plt.close()
