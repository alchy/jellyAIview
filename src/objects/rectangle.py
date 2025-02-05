from OpenGL.GL import *
import numpy as np
from ..config import TEXT_SCALE
from .text import draw_text


class Rectangle:
    def __init__(self, key, value, position=(0, 0, 0), size=(3.0, 0.5)):
        self.key = key
        self.value = value
        self.text = f"{key} : {value}"
        self.position = list(position)
        self.size = size

    def draw(self):
        glPushMatrix()

        # Přesun na pozici objektu
        glTranslatef(*self.position)

        # Billboard efekt
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        modelview[0:3, 0:3] = np.identity(3)
        glLoadMatrixd(modelview.flatten())

        # Vykreslení obdélníku
        self._draw_wireframe()

        # Vykreslení textu
        self._draw_text()

        glPopMatrix()

    def _draw_wireframe(self):
        # Barva podle hodnoty
        if self.value < 0:
            glColor3f(1, 0, 0)  # červená pro záporné
        else:
            glColor3f(0, 1, 0)  # zelená pro kladné

        half_width = self.size[0] / 2
        half_height = self.size[1] / 2

        # Vykreslení obdélníku
        glBegin(GL_LINE_LOOP)
        glVertex3f(-half_width, -half_height, 0)
        glVertex3f(half_width, -half_height, 0)
        glVertex3f(half_width, half_height, 0)
        glVertex3f(-half_width, half_height, 0)
        glEnd()

    def _draw_text(self):
        glPushMatrix()
        glColor3f(1, 1, 1)  # bílý text
        glScalef(TEXT_SCALE, TEXT_SCALE, TEXT_SCALE)
        draw_text(self.text, centered=True)
        glPopMatrix()