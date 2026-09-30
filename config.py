# Archivo de configuración global para el juego
import os

# Dimensiones de pantalla
ANCHO_PANTALLA = 1000
ALTO_PANTALLA = 600

# Rutas
CARPETA = os.path.split(os.path.abspath(__file__))[0]
ARCHIVOS = os.path.join(CARPETA, 'archivos')

# Colores
COLOR_FONDO = (0, 0, 0)
COLOR_TEXTO = (255, 255, 255)
COLOR_TEXTO_SECUNDARIO = (200, 200, 200)
COLOR_MUERTE = (255, 0, 0)
COLOR_PUNTAJES = (0, 0, 0)
COLOR_PUNTAJES_ERROR = (255, 0, 0)

# Tamaños
TAM_BOTON = (200, 50)
TAM_CORAZON = (40, 40)
TAM_ICONO = (30, 30)
TAM_ESCALERA = (50, 50)

# Otros parámetros
FPS = 60
TOTAL_NIVELES = 5
POSICIONES_INICIALES = {
    1: (50, 400),
    2: (450, 450),
    3: (450, 450),
    4: (450, 450),
    5: (450, 450),
} 