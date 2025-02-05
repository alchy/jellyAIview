import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
from ..config import (
    DISPLAY_WIDTH, DISPLAY_HEIGHT,
    RECT_HEIGHT, RECT_WIDTH, RECT_SPACING_Y, RECT_SPACING_X, RECT_START_Z,
    CENTER_LINE_COLOR, CENTER_LINE_LENGTH, CENTRAL_GAP
)
from ..objects.rectangle import Rectangle
from ..utils.math_helpers import calculate_bounding_box, calculate_scene_center_and_size
from .camera import Camera


class Scene:
    def __init__(self):
        """Inicializace scény."""
        pygame.init()
        glutInit()
        self.display_size = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
        pygame.display.set_mode(self.display_size, pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption("Data Visualization")

        glEnable(GL_DEPTH_TEST)
        self.rectangles = []
        self.camera = Camera(self.display_size)
        self.scene_bounds = None
        self.running = True

        # Nastavení pro ovládání kamery
        self.camera_speed = 0.5  # Rychlost pohybu kamery
        self.zoom_speed = 1.0  # Rychlost zoomu
        self.auto_camera = True  # Přepínač pro automatické sledování scény

    def create_rectangles_from_list(self, data_list):
        """Vytvoří sloupce obdélníků z dodaného seznamu slovníků."""
        self.rectangles = []

        total_columns = len(data_list)
        total_width = (total_columns - 1) * RECT_SPACING_X
        start_x = -total_width / 2

        for column_index, data_dict in enumerate(data_list):
            x_pos = start_x + (column_index * RECT_SPACING_X)

            # Rozdělení a seřazení položek
            positive_items = dict(sorted(
                [(k, v) for k, v in data_dict.items() if v >= 0],
                key=lambda x: x[1],
                reverse=True
            ))
            negative_items = dict(sorted(
                [(k, v) for k, v in data_dict.items() if v < 0],
                key=lambda x: x[1]
            ))

            # Výpočet pozic pro kladné hodnoty
            for i, (key, value) in enumerate(positive_items.items()):
                # Začínáme od CENTRAL_GAP a přidáváme RECT_SPACING_Y mezi každým obdélníkem
                y_pos = CENTRAL_GAP + (i * (RECT_SPACING_Y + RECT_HEIGHT))
                position = [x_pos, y_pos, RECT_START_Z]
                rect = Rectangle(key, value, position, (RECT_WIDTH, RECT_HEIGHT))
                self.rectangles.append(rect)

            # Výpočet pozic pro záporné hodnoty
            for i, (key, value) in enumerate(negative_items.items()):
                # Začínáme od -CENTRAL_GAP a odečítáme RECT_SPACING_Y + výška mezi každým obdélníkem
                y_pos = -(CENTRAL_GAP + (i * (RECT_SPACING_Y + RECT_HEIGHT)))
                position = [x_pos, y_pos, RECT_START_Z]
                rect = Rectangle(key, value, position, (RECT_WIDTH, RECT_HEIGHT))
                self.rectangles.append(rect)

    def draw_center_line(self):
        """Vykreslí centrální osu přes celou šířku scény."""
        if self.scene_bounds is None:
            return

        min_pos, max_pos = self.scene_bounds
        glPushMatrix()
        glLoadIdentity()

        # Aplikace transformací kamery
        glTranslatef(self.camera.position[0], self.camera.position[1], self.camera.position[2])

        # Nastavení barvy pro centrální osu
        glColor3f(*CENTER_LINE_COLOR)

        # Vykreslení centrální osy
        glBegin(GL_LINES)
        extra_length = CENTER_LINE_LENGTH
        glVertex3f(min_pos[0] - extra_length, 0, RECT_START_Z)
        glVertex3f(max_pos[0] + extra_length, 0, RECT_START_Z)
        glEnd()

        glPopMatrix()

    def update_camera(self):
        """Aktualizuje kameru podle pozic objektů."""
        if not self.rectangles:
            return

        positions = [rect.position for rect in self.rectangles]
        min_pos, max_pos = calculate_bounding_box(positions)
        self.scene_bounds = (min_pos, max_pos)
        center, size = calculate_scene_center_and_size(min_pos, max_pos)
        self.camera.update(center, size)

    def handle_events(self):
        """Zpracování událostí.
        Returns:
            bool: False pokud má aplikace skončit, jinak True
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    # Přepínání mezi automatickým a manuálním ovládáním kamery
                    self.auto_camera = not self.auto_camera
                    print("Camera mode:", "Auto" if self.auto_camera else "Manual")

        # Zpracování vstupů pro kameru
        self.handle_camera_input()
        return True

    def handle_camera_input(self):
        """Zpracování vstupu pro ovládání kamery"""
        keys = pygame.key.get_pressed()

        # Pohyb kamery pouze když není aktivní automatické sledování
        if not self.auto_camera:
            if keys[pygame.K_a]:  # Vlevo
                self.camera.position[0] -= self.camera_speed
            if keys[pygame.K_d]:  # Vpravo
                self.camera.position[0] += self.camera_speed
            if keys[pygame.K_w]:  # Přiblížení
                self.camera.position[2] += self.zoom_speed
            if keys[pygame.K_s]:  # Oddálení
                self.camera.position[2] -= self.zoom_speed

    def update(self):
        """Aktualizace scény."""
        # Automatická aktualizace kamery pouze když je aktivní
        if self.auto_camera:
            self.update_camera()

    def draw(self):
        """Vykreslení scény."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Aplikace transformací kamery
        glLoadIdentity()
        glTranslatef(self.camera.position[0], self.camera.position[1], self.camera.position[2])

        # Vykreslení středové osy
        self.draw_center_line()

        # Vykreslení všech obdélníků
        for rect in self.rectangles:
            rect.draw()

        pygame.display.flip()

    def run(self):
        """Hlavní smyčka aplikace."""
        clock = pygame.time.Clock()

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)

        self.cleanup()

    def cleanup(self):
        """Úklid a ukončení."""
        pygame.quit()