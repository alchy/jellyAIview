from OpenGL.GL import *
from OpenGL.GLUT import *



def calculate_text_width(text):
    """Vypočítá šířku textu v GLUT jednotkách."""
    return sum(glutStrokeWidth(GLUT_STROKE_ROMAN, ord(c)) for c in text)


def get_text_height():
    """Vrátí výšku textu v GLUT jednotkách."""
    return glutStrokeHeight(GLUT_STROKE_ROMAN)


def draw_text(text, centered=True):
    """Vykreslí text, volitelně vycentrovaný."""
    if centered:
        text_width = calculate_text_width(text)
        glTranslatef(-text_width / 2, -get_text_height() / 4, 0)

    for c in text:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
