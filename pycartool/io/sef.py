# -*- coding: utf-8 -*-
# Authors: Tanguy Vivier <tanguy.viv@gmail.com>
#          Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)
import struct
import time

import numpy as np
import mne
from mne.io import RawArray
from mne import create_info


def read_sef(path):
    """
    Reads file with format .sef, and returns a mne.io.Raw object containing
    the data.

    Parameters
    ----------
    filename : str
        The filename of the sef file.

    Returns
    -------
    raw : mne.io.RawArray
        RawArray containing the EEG signals.
    """
    f = open(filename, 'rb')
    #   Read fixed part of the headerà
    version = f.read(4).decode('utf-8')
    if version != "SE01":
        priint(f"Version : {version} not supported")
        raise ValueError()
    n_channels,         = struct.unpack('I', f.read(4))
    num_aux_electrodes, = struct.unpack('I', f.read(4))
    num_time_frames,    = struct.unpack('I', f.read(4))
    sfreq,              = struct.unpack('f', f.read(4))
    year,               = struct.unpack('H', f.read(2))
    month,              = struct.unpack('H', f.read(2))
    day,                = struct.unpack('H', f.read(2))
    hour,               = struct.unpack('H', f.read(2))
    minute,             = struct.unpack('H', f.read(2))
    second,             = struct.unpack('H', f.read(2))
    millisecond,        = struct.unpack('H', f.read(2))

    #   Read variable part of the header
    ch_names = []
    for _ in range(n_channels):
        name = [char for char in f.read(8).split(b'\x00')
                if char != b''][0]
        ch_names.append(name.decode('utf-8'))
    # Read data
    buffer = np.frombuffer(
        f.read(n_channels * num_time_frames * 8),
        dtype=np.float32,
        count=n_channels * num_time_frames)
    data = np.reshape(buffer, (num_time_frames, n_channels))
    # Create infos
    description = "Imported from Pycartool"
    record_time = time.struct_time(tm_year=year, tm_mon=month, tm_mday=day,
                                   tm_hour=hour, tm_min=minute, tm_sec=second,
                                   tm_isdst=-1)
    meas_date = (time.mktime(record_time), millisecond)
    ch_types = ['eeg' for i in range(n_channels)]
    infos = create_info(ch_names=ch_names, sfreq=sfreq,
                        description=description, ch_types=ch_types,
                        meas_date=meas_date)
    raw = RawArray(np.transpose(data), infos)
    return (raw)


def write_sef(filename, raw):
    """Export a raw mne file to a sef file.

    Parameters
    ----------
    filename : str
        Filename of the exported dataset.
    raw : instance of mne.io.Raw
        The raw data to export.
    """
    n_channels = len(raw.info['ch_names'])
    num_freq_frames = raw.n_times
    info = raw.info
    sfreq = info['sfreq']
    num_aux_electrodes = n_channels - len(mne.pick_types(info, meg=False,
                                                         eeg=True,
                                                         exclude=[""]))
    f = open(filename, 'wb')
    f.write("SE01".encode('utf-8'))
    f.write(struct.pack('I', n_channels))
    f.write(struct.pack('I', num_aux_electrodes))
    f.write(struct.pack('I', num_freq_frames))
    f.write(struct.pack('f', sfreq))
    f.write(struct.pack('H', 0))
    f.write(struct.pack('H', 0))
    f.write(struct.pack('H', 0))
    f.write(struct.pack('H', 0))
    f.write(struct.pack('H', 0))
    f.write(struct.pack('H', 0))
    f.write(struct.pack('H', 0))

    ch_names = info["ch_names"]
    for k in range(n_channels):
        ch_name = ch_names[k]
        ch_name = ch_name.ljust(8)
        f.write(ch_name.encode('utf-8'))

    data = raw.get_data().astype(np.float32)
    data = np.reshape(data, n_channels * num_freq_frames, order='F')
    data.tofile(f)
    f.close()
