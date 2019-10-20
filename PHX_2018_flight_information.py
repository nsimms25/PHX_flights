"""
Arrival and Departure Flight information for PHX International Airport for 2018.

Information provided by
https://www.phoenixopendata.com/dataset/aviation-flight-information
"""

import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np


def plot_airliners(csv):
    """Plot a bar chart for the number of flights that Arrived or Departed at PHX Airport."""
    unique_airlines = csv['Airline'].unique()
    airline_list = []

    for airline in unique_airlines:
        flights = (csv[csv['Airline'] == airline]).count()
        if 'Airlines' in airline:
            airline_label = airline.replace('Airlines', '')
        else:
            airline_label = airline
        airline_list.append({'Airliner': airline_label, 'Number of flights': flights[0]})

    data_frame = pd.DataFrame(airline_list)
    data_frame = data_frame.sort_values(by='Number of flights', ascending=False)
    data_frame = data_frame.set_index('Airliner')

    # print(data_frame)

    data_frame.plot.bar()
    plt.xlabel('Airliner')
    plt.xticks(rotation=30)
    plt.ylabel('Number of flights')
    plt.show()


def plot_terminals(csv):
    """Plot a bar chart for the terminal uses for each airliner that Arrived or Depart at PHX airport."""
    unique_terminals = csv['Terminal'].dropna().unique()

    terminal_list = []

    for terminal in unique_terminals:
        flights = (csv[csv['Terminal'] == terminal]).count()
        # print(flights)
        terminal_list.append({'Terminal': int(terminal), 'Number of flights': flights[0]})

    data_frame = pd.DataFrame(terminal_list)
    data_frame = data_frame.sort_values(by='Number of flights', ascending=False)
    data_frame = data_frame.set_index('Terminal')

    # print(data_frame)

    data_frame.plot.bar()
    plt.xlabel('Terminal')
    plt.xticks(rotation=0)
    plt.ylabel('Number of flights')
    plt.show()


# get all .CSV files in the 'PHX flight information'.
glob_files = glob.glob('PHX flight information/*.csv')

file_names = []

# Reformat files from glob to be the actual file location.
for new_file in glob_files:
    temp = new_file.split('\\')
    file = 'PHX flight information/{}'.format(temp[1])
    file_names.append(file)

# Combine all CSV files into one pandas dataframe.
combined_csv = pd.concat([pd.read_csv(f, index_col=['Arrive Or Depart', 'Schedule'], parse_dates=True,
                                      infer_datetime_format=True) for f in file_names])

# Pick on single file to speed up testing, instead loading and testing over all files.
test_csv = pd.read_csv('PHX flight information/aviation-flight-information_apr_2018.csv',
                       index_col=['Arrive Or Depart', 'Schedule'], parse_dates=True, infer_datetime_format=True)

# Sort the index in order to be able to slice effectively.
combined_csv.sort_index(inplace=True)
test_csv.sort_index(inplace=True)

# Calling the function to plot all airliners and the number of flights that arrived or departed using the airliner.
# plot_airliners(combined_csv)

# Calling the function to plot all terminals and the number of flights that arrived or depart from that Terminal.
# plot_terminals(test_csv)
# plot_airliners(test_csv)

plot_terminals(combined_csv)
