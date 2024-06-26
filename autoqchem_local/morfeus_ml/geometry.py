import numpy as np
from morfeus.data import atomic_symbols, atomic_numbers
# from scipy.spatial.distance import cdist


def convert_to_symbol(elements):
    """ Converts an element vector from number format to str format """
    return np.array(list(map(lambda x: atomic_symbols[x], elements)))


def convert_to_numbers(elements):
    """ Converts an element vector from str format to number format """
    return np.array(list(map(lambda x: atomic_numbers[x], elements)))


def euclid_dist(p1, p2):
    """ 
    Euclidean distance between two points in the x y z dimension 
    :param numpy.ndarray p1: first point coordinates [x, y, z, ...]
    :param numpy.ndarray p2: second point coordinates [x, y, z, ...]
    :return: the Euclidean distance between both points
    """
    # cdist(np.array(p1).reshape(-1, 3), np.array(p2).reshape(-1, 3))
    return np.sqrt(sum(np.square(p1 - p2)))


def get_all_idx(atom, elements):
    """
    Return all indexes of specified atom inside elements
    """

    return [x for x in range(len(elements)) if atom == elements[x]]


def get_first_idx(atom, elements):
    """
    Return the first found element inside elements that matches atom
    """
    idx = get_all_idx(atom, elements)
    if len(idx) > 0:
        idx = idx[0]
    else:
        idx = None
    
    return idx


def get_closest_atom_to_metal(atom, elements, metal_idx, coordinates):
    """
    Return the index of the closest element that matches atom to the metal in metal_idx
    """
    atoms_idx = get_all_idx(atom, elements)
    metal_coords = coordinates[metal_idx]
    dist = [euclid_dist(metal_coords, coordinates[x]) for x in atoms_idx]

    return atoms_idx[np.argmin(dist)]


def get_all_closest_atom_to_metal(atom, elements, metal_idx, coordinates):
    """
    Return the index of the all elements that matches atom to the metal in metal_idx sorted by proximity.
    The first one in the list is the closest and the last one the furthest away.
    """
    atoms_idx = np.array(get_all_idx(atom, elements))
    metal_coords = coordinates[metal_idx]
    dist = [euclid_dist(metal_coords, coordinates[x]) for x in atoms_idx]
    ord_idx = np.argsort(dist)

    return atoms_idx[np.argsort(dist)]


def get_dist_vector(atom_idx, coordinates):
    """
    Return the distance from the atom in the specified index to all the other elements
    """
    atom_coords = coordinates[atom_idx]

    return [euclid_dist(atom_coords, x) for x in coordinates]


def get_central_carbon(elements, coordinates, metal_idx):
    """
    Get the central carbon between a copper and two nitrogens. This will be the closest to the three of them combined.
    """

    # Get all carbon indexes
    carbon_idx = get_all_idx('C', elements)

    # Get all nitrogen indexes
    nitrogen_idx = get_all_idx('N', elements)

    # Calculate carbon distances to the three atoms
    carbon_dist = [euclid_dist(coordinates[idx], coordinates[metal_idx]) +
                   euclid_dist(coordinates[idx], coordinates[nitrogen_idx[0]]) +
                   euclid_dist(coordinates[idx], coordinates[nitrogen_idx[1]]) for idx in carbon_idx]

    # Get the closest carbon
    carbon_min_idx = np.argmin(carbon_dist)

    return carbon_idx[carbon_min_idx]


def get_carbon_single_nitro(elements, coordinates, metal_idx):
    # Get all carbon indexes
    carbon_idx = get_all_idx('C', elements)

    # Get all nitrogen indexes
    nitrogen_idx = get_all_idx('N', elements)

    # Calculate carbon distances to the nitrogen and metal atoms
    carbon_dist = [euclid_dist(coordinates[idx], coordinates[metal_idx]) +
                   euclid_dist(coordinates[idx], coordinates[nitrogen_idx[0]]) for idx in carbon_idx]

    # Get the closest carbon
    carbon_min_idx = np.argmin(carbon_dist)

    return carbon_idx[carbon_min_idx]


def get_three_point_angle(central_p, p1, p2):
    # Derived from the law of cosine, all points are coordinates
    c = euclid_dist(p1, p2)
    a = euclid_dist(central_p, p1)
    b = euclid_dist(central_p, p2)
    cos = (a*a + b*b - c*c) / (2*a*b)

    return np.rad2deg(np.arccos(cos))

