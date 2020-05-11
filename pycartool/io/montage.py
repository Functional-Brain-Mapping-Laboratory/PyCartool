# -*- coding: utf-8 -*-
# Authors: Tanguy Vivier <tanguy.viv@gmail.com>
#          Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)

from mne.channels import make_dig_montage
import numpy as np

def read_xyz(filename):
    """Reads and convert xyz positions to a mne montage type

    Parameters
    ----------
    filename : str
        The filename of the xyz file.
    Returns
    -------
    montage : mne.channels.montage.Montage
        Montage for EEG electrode locations.
    """

    n = int(open(filename).readline().lstrip().split(' ')[0])
    coord = np.loadtxt(filename, skiprows=1, usecols=(0, 1, 2), max_rows=n) / 1e3
    print(coord)
    names = np.loadtxt(filename, skiprows=1, usecols=3, max_rows=n,
                       dtype=np.dtype(str))
    names = names.tolist()
    ch_pos = dict()
    for i, name in enumerate(names):
        ch_pos[name] = coord[i]
    montage = make_dig_montage(ch_pos=ch_pos, coord_frame='head')
    return montage
