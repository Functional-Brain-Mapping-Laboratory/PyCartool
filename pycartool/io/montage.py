# -*- coding: utf-8 -*-
# Authors: Tanguy Vivier <tanguy.viv@gmail.com>
#          Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)

from mne.channels import Montage
import numpy as np


def read_xyz(filename, kind=''):
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
    coord = np.loadtxt(filename, skiprows=1, usecols=(0, 1, 2), max_rows=n)
    names = np.loadtxt(filename, skiprows=1, usecols=3, max_rows=n,
                       dtype=np.dtype(str))
    names = names.tolist()
    montage = Montage(coord, names, kind,
                      selection=[i for i in range(n)])
    return(montage)
