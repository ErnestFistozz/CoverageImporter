import pandas as pd
import matplotlib.pyplot as plt

def plot_graphs(filename, header_names):
    df = pd.read_csv(filename, names = header_names)
    #bins = [0, 10, 20, 30, 40, 50]
    bins = [0, 25, 50, 75, 100] 
    #labels = ['0-10', '11-20', '21-30', '31-40', '41-50']
    labels = ['0-25', '25-50', '50-75', '75-100']
    df['Bin'] = pd.cut(df['patch_coverage'], bins=bins, labels=labels, right=False)
    pivot_table = df.pivot_table(index='repository_name', columns='Bin', aggfunc='size', fill_value=0)
    total_rows = df['repository_name'].value_counts()
    fig, ax1 = plt.subplots(figsize=(10, 6))

    pivot_table.plot(kind='barh', stacked=True, ax=ax1)
    ax1.set_title('Horizontally Stacked Bar Graph')
    ax1.set_xlabel('Coverage Percentage')
    ax1.set_ylabel('Project Name')
    ax1.legend(title='Bin', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.tick_params(axis='y', labelcolor='black')

    ax12 = ax1.twinx()  # Create a second y-axis on the right

    # Set the y-axis ticks to display total rows without labeling
    ax12.set_yticks(range(len(total_rows)))
    ax12.set_yticklabels(total_rows.values)
    ax12.tick_params(axis='y', labelcolor='gray')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # headers = [ 'date', 'commitHash', 'api_coverage', 'branch', 
    #             'code_patch_size', 'test_patch_size', 'config_patch_size',
    #             'test_files', 'code_files', 'test_code_files', 'other_files',
    #             'patch_coverage', 'repository_name', 'computed_coverage', 'dmm_unit_size',
    #             'dmm_unit_complexity', 'dmm_unit_interface', 'dmm', 'crap_metric'
    #             ]
    headers = [ 'date', 'commitHash', 'coverage_change', 'coverage', 'branch',
                'code_patch_size', 'test_patch_size', 'config_patch_size',
                'test_files', 'code_files', 'test_code_files', 'other_files',
                'patch_coverage', 'repository_name', 'dmm_unit_size',
                'dmm_unit_complexity', 'dmm_unit_interface', 'dmm', 'crap_metric'
                ]
    plot_graphs('large_scale_paper_coveralls_result.csv', headers)
    #  df = pd.read_csv('codecovdata.csv', names = headers)
    #  print(df['patch_coverage'])


            