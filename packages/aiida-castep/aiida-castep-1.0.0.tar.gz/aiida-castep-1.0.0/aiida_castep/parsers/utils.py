"""
Utility functions
"""
from __future__ import absolute_import
import numpy as np
from aiida.common import OutputParsingError
from six.moves import zip


class CASTEPOutputParsingError(OutputParsingError):
    pass


def structure_from_input(cell, positions, symbols):
    """
    Receives the dictionary cell parsed from CASTEP
    Convert it into an AiiDA structure object
    """

    from aiida.plugins import DataFactory
    SructureData = DataFactory("structure")

    out_structure = SructureData(cell=cell)

    for symbol, position in zip(symbols, positions):

        out_structure.append_atom(symbols=symbol, position=position)

    return out_structure


def add_last_if_exists(dict_of_sequence, key, dict_to_be_added):
    """
    Added the last term of a sequence to a dictionary.
    This is used for collecting final values in a dictionary of 'trajectory'
    """

    try:
        last = dict_of_sequence[key][-1]
    except (KeyError, IndexError):
        return
    else:
        # Check if last exist - in case of DefaultDict being passed
        if last:
            dict_to_be_added[key] = last


def desort_structure(structure, original_structure):
    """
    Recover the order of structure. CASTEP will sort the input structure
    according to the atomic numbers
    """
    import copy
    new_structure = copy.deepcopy(structure)

    rsort = get_desort_args(original_structure)
    new_sites = np.array(structure.sites)[rsort]

    # Map back to the original order
    new_structure.clear_sites()
    for s in new_sites:
        new_structure.append_site(s)

    # Check for sure
    assert [s.kind_name for s in original_structure.sites
            ] == [s.kind_name for s in new_structure.sites]

    return new_structure


def get_desort_args(original_structure):
    """
    Return an index array for desorting the structure

    :return: An array used to recovery the original order
    """
    numbers = original_structure.get_ase().numbers
    isort = np.argsort(numbers, kind='mergesort')
    rsort = [-1] * len(numbers)
    for i, s in enumerate(isort):
        rsort[s] = i
    assert -1 not in rsort

    return rsort
