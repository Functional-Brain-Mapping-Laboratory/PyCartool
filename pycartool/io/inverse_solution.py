# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)
import struct
import numpy as np


def read_is(filename):
    """Read Cartool inverse solution (.is) file.

    Parameters
    ----------
    filename : str
        the is file to read.

    Returns
    -------
    ndarray, shape (n_regularizations, n_dim, n_solutionpoints, n_channels)
        the inverse solution matrices. n_dim=1 if solutions are scalar or
        n_dim=3 for vectorial solutions.

    """
    with open(filename, "rb") as f:
        print(f"Reading {filename}")
        print(f"Reading Header...")
        is_type = [struct.unpack('c', f.read(1))[0].decode("utf-8")
                   for i in range(4)]
        is_type = ''.join(is_type)
        if is_type not in ["IS01", "IS02", "IS03"]:
            print(f"{is_type} : Invalid IS type, please check that "
                  "input file is a Inverse Solution matrix")
            raise ValueError
        print(f"IS type: {is_type}")
        n_channels = struct.unpack('I', f.read(4))[0]
        print(f"n_channels: {n_channels}")
        numsolutionpoints = struct.unpack('I', f.read(4))[0]
        print(f"n_solutionpoints: {numsolutionpoints}")
        numregularizations = struct.unpack('I', f.read(4))[0]
        print(f"n_regularizations: {numregularizations}")
        isinversescalar = struct.unpack('c', f.read(1))[0]
        if isinversescalar == "0":
            n_dim = 1
            print(f"Inverse solution is Scalar")
        else:
            print(f"Inverse solution is Vectorial")
            n_dim = 3

        if is_type in ["IS01", "IS02"]:
            buf = f.read(n_dim * numsolutionpoints * n_channel * 4)
            data = np.frombuffer(buf, dtype=np.float32)
            data = data.reshape(ndim, numsolutionpoints, n_channel)
            data = no.array([data])

        elif is_type == "IS03":
            print(f"Reading Variable Header...")

            ch_names = []
            for _ in range(n_channels):
                name = [char for char in f.read(32).split(b'\x00')
                        if char != b''][0]
                ch_names.append(name.decode('utf-8'))

            solutionpoints_names = []
            for _ in range(numsolutionpoints):
                name = [char for char in f.read(16).split(b'\x00')
                        if char != b''][0]
                solutionpoints_names.append(name.decode('utf-8'))

            regularizations_values = []
            for _ in range(numregularizations):
                value = struct.unpack('d', f.read(8))[0]
                regularizations_values.append(value)
            print(f"Regularizations values: {regularizations_values}")

            regularizations_names = []
            for _ in range(numregularizations):
                name = [char for char in f.read(32).split(b'\x00')
                        if char != b''][0]
                regularizations_names.append(name.decode('utf-8'))
            print(f"Regularizations names: {regularizations_names}")

            regularisation_solutions = []
            buf = f.read(numregularizations * n_dim * numsolutionpoints * n_channels * 4)
            data = np.frombuffer(buf, dtype=np.float32)
            data = data.reshape(numregularizations, n_dim, numsolutionpoints, n_channels)

    regularisation_solutions = np.array(regularisation_solutions)
    inverse_solution = {"is_type": is_type,
                        "is_scalar": True if isinversescalar == "0" else False,
                        "ch_names": ch_names,
                        "solutionpoints_names": solutionpoints_names,
                        "regularizations_values": regularizations_values,
                        "regularizations_names": regularizations_names,
                        "regularisation_solutions": data}
    return(inverse_solution)


def read_ris(filename):
    with open(filename, "rb") as f:
        print(f"Reading {filename}")
        print(f"Reading Header...")
        ris_type = [struct.unpack('c', f.read(1))[0].decode("utf-8")
                    for i in range(4)]
        ris_type = ''.join(ris_type)
        if ris_type not in ["RI01"]:
            raise ValueError(f"{ris_type} : Invalid RI type, please check that"
                             f" input file is a Result of Inverse Solution "
                             f" computation")
        print(f"IS type: {ris_type}")
        n_solutionpoints = struct.unpack('I', f.read(4))[0]
        print(f"n_solutionpoints: {n_solutionpoints}")
        n_timeframes = struct.unpack('I', f.read(4))[0]
        print(f"n_timeframes: {n_timeframes}")
        s_freq = struct.unpack('f', f.read(4))[0]
        print(f"Samplimg frequency: {s_freq}")
        isinversescalar = struct.unpack('c', f.read(1))[0]
        if isinversescalar == "0":
            n_dim = 1
            print(f"Result of Inverse Solution computation is Scalar")
        else:
            print(f"Result of Inverse Solution computation is Vectorial")
            n_dim = 3

        buf = f.read(n_dim * n_solutionpoints * n_timeframes * 4)
        data = np.frombuffer(buf, dtype=np.float32)
        data = data.reshape(n_timeframes, n_dim, n_solutionpoints)
        results_of_is = {"ris_type": ris_type,
                         "is_scalar": True if isinversescalar == "0" else False,
                         "s_freq": s_freq,
                         "regularisation_solutions": data}
        return(results_of_is)
