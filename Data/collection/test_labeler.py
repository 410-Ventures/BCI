
# test

import os, sys
import timeit
import numpy as np
import pandas as pd
from sklearn import preprocessing
import matplotlib.pyplot as plt


def iterator(df, co, hz, durat, itttern, shift, t_length):
    end = len(df)
    start = int((itttern - durat / 2) * hz)
    gap = np.zeros(int((itttern - durat) * hz))
    shifter = int(shift * hz)  # seconds shifted

    # create arr to append to df
    label_arr = np.zeros(start)
    ii, jj = start, int(start + durat * hz)

    while ii < end:
        # add label
        if ii < jj:
            label_arr = np.append(label_arr, co)
            ii = ii + 1
        # add zeros to end of df
        elif int(ii + (itttern - durat) * hz) > end:
            end_zeros = np.zeros(end - ii)
            label_arr = np.append(label_arr, end_zeros)
            break
        # skip ahead by (iteration - duration)
        else:
            label_arr = np.append(label_arr, gap)
            ii = int(ii + (itttern - durat) * hz)
            jj = int(jj + itttern * hz)

    # shift values
    if shifter >= 0:
        # shave off shifter values from end
        label_arr = label_arr[:(end - shifter)]
        # insert shifter-many zeros at beginning
        shift_zeros = np.zeros(shifter)
        label_arr = np.append(shift_zeros, label_arr)
    elif shifter <= 0:
        # shave off shifter values from end
        label_arr = label_arr[-shifter:]
        # insert shifter-many zeros at beginning
        shift_zeros = np.zeros(-shifter)
        label_arr = np.append(label_arr, shift_zeros)

    # make final 5s zeros
    for kk in range(0, 5 * hz):
        label_arr[kk] = 0
        label_arr[(end - kk) - 1] = 0

    return label_arr


def labeler(data, hz, comm, lab_info, dura, ittern, shift, trial_len):  # duration, interval, length, trial):

    # cutoff all data past trial length
    data = data[0:(int(trial_length * hz))]
    # cutoff first and last 5s
    trunk = data[(5 * hz):(int(hz * (trial_len-5)))]
    trunk = trunk.reset_index(drop=True)

    # add labels
    signal_lengths = np.linspace(lab_info[0], lab_info[1], lab_info[2])  # BIG IMPORTANT
    for ii in range(0, len(shift)):
        for kk in range(0, lab_info[2]):
            # troubleshooting for label length vs iteration length
            if dura * signal_lengths[lab_info[2] - 1] > ittern:
                print('Check duration vs iteration!')
                break
            else:
                label_arr = iterator(trunk, comm, hz, dura * signal_lengths[kk], ittern, 0, trial_len)
                label_arr2 = iterator(trunk, comm, hz, dura * signal_lengths[kk], ittern, shift[ii], trial_len)
                label_arr3 = iterator(trunk, comm, hz, dura * signal_lengths[kk], ittern, -shift[ii], trial_len)
                trunk[f'LABEL_{(ii * (lab_info[2])) + kk + 1}'] = label_arr
                trunk[f'LABEL_{(lab_info[2] * len(shift)) + (ii * (lab_info[2])) + kk + 1}'] = label_arr2
                trunk[f'LABEL_{(lab_info[2] * len(shift))*2 + (ii * (lab_info[2])) + kk + 1}'] = label_arr3

    return trunk


def graph(data_0):

    # TODO: graph all electrodes
    # normalize
    min_max_scaler = preprocessing.MinMaxScaler()
    data = pd.DataFrame(min_max_scaler.fit_transform(data_0))

    # name simplification
    columns = np.array(data.columns.values)
    electrodes, col_names = columns[3:17], columns[19:]
    label_len = len(col_names)
    fig, axes = plt.subplots(nrows=label_len, ncols=1)

    for kk in range(0, label_len):
        data.plot.line(y=4, ax=axes[kk])
        data.plot.line(y=col_names[kk], ax=axes[kk])

    plt.show()


def main(data_path, com, hz, dur, itter, lab_control, shiftr, trial_leng):

    raw_df = pd.read_csv(data_path)
    lab_data = labeler(raw_df, hz, com, lab_control, dur, itter, shiftr, trial_leng)
    graph(lab_data)

    return raw_df, lab_data


time_start = timeit.default_timer()

# inputs
Hz = 128                            # sampling freq                                 # TODO: CHECK!
iteration = 5                       # seconds between command inputs                # TODO: CHECK
duration = 1                        # seconds per command input                     # TODO: CHECK
labels = [.5, 3, 6]                 # [smallest, largest, number]                   # TODO: CHECK
shifts = [0.2, 0.4, 0.8]                                                            # TODO: CHECK

# trial info
user = 'test'                                                                      # TODO: CHECK!
date = '19-02-08'                  # YY-MM-DD                                     # TODO: CHECK!
command = 1                                                                        # TODO: CHECK!
trial = 0                                                                          # TODO: CHECK!
trial_length = 240                  # seconds                                      # TODO: CHECK!

# i/o paths
file_in = '/Volumes/BOOTCAMP/Code/BCI/cortex_Code_G/EEGLogger/bin/Debug/EEGLogger.csv'
out_home = '/Users/andrew/Code/BCI/templates/Data/profiles'

raw_path = str(out_home + '/' + user + '/f_' + str(Hz) + '/' + date + '/raw')
lab_path = str(out_home + '/' + user + '/f_' + str(Hz) + '/' + date + '/lab')
if not os.path.exists(raw_path):
    os.makedirs(raw_path)
if not os.path.exists(lab_path):
    os.makedirs(lab_path)

# call main
dfs = main(file_in, command, Hz, duration, iteration, labels, shifts, trial_length)
file_name = ('c' + str(command) + '_' + str(duration) + 's_' + str(iteration) + 's_t' + str(trial))

# output raw, labeled, and simplified csv files (takes ~2 s/file)
dfs[0].to_csv(raw_path + '/' + f'{file_name}_raw.csv')
dfs[1].to_csv(lab_path + '/' + f'{file_name}_lab.csv')
print('Df', '\n', 'raw: ', dfs[0].shape, '\n', 'lab: ', dfs[1].shape)


print('Process took', round(timeit.default_timer() - time_start, 2), 'seconds', '\n')
print('Check the database!')


# TODO: 1) verify that all new data is unique and correctly labeled!
# TODO: 2)

