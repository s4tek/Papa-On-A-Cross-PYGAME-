# Papa on a Cross

## Descripción

"Papa on a Cross" es un videojuego de plataformas desarrollado en Python usando Pygame y MySQL como proyecto final de un curso de Programación en Python y SQL. El juego incluye varios niveles, enemigos, jefe final, sistema de vidas, corazones, animaciones, sonidos, video final y guardado de puntajes en base de datos con respaldo local automático.

## Características principales
- Varios niveles con dificultad progresiva
- Enemigos con IA básica y jefe final
- Sistema de vidas y corazones
- Animaciones y efectos de sonido
- Guardado y visualización de puntajes en MySQL
- Respaldo local de puntajes en `puntajes.txt` cuando MySQL no está disponible
- Menú principal, historia y final con video

## Instalación

1. **Clona el repositorio o descarga los archivos.**
2. **Instala las dependencias:**

```bash
pip install pygame opencv-python mysql-connector-python
```

3. **Configura la base de datos MySQL:**
   - Crea una base de datos llamada `papa_juego`.
   - Ejecuta el script `papa_juego.sql` para crear la tabla de puntajes.
  - Configura la contraseña como variable de entorno `DB_PASSWORD`.

  **PowerShell (Windows):**

```powershell
$env:DB_PASSWORD="TU_PASSWORD_MYSQL"
```

  **Opcionales:**
  - `DB_HOST` (default: `127.0.0.1`)
  - `DB_USER` (default: `root`)
  - `DB_NAME` (default: `papa_juego`)

4. **Ejecuta el juego:**

```bash
python main.py
```

5. **Ejecuta tests unitarios (opcional pero recomendado):**

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Estructura de carpetas

```
Trabajo Final/
  ├── archivos/           # Imágenes, sonidos y videos del juego
  ├── clases.py           # Clases principales del juego (jugador, enemigos, etc.)
  ├── conexion.py         # Conexión a la base de datos MySQL
  ├── ingreso_nombre.py   # Pantalla de ingreso de nombre
  ├── main.py             # Lógica principal y bucle del juego
  ├── modelo.py           # Lógica de guardado y consulta de puntajes
  ├── puntajes.py         # Visualización de puntajes
  ├── serializacion.py    # Utilidad para serializar niveles
  ├── tiempo_puntaje.py   # Gestión de tiempo y puntaje
  ├── config.py           # Configuración global del juego
  ├── niveles.txt, nivelX.pkl # Datos de niveles
  └── papa_juego.sql      # Script SQL para la base de datos
```

## Notas
- El juego requiere Python 3.7+.
- Asegúrate de tener los recursos multimedia en la carpeta `archivos/`.
- Si tienes problemas con la base de datos, revisa la configuración en `conexion.py`.
- Si MySQL falla o no está disponible, el juego guarda y muestra puntajes desde `puntajes.txt`.

---
¡Gracias por jugar y revisar este proyecto! 
