
import numpy as np

from ..io import read_sef
from ..io import read_is


def compute_sources_tc(is_filename, sef_filename, regularizations_names=None):
    print("Reading inverse solution...")
    inverse_solution = read_is(is_filename)
    print("Reading EEG...")
    eeg = read_sef(sef_filename)
    # Check that electrodes match betweens eeg and inverse_solution
    if eeg.info["ch_names"] != inverse_solution["ch_names"]:
        raise ValueError("EEG and Inverse solution channels names do not match")
    else:
        print("EEG and Inverse solution channels names match")

    if regularizations_names is not None:
        regularizations_indices = []
        if not isinstance(regularizations_names, list()):
            raise TypeError(f"regularizations_names must be a list, but "
                            f"type {type(regularizations_names)} were found")
        for reg_name in regularizations_names:
            if reg_name not in inverse_solution["regularizations_names"]:
                raise TypeError(f"{reg_name} not found in inverse solution")
            else:
                reg_indice = np.where(inverse_solution["regularizations_names"] == reg_name)
                regularizations_indices.append(reg_indice)
        inverse_matrix = inverse_solution["regularisation_solutions"][regularizations_indices]
    else:
        inverse_matrix = inverse_solution["regularisation_solutions"]

    sources_tc = np.dot(inverse_matrix, eeg.get_data())
    return(sources_tc)
