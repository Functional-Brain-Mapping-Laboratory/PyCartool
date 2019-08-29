# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)
import struct
import numpy as np


def read_is(fname):
    with open(fname,"rb") as f:
        print(f"Reading {fname}")
        print(f"Reading Header...")
        iso = ''.join([struct.unpack('c', f.read(1))[0].decode("utf-8") for i in range(4)])
        if iso not in ["IS01", "IS02", "IS03"]:
            print(f"{iso} : Invalid ISO type, please check that input file is "
                  "a Inverse Solution matrix")
            raise ValueError
        print(f"ISO: {iso}")
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

        if iso in ["IS01", "IS02"]:
            regularisation_solutions = []
            buf = f.read(n_dim * numsolutionpoints * n_channel * 4)
            data = np.frombuffer(buf, dtype=np.float32)
            data = data.reshape(numsolutionpoints, ndim, n_channels)
            regularisation_solutions.append(data)

        elif iso == "IS03":
            print(f"Reading Variable Header...")

            ch_names = []
            for k in range(n_channels):
                name = [char for char in f.read(32).split(b'\x00')
                        if char != b''][0]
                ch_names.append(name.decode('utf-8'))

            solutionpoints_names = []
            for k in range(numsolutionpoints):
                name = [char for char in f.read(16).split(b'\x00')
                        if char != b''][0]
                solutionpoints_names.append(name.decode('utf-8'))

            regularizations_values = []
            for k in range(numregularizations):
                value = struct.unpack('d', f.read(8))[0]
                regularizations_values.append(value)
            print(f"Regularizations values: {regularizations_values}")

            regularizations_names = []
            for k in range(numregularizations):
                name = [char for char in f.read(32).split(b'\x00')
                        if char != b''][0]
                regularizations_names.append(name.decode('utf-8'))
            print(f"Regularizations names: {regularizations_names}")

            regularisation_solutions = []
            for k in range(0, numregularizations):
                buf = f.read(n_dim * numsolutionpoints * n_channels * 4)
                data = np.frombuffer(buf, dtype=np.float32)
                data = data.reshape(n_dim, numsolutionpoints, n_channels)
                regularisation_solutions.append(data)

    return(np.array(regularisation_solutions))

a = read_is(r"C:\Users\Victor Ferat\Desktop\MNI_LA_204.Laura.is")
print(a.shape)
