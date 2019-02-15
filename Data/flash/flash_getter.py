
# Andrew Kavas
# Project DONNA
# Data gatherer

import os, sys
import timeit
import numpy as np
import pandas as pd
from sklearn import preprocessing
import matplotlib.pyplot as plt


def bin_search(path, suffix):
    # returns csv and folder path arrays
    csv_arr, folder_arr = np.array([]), np.array([])
    content_arr = np.array(os.listdir(path))
    for kk in range(0, len(content_arr)):
        element = str(content_arr[kk])
        if element.endswith(suffix):
            csv_arr = np.append(csv_arr, str(path + '/' + element))
        if os.path.isdir(path + '/' + element):
            folder_arr = np.append(folder_arr, str(path + '/' + element))

    return csv_arr, folder_arr


def repeater(paths, sufx):
    # updates all paths to next path
    c_arr, p_arr = np.array([]), np.array([])

    for kk in range(0, len(paths)):
        aa, bb = bin_search(paths[kk], sufx)
        c_arr = np.append(c_arr, aa)
        p_arr = np.append(p_arr, bb)

    return c_arr, p_arr


def bin_tree(home_path, suf):
    path = home_path
    c_arr, p_arr = np.array([]), np.array([])

    a, b = bin_search(home_path, suf)
    c_arr, p_arr = np.append(c_arr, a), np.append(p_arr, b)
    while(len(b)) > 0:
        a, b = repeater(b, suf)
        c_arr = np.append(c_arr, a)
        p_arr = np.append(p_arr, b)

    return c_arr, p_arr


def df_maker(paths):
    d = {}
    for path in paths:
        df_r = pd.read_csv(path)
        d[path] = df_r.drop(df_r.columns[[19, 18, 2, 1, 0]], axis=1)
    return d


def aggregator(d_frames, paths):
    df = pd.DataFrame(d_frames[paths[0]])
    for kk in range(1, len(paths)):
        frame = pd.DataFrame(d_frames[paths[kk]])
        df = pd.concat([df, frame], ignore_index=True)
    return df


def normalize(data):
    # normalize
    df_values = data[data.columns[0:15]]
    df_columns = df_values.columns
    df_labels = df_all[df_all.columns[15:]]

    min_max_scaler = preprocessing.MinMaxScaler()
    df_values = pd.DataFrame(min_max_scaler.fit_transform(df_values))
    for kk in range(0, len(df_columns)):
        df_values.rename(columns={kk: df_columns[kk]}, inplace=True)

    df_normalized = pd.concat([df_values, df_labels], axis=1)

    return df_normalized


home = '/Users/andrew/Google_Drive/BCI/Data/Profiles/users/akavas'
csv_paths, b = bin_tree(home, 'lab.csv')


frames = df_maker(csv_paths)
df_all = aggregator(frames, csv_paths)


df_all_normalized = normalize(df_all)
print(df_all_normalized)


# TODO: create grapher, correct labeler, finish getter
# TODO: make it all work live (except labeler)
# TODO: make the neural network!

# TODO: 1) figure out how algorithm needs data processed
# TODO: 2) figure out train/test split
# TODO: 3) make option to specify user data or all data
# TODO: 4) apply transformations to live data
# TODO: 5)

