import os
from conexion import Conexion

PUNTAJES_TXT = os.path.join(os.path.dirname(__file__), 'puntajes.txt')


def _guardar_en_txt(jugador, puntos, fecha):
    """Guarda puntajes localmente cuando no hay conexión a MySQL."""
    linea = f"{jugador}: {float(puntos):.2f} segundos - Fecha: {fecha}\n"
    with open(PUNTAJES_TXT, 'a', encoding='utf-8') as archivo:
        archivo.write(linea)


def _leer_desde_txt():
    """Lee puntajes locales y devuelve lista de tuplas (jugador, puntos, fecha)."""
    if not os.path.exists(PUNTAJES_TXT):
        return []

    jugadores = []
    with open(PUNTAJES_TXT, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            try:
                jugador, resto = linea.split(':', 1)
                puntos_txt, fecha_txt = resto.split('segundos - Fecha:', 1)
                puntos = float(puntos_txt.strip())
                fecha = fecha_txt.strip()
                jugadores.append((jugador.strip(), puntos, fecha))
            except (ValueError, IndexError):
                continue

    jugadores.sort(key=lambda x: x[1], reverse=True)
    return jugadores

def nuevo_jugador(jugador, puntos, fecha):
    """Guarda un nuevo jugador y su puntaje en MySQL o en archivo local de respaldo."""
    conexion = Conexion()
    try:
        cursor = conexion.conectar()
        sql = 'INSERT INTO partidas (jugador, puntos, fecha) VALUES (%s, %s, %s);'
        cursor.execute(sql, (jugador, puntos, fecha))
        conexion.commit()
        print("Se grabó correctamente el jugador")
        return True
    except Exception as e:
        conexion.rollback()
        print(f"Error MySQL al guardar puntaje: {e}")
        try:
            _guardar_en_txt(jugador, puntos, fecha)
            print("Puntaje guardado en archivo local de respaldo.")
            return True
        except OSError as file_error:
            print(f"Error al guardar puntaje local: {file_error}")
            return False
    finally:
        conexion.desconectar()

def listar_jugadores():
    """Devuelve una lista de jugadores y sus puntajes desde MySQL o respaldo local."""
    conexion = Conexion()
    try:
        cursor = conexion.conectar()
        sql = """
        SELECT jugador, puntos, fecha
        FROM partidas
        ORDER BY puntos DESC
        """
        cursor.execute(sql)
        jugadores = cursor.fetchall()
        return True, jugadores
    except Exception as e:
        print(f'Error MySQL al listar: {e}')
        jugadores_locales = _leer_desde_txt()
        if jugadores_locales:
            print('Mostrando puntajes desde respaldo local.')
            return True, jugadores_locales
        return True, []
    finally:
        conexion.desconectar()

