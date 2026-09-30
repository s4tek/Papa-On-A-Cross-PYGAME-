import datetime
from modelo import nuevo_jugador
import config

class TiempoPuntaje:
    """Clase para gestionar el tiempo y puntaje del jugador."""
    def __init__(self):
        self.tiempo_inicio = None
        self.tiempo_final = None

    def iniciar_tiempo(self):
        """Registra el tiempo de inicio del juego."""
        self.tiempo_inicio = datetime.datetime.now()

    def finalizar_tiempo(self):
        """Registra el tiempo de finalización del juego."""
        self.tiempo_final = datetime.datetime.now()

    def calcular_puntaje(self):
        """Calcula el tiempo transcurrido en segundos."""
        if self.tiempo_inicio and self.tiempo_final:
            diferencia = self.tiempo_final - self.tiempo_inicio
            return int(diferencia.total_seconds())
        return 0

    def guardar_puntaje(self, jugador):
        """
        Guarda el jugador con su puntaje (tiempo transcurrido) en la base de datos.
        """
        puntaje = self.calcular_puntaje()
        fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if nuevo_jugador(jugador, puntaje, fecha):
            print(f"Jugador {jugador} guardado con {puntaje} segundos de puntaje.")
        else:
            print("Error al guardar el puntaje.")
