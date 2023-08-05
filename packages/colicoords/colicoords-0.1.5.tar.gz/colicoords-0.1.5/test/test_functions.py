from colicoords.data_models import Data
from colicoords.config import cfg
from colicoords.fileIO import load_thunderstorm
import tifffile
import numpy as np
import os


def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


def load_data(dataset):
    dclasses = ['binary', 'brightfield', 'fluorescence']
    f_path = os.path.dirname(os.path.realpath(__file__))
    data = Data()
    for dclass in dclasses:
        files = sorted(listdir_fullpath(os.path.join(f_path, 'test_data', dataset, dclass.lower())), key=str)
        arr = np.empty((len(files), 512, 512)).astype('uint16')
        for i, f in enumerate(files):
            arr[i] = tifffile.imread(f)
        data.add_data(arr, dclass)

    return data


def load_stormdata():
    f_path = os.path.dirname(os.path.realpath(__file__))
    binary = tifffile.imread(os.path.join(f_path, r'test_data/ds2/binary_resized.tif')).astype('int')

    dtype = {
        'names': ("id", "frame", "x", "y", "sigma", "intensity", "offset", "bkgstd", "chi2", "uncertainty_xy"),
        'formats': (int, int, float, float, float, float, float, float, float, float)
    }

    storm_table = np.genfromtxt(os.path.join(f_path, r'test_data/ds2/storm_table.csv'), skip_header=1, dtype=dtype, delimiter=',')
    storm_table['x'] /= cfg.IMG_PIXELSIZE
    storm_table['y'] /= cfg.IMG_PIXELSIZE

    data = Data()
    data.add_data(binary, 'binary')
    data.add_data(storm_table, 'storm')

    return data


def load_escvdata():
    binary = tifffile.imread(r'test_data/ds5/binary.tif')
    flu = tifffile.imread(r'test_data/ds5/flu.tif')
    storm = load_thunderstorm(r'test_data/ds5/storm_table.csv')

    data = Data()
    data.add_data(binary, 'binary')
    data.add_data(flu, 'fluorescence')
    data.add_data(storm, 'storm')

    return data

def load_testdata(dataset):
    return load_data(dataset)
