
# Andrew Kavas
# BCI Drone project
# Grapher for verification

import os, sys
import timeit
import numpy as np
import pandas as pd
from sklearn import preprocessing
import matplotlib.pyplot as plt


def electrode_graph(data):

    electrode_names = np.array(['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4'])
    electrodes, label_names = data.columns.values[4:18], data.columns.values[20:]

    fig, ax = plt.subplots(nrows=7, ncols=1, figsize=[11, 8])
    fig.suptitle('Electrodes (AF3-O1))', fontsize=16)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

    for kk in range(0, 7):
        ax[kk].set_title(electrode_names[kk])  # TODO!
        data.plot.line(y=electrodes[kk], ax=ax[kk])
        data.plot.line(y=label_names[0], ax=ax[kk])

    plt.show()

    fig, ax = plt.subplots(nrows=7, ncols=1, figsize=[11, 8])
    fig.suptitle('Electrodes (O2-AF4)', fontsize=16)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

    for kk in range(0, 7):
        ax[kk].set_title(electrode_names[kk+7])
        data.plot.line(y=electrodes[7+kk], ax=ax[kk])
        data.plot.line(y=label_names[0], ax=ax[kk])

    plt.show()


def zoom_graph(data):

    electrodes, label_names = data.columns.values[4:18], data.columns.values[20:]
    # zoom in for one electrode
    steps = 5
    hz = 128

    fig, axes = plt.subplots(nrows=(steps+1), ncols=1, figsize=[11, 8])
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    fig.suptitle('Zoom on FC5', fontsize=16)
    data.plot.line(y=electrodes[3], ax=axes[0])
    data.plot.line(y=label_names[4], ax=axes[0])

    breaks = np.linspace(hz*20, (len(data)-hz*20), steps)
    for kk in range(1, steps+1):
        end = int(len(data) - breaks[kk-1])
        data_z = data[:end]
        data_z.plot.line(y=electrodes[3], ax=axes[kk])
        data_z.plot.line(y=label_names[4], ax=axes[kk])

    plt.show()


def label_graph(data, div):

    electrodes, label_names = data.columns.values[4:18], data.columns.values[20:]
    print(label_names)
    label_n = int(len(label_names) / div)

    fig, axes = plt.subplots(nrows=label_n, ncols=1, figsize=[11, 8])
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    fig.suptitle('Labels', fontsize=16)

    for kk in range(0, label_n):
        data.plot.line(y=electrodes[3], ax=axes[kk])
        data.plot.line(y=label_names[kk * div], ax=axes[kk])
    plt.show()


def formatter(data):
    # prepare data
    min_max_scaler = preprocessing.MinMaxScaler()
    data_file = pd.read_csv(folder_in + file_in)

    cols = data_file.columns
    electrodes, labels = cols[4:18], cols[20:]
    data_frame = pd.DataFrame(min_max_scaler.fit_transform(data_file)).drop(0)

    return data_frame


def main(data):

    # length, hz = 16, 128
    # data_short = data[0:int(length * hz)]
    zoom_graph(data)
    electrode_graph(data)

    divisor = int(3)
    label_graph(data, divisor)


t_0 = timeit.default_timer()


# i/o paths
# folder_in = '/Users/andrew/Google_Drive/BCI/Data/Profiles/users/efrantz/lab/19-02-06'
folder_in = '/Users/andrew/Code/Data/EEG/hz_128/users/jjoiner/lab/19-02-07'
file_in = '/c1_1s_5s_t0_lab.csv'

data_frame = formatter(folder_in + file_in)
main(data_frame)


t_f = round((timeit.default_timer() - t_0), 2)
print('\n', 'Process took: ' + str(t_f) + 's')


# TODO: make it...

# TODO: 1) graph saved csv
# TODO:      a) graph main electrodes for useful time
# TODO:      b) graph labels intuitively

# TODO: 2) graph live data
# TODO: 3)
# TODO: 4)

# TODO: LIST OF BAD FILES:
# TODO: akavas --> c1, (c2?),

