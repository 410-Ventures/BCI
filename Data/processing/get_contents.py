
import os, sys
import timeit
import numpy as np
import pandas as pd


import os, sys
import timeit
import numpy as np
import pandas as pd


def find_contents(path_dir, suffix):
    names = os.listdir(path_dir)
    return np.array([filename for filename in names if filename.endswith(suffix) and not filename.endswith('.ini')
                     and not filename.endsWith('.DS_Store')])






