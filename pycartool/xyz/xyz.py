# -*- coding: utf-8 -*-
# Authors: Tanguy Vivier <tanguy.viv@gmail.com>
#          Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)

import numpy as np
from mne.channels import make_dig_montage


def read_xyz(filename):
    """Read and convert xyz positions to a mne montage type.

    Parameters
    ----------
    filename : str
        The filename of the xyz file.

    Returns
    -------
    montage : `~mne.channels.DigMontage`
        Montage for EEG electrode locations.
    """
    n = int(open(filename).readline().lstrip().split(" ")[0])
    coord = (
        np.loadtxt(filename, skiprows=1, usecols=(0, 1, 2), max_rows=n) / 1e3
    )
    names = np.loadtxt(
        filename, skiprows=1, usecols=3, max_rows=n, dtype=np.dtype(str)
    )
    names = names.tolist()
    ch_pos = dict()
    for i, name in enumerate(names):
        ch_pos[name] = coord[i] / 1000
    montage = make_dig_montage(ch_pos=ch_pos, coord_frame="head")
    return montage


def write_xyz(filename, info):
    """Export channels coordinates from raw.info to a xyz file.

    Parameters
    ----------
    filename : str or file-like
        Filename of the xyz file .
    info : mne.Info
        The info object use to extract the montage.
    """
    pos = np.array([e["loc"][:3] for e in info["chs"]]).reshape(-1, 3) * 1e3
    names = info["ch_names"]
    n = len(names)
    with open(filename, "w") as f:
        f.write(str(n) + "    " + str(np.max(np.mean(pos, axis=1))) + "\n")
        for e, elec in enumerate(names):
            f.write(
                "{0:<16}    {1:<16}    {2:<16}    {3:<25}\n".format(
                    pos[e][0], pos[e][1], pos[e][2], elec
                )
            )
