import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from ..config import FOV_Y, NEAR_PLANE, FAR_PLANE


class Camera:
    def __init__(self, display_size):
        self.display_size = display_size
        self.position = [0.0, 0.0, -20.0]  # Výchozí pozice kamery
        self.movement_speed = 0.5  # Rychlost pohybu kamery
        self.zoom_speed = 1.0  # Rychlost zoomu

        # Nastavení projekce
        self.aspect_ratio = display_size[0] / display_size[1]
        self.setup_projection()

    def setup_projection(self):
        """Nastaví projekční matici"""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(FOV_Y, self.aspect_ratio, NEAR_PLANE, FAR_PLANE)
        glMatrixMode(GL_MODELVIEW)

    def update(self, center=None, size=None):
        """Aktualizuje pohled kamery"""
        glLoadIdentity()

        # Aplikace pozice kamery
        glTranslatef(self.position[0], self.position[1], self.position[2])

        if center is not None and size is not None:
            # Automatické přizpůsobení pohledu na všechny objekty
            # Převedeme size na float
            if isinstance(size, (np.ndarray, list, tuple)):
                max_size = float(np.max(size))
            else:
                max_size = float(size)  # Pokud je size už skalár

            scale = 15.0 / max_size if max_size > 0 else 1.0
            glScalef(scale, scale, scale)

            # Převedeme center na seznam floatů
            if isinstance(center, np.ndarray):
                center = center.tolist()
            glTranslatef(-center[0], -center[1], -center[2])