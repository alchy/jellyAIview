from OpenGL.GL import *  # Přidán import OpenGL.GL
from OpenGL.GLU import *
import numpy as np
from ..config import FOV_Y, NEAR_PLANE, FAR_PLANE


class Camera:
    def __init__(self, display_size):
        self.display_size = display_size

    def update(self, scene_center, scene_size):
        """Aktualizuje pozici a nastavení kamery."""
        aspect_ratio = self.display_size[0] / self.display_size[1]

        # Výpočet vzdálenosti kamery
        distance = self._calculate_camera_distance(scene_size)

        # Nastavení projekce
        self._set_projection(aspect_ratio, distance)

        # Nastavení pohledu kamery
        self._set_camera_view(scene_center, distance)

    def _calculate_camera_distance(self, scene_size):
        """Vypočítá optimální vzdálenost kamery."""
        return (scene_size / (2.0 * np.tan(np.radians(FOV_Y / 2.0)))) * 1.5

    def _set_projection(self, aspect_ratio, distance):
        """Nastaví projekční matici."""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(FOV_Y, aspect_ratio, NEAR_PLANE, distance * 4)
        glMatrixMode(GL_MODELVIEW)

    def _set_camera_view(self, center, distance):
        """Nastaví pohled kamery."""
        glLoadIdentity()
        gluLookAt(
            center[0], center[1], center[2] + distance,  # pozice kamery
            center[0], center[1], center[2],  # cíl
            0, 1, 0  # up vektor
        )