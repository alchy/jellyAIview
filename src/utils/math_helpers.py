import numpy as np

def calculate_bounding_box(positions):
    """Vypočítá boundingbox pro seznam pozic."""
    if not positions:
        return None, None
    positions_array = np.array(positions)
    min_pos = np.min(positions_array, axis=0)
    max_pos = np.max(positions_array, axis=0)
    return min_pos, max_pos

def calculate_scene_center_and_size(min_pos, max_pos):
    """Vypočítá střed a velikost scény."""
    center = (min_pos + max_pos) / 2
    size = np.max(max_pos - min_pos)
    return center, size
