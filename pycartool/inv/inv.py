# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)
import struct

import numpy as np

from ..utils._docs import fill_doc
from ..utils._logs import logger, verbose

@fill_doc
@verbose
def read_is(filename, verbose=None):
    """Read Cartool inverse solution (``.is``) file.

    Parameters
    ----------
    filename : str or file-like
        Path to the inverse solution file ``(.is``) to read.

    Returns
    -------
    inverse_solution : `~numpy.array`
        Inverse solution matrices. n_dim=1 if solutions are scalar or
        n_dim=3 for vectorial solutions.
        shape(``n_regularizations``, ``n_dim``, ``n_solutionpoints``, ``n_channels``). # noqa
    """
    with open(filename, "rb") as f:
        logger.info(f"Reading {filename}")
        logger.info(f"Reading Header...")
        is_type = [
            struct.unpack("c", f.read(1))[0].decode("utf-8") for i in range(4)
        ]
        is_type = "".join(is_type)
        if is_type not in ["IS01", "IS02", "IS03"]:
            raise ValueError(
                f"{is_type} : Invalid IS type, please check that "
                "input file is a Inverse Solution matrix"
            )
        logger.info(f"IS type: {is_type}")
        n_channels = struct.unpack("I", f.read(4))[0]
        logger.info(f"n_channels: {n_channels}")
        numsolutionpoints = struct.unpack("I", f.read(4))[0]
        logger.info(f"n_solutionpoints: {numsolutionpoints}")
        numregularizations = struct.unpack("I", f.read(4))[0]
        logger.info(f"n_regularizations: {numregularizations}")
        isinversescalar = struct.unpack("c", f.read(1))[0]
        if isinversescalar == b"\x01":
            n_dim = 1
            logger.info(f"Inverse solution is Scalar")
        elif isinversescalar == b"\x00":
            logger.info(f"Inverse solution is Vectorial")
            n_dim = 3
        else:
            raise ValueError(
                f"isinversescalar must be either 1 for scalar, "
                f"either 0 for vectorial, but "
                f"{ord(isinversescalar)} found."
            )

        if is_type in ["IS01", "IS02"]:
            buf = f.read(n_dim * numsolutionpoints * n_channels * 4)
            data = np.frombuffer(buf, dtype=np.float32)
            data = data.reshape(numsolutionpoints, n_dim, n_channels)
            data = np.array([data])
            data = np.swapaxes(data, 1, 2)

        elif is_type == "IS03":
            logger.info(f"Reading Variable Header...")

            ch_names = []
            for _ in range(n_channels):
                name = [
                    char for char in f.read(32).split(b"\x00") if char != b""
                ][0]
                ch_names.append(name.decode("utf-8"))

            solutionpoints_names = []
            for _ in range(numsolutionpoints):
                name = [
                    char for char in f.read(16).split(b"\x00") if char != b""
                ][0]
                solutionpoints_names.append(name.decode("utf-8"))

            regularizations_values = []
            for _ in range(numregularizations):
                value = struct.unpack("d", f.read(8))[0]
                regularizations_values.append(value)
            logger.info(f"Regularizations values: {regularizations_values}")

            regularizations_names = []
            for _ in range(numregularizations):
                name = [
                    char for char in f.read(32).split(b"\x00") if char != b""
                ][0]
                regularizations_names.append(name.decode("utf-8"))
            logger.info(f"Regularizations names: {regularizations_names}")

            regularisation_solutions = []
            buf = f.read(
                numregularizations * n_dim * numsolutionpoints * n_channels * 4
            )
            data = np.frombuffer(buf, dtype=np.float32)
            data = data.reshape(
                numregularizations, numsolutionpoints, n_dim, n_channels
            )
            data = np.swapaxes(data, 1, 2)

    regularisation_solutions = np.array(regularisation_solutions)
    inverse_solution = {
        "is_type": is_type,
        "is_scalar": True if isinversescalar == "0" else False,
        "ch_names": ch_names,
        "solutionpoints_names": solutionpoints_names,
        "regularizations_values": regularizations_values,
        "regularizations_names": regularizations_names,
        "regularisation_solutions": data,
    }
    return inverse_solution
