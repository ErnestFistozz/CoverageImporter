import pandas as pd
import matplotlib.pyplot as plt

# Sample data
data = [
    ('a', 1),
    ('b', 0),
    ('b', 12),
    ('b', 48),
    ('a', 0),
    ('a', 0),
    ('c', 17),
    ('c', 33),
    ('c', 2),
]

# Create a DataFrame
df = pd.DataFrame(data, columns=['Column1', 'Column2'])

# Group by 'Column1' and categorize counts into bins
bins = [0, 10, 20, 30, 40, 50]
labels = ['0-10', '11-20', '21-30', '31-40', '41-50']
df['Bin'] = pd.cut(df['Column2'], bins=bins, labels=labels, right=False)

# Pivot the data to create a pivot table
pivot_table = df.pivot_table(index='Column1', columns='Bin', aggfunc='size', fill_value=0)

# Calculate the total number of rows per first column
total_rows = df['Column1'].value_counts()

# Plot only the horizontally stacked bar graph
fig, ax1 = plt.subplots(figsize=(10, 6))

pivot_table.plot(kind='barh', stacked=True, ax=ax1)
ax1.set_title('Horizontally Stacked Bar Graph')
ax1.set_xlabel('Count')
ax1.set_ylabel('Column1')
ax1.legend(title='Bin', bbox_to_anchor=(1.05, 1), loc='upper left')
ax1.tick_params(axis='y', labelcolor='black')

ax12 = ax1.twinx()  # Create a second y-axis on the right

# Set the y-axis ticks to display total rows without labeling
ax12.set_yticks(range(len(total_rows)))
ax12.set_yticklabels(total_rows.values)
ax12.tick_params(axis='y', labelcolor='gray')

plt.tight_layout()
plt.show()
