import pandas as pd
import matplotlib.pyplot as plt
import os


df = pd.read_csv('petri_results.csv', names=['runner_name', 'case_name', 'index', 'time', 'expanded_states', 'explored_states', 'discovered_states'])

pairs = df[['runner_name', "case_name"]].drop_duplicates().values

if not os.path.exists('plots'):
    os.makedirs('plots')


# Bell curve esque plot but with all solvers on the same plot. Contains both the median and average time for each solver
for _, test_case in pairs:
    plt.figure(figsize=(10, 6))
    stats = []
    for runner in df['runner_name'].unique():
        subset = df[(df['runner_name'] == runner) & (df['case_name'] == test_case)]
        subset['time'].plot(kind='density', label=runner)

        # Calculate the median and average time for each runner
        median_time = subset['time'].median()
        average_time = subset['time'].mean()
        stats.append(f'Runner: {runner}\nMedian Time: {median_time:.4f}\nAverage Time: {average_time:.4f}\n')
  
    plt.title(f'Density Plot for Problem: {test_case}')
    plt.xlabel('Time Spent on Verification')

    # Weird hack to get the legend to display outside the box for median and average time
    plt.gca().legend(loc='best',  bbox_to_anchor=(0, 0, 1, 0.6))
    
    # Display these in a box on the upper right corner of each plot
    textstr = '\n'.join(stats)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.gca().text(0.95, 0.95, textstr, transform=plt.gca().transAxes, fontsize=10,
                   verticalalignment='top', horizontalalignment='right', bbox=props)

    filename = f'plots/Density_{test_case}.png'
    plt.savefig(filename)

    plt.close()


"""
# Bell curve esque plot
for runner, test_case in pairs:
    subset = df[(df['runner_name'] == runner) & (df['case_name'] == test_case)]
    plt.figure(figsize=(10, 6))
    subset['time'].plot(kind='density')
    plt.title(f'Runner: {runner}, Problem: {test_case}')
    plt.xlabel('Time')

    # Calculate the median and average time
    median_time = subset['time'].median()
    average_time = subset['time'].mean()

    # Display these in a box on the upper right corner of each plot
    textstr = f'Median Time: {median_time:.4f}\nAverage Time: {average_time:.4f}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.gca().text(0.95, 0.95, textstr, transform=plt.gca().transAxes, fontsize=10,
                   verticalalignment='top', horizontalalignment='right', bbox=props)

    #Saving the plots
    filename = f'plots/{runner}_{test_case}.png'
    plt.savefig(filename)
"""


""" Creates a weird plot
for runner, test_case in pairs:
    subset = df[(df['runner_name'] == runner) & (df['case_name'] == test_case)]
    plt.figure(figsize=(10, 6))
    plt.plot(subset['index'], subset['time'], 'o-')
    plt.title(f'Runner: {runner}, Test Case: {test_case}')
    plt.xlabel('Index')
    plt.ylabel('Time')
    
    #Saving the plots
    filename = f'plots/{runner}_{test_case}.png'
    plt.savefig(filename)
"""