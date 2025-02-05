import pygame
from src.graphics.scene import Scene
from src.api import ApiServer
import threading
import queue


class Application:
    def __init__(self):
        # Inicializace scény
        self.scene = Scene()

        # Inicializace fronty pro aktualizace dat
        self.update_queue = queue.Queue()

        # Počáteční testovací data
        self.rect_objects = [
            {
                '<reserved-0>': -0.01,
                'ema': 0.02,
                'ma': 0.03,
                'misu': 0.03,
                'je': 0.03,
                'holka': -0.02,
                'starsi': 0.05,
                'mamy': 0.05,
                'misa': -0.02,
                'mamu': 0.02
            },
            {
                '<reserved-1>': -0.11,
                'ema': 0.12,
                'asd': 0.3,
                'koo': 0.33,
                'je': 0.03
            }
        ]

        # Inicializace API serveru
        self.api_server = ApiServer()
        self.api_server.set_initial_data(self.rect_objects)
        self.api_server.set_update_callback(self.handle_data_update)

    def handle_data_update(self, new_data):
        """Callback pro aktualizaci dat z API"""
        self.update_queue.put(new_data)

    def run(self):
        # Spuštění API serveru
        self.api_server.run_server()

        # Inicializace scény s počátečními daty
        self.scene.create_rectangles_from_list(self.rect_objects)

        # Hlavní smyčka aplikace
        clock = pygame.time.Clock()
        running = True

        while running:
            # Zpracování událostí Pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # Kontrola nových dat
            try:
                while True:  # Zpracujeme všechny aktualizace ve frontě
                    new_data = self.update_queue.get_nowait()
                    self.rect_objects = new_data
                    self.scene.create_rectangles_from_list(new_data)
            except queue.Empty:
                pass  # Žádná nová data k dispozici

            # Aktualizace a vykreslení scény
            self.scene.update()
            self.scene.draw()

            clock.tick(60)

        pygame.quit()


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
