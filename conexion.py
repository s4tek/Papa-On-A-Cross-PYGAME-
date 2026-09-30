import os
import mysql.connector
from mysql.connector import Error

class Conexion:
    """Clase para gestionar la conexión a la base de datos MySQL."""
    def __init__(self):
        self.conexion = None
        self.cursor = None

    def conectar(self):
        """Establece la conexión y devuelve el cursor."""
        host = os.getenv('DB_HOST', '127.0.0.1')
        user = os.getenv('DB_USER', 'root')
        password = os.getenv('DB_PASSWORD')
        database = os.getenv('DB_NAME', 'papa_juego')

        if not password:
            raise ValueError('Falta la variable de entorno DB_PASSWORD para conectarse a MySQL.')

        self.conexion = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            db=database,
        )
        self.cursor = self.conexion.cursor()
        return self.cursor

    def commit(self):
        """Confirma la transacción activa."""
        if self.conexion and self.conexion.is_connected():
            self.conexion.commit()

    def rollback(self):
        """Revierte la transacción activa."""
        if self.conexion and self.conexion.is_connected():
            self.conexion.rollback()

    def desconectar(self):
        """Cierra la conexión y el cursor."""
        try:
            if self.cursor is not None:
                self.cursor.close()
        except Error:
            pass
        finally:
            self.cursor = None

        try:
            if self.conexion is not None and self.conexion.is_connected():
                self.conexion.close()
        except Error:
            pass
        finally:
            self.conexion = None