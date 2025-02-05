import numpy as np

def calculate_bounding_box(positions):
    """Vypočítá minimální a maximální pozice pro seznam bodů."""
    positions_array = np.array(positions)
    min_pos = np.min(positions_array, axis=0)
    max_pos = np.max(positions_array, axis=0)
    return min_pos, max_pos

def calculate_scene_center_and_size(min_pos, max_pos):
    """Vypočítá střed a velikost scény z hranic."""
    center = (min_pos + max_pos) / 2.0
    size = np.abs(max_pos - min_pos)  # Velikost v každé dimenzi
    max_size = np.max(size)  # Největší rozměr scény
    return center, max_size  # Vracíme center jako np.array a max_size jako skalár