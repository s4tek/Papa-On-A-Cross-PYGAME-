import tkinter.messagebox
import pygame
import clases
from clases import Boton, Jugador, Mundo, Enemigo, Corazon, Jesucristo, Bala, Emeritus
from conexion import Conexion
import os
import sys
import pickle
import tkinter
import datetime
from puntajes import mostrar_puntajes
from modelo import nuevo_jugador
from ingreso_nombre import ingresar_nombre
from tiempo_puntaje import TiempoPuntaje
import config

pygame.init()
pygame.mixer.init()

# Configuración de carpeta y archivos
carpeta = config.CARPETA
archivos = config.ARCHIVOS

# Configuración de la pantalla
ancho = config.ANCHO_PANTALLA
alto = config.ALTO_PANTALLA
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Papa on a Cross')
jugador=ingresar_nombre(ventana, ancho, alto)
if jugador is None:
    ejecutar=False


# Carga imagenes y recursos
def cargar_imagen(ruta, tamaño=None):
    imagen = pygame.image.load(os.path.join(archivos, ruta))
    if tamaño:
        imagen = pygame.transform.scale(imagen, tamaño)
    return imagen

icono = cargar_imagen('papaicono.png')
pygame.display.set_icon(icono)

# Recursos de imagenes
logospygameaseprite = cargar_imagen('cargalogos.png', (ancho, alto))    
logoghost = cargar_imagen('ghostlogo.jpg', (ancho, alto))
cementerio = cargar_imagen('cementerio.png', (ancho, alto))
menu_imagen = cargar_imagen('imagen_menu.png', (ancho, alto))
cielo = cargar_imagen('cielocementerio.png', (ancho, alto))
cielo2 = cargar_imagen('cielocementerio2.png', (ancho, alto))
cielo3 = cargar_imagen('cielocementerio3.png', (ancho, alto))
cielo_final = cargar_imagen('cielofinal.png', (ancho, alto))
historia1 = cargar_imagen('historiainicio1.png', (ancho, alto))
historia2 = cargar_imagen('historiainicio2.png', (ancho, alto))
corazon_imagen = cargar_imagen('corazonvida.png', (30, 30))
parlanteon = cargar_imagen('parlanteon.png', (30, 30))
parlanteoff = cargar_imagen('parlanteoff.png', (30, 30))
escalera = cargar_imagen('escalera.png', (50, 50))

# Botones del menu
btn_jugar = Boton(400, 425, cargar_imagen('boton_jugar.png', (200, 50)))
btn_puntuaciones = Boton(400, 485, cargar_imagen('boton_puntuaciones.png', (200, 50)))
btn_salir = Boton(400, 545, cargar_imagen('boton_salir.png', (200, 50)))

# Inicializacion del juego
nivel_juego = 1
archivo_nivel = os.path.join(carpeta, f'nivel{nivel_juego}.pkl')
with open(archivo_nivel, 'rb') as picle_dato:
    datos = pickle.load(picle_dato)

mundo = Mundo(datos, archivos)

# Tiempo, jugador, puntaje  y fin del juego   
def guardar_puntaje(jugador, puntos):
    fecha_actual= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if nuevo_jugador(jugador, puntos, fecha_actual):
        print(f"El puntaje de {jugador} se guardó correctamente.")
    else: 
        print(f"Error al guardar el puntaje de {jugador}")
           
# Crear jugador y enemigos
corazones_nameless = pygame.sprite.Group()
enemigo_frames = [cargar_imagen('enemigo_anim.png', (150, 75)).subsurface(pygame.Rect(i * 50, 0, 50, 75)) for i in range(2)]
jugador_frames = [cargar_imagen('nameless_anim.png', (150, 75)).subsurface(pygame.Rect(i * 50, 0, 50, 75)) for i in range(2)]
imagen_jesucristo = pygame.image.load(archivos+ '\\cristo_m4.png')
imagen_bala = cargar_imagen('bala.png')
nameless = Jugador(50, 450, jugador_frames, archivos)
emeritus = Emeritus(50, 350)
jesucristo = Jesucristo(100, 200, imagen_jesucristo, imagen_bala, emeritus=emeritus)  # Correcto
enemigos_nameless = pygame.sprite.Group()


def configurar_corazones(nivel):
    corazones_nameless.empty()
    if nivel == 1:                     #H   #V
        corazones_nameless.add(Corazon(  0, 150, corazon_imagen))  
    
    if nivel == 2:
        corazones_nameless.add(Corazon(700,  50, corazon_imagen))  
    
    if nivel == 3:
        corazones_nameless.add(Corazon(950, 250, corazon_imagen))
        
    if nivel == 4:
        corazones_nameless.add(Corazon(950, 250, corazon_imagen))  

configurar_corazones(nivel_juego)

def configurar_enemigos(nivel):
    enemigos_nameless.empty()
    if nivel == 1:                    #H  #V
        
       enemigos_nameless.add(Enemigo(250, 250, enemigo_frames, archivos))
       enemigos_nameless.add(Enemigo(300, 450, enemigo_frames, archivos))
       enemigos_nameless.add(Enemigo(450, 300, enemigo_frames, archivos))
       enemigos_nameless.add(Enemigo(250,  50, enemigo_frames, archivos))
       
       
    elif nivel == 2:
        enemigos_nameless.add(Enemigo(400, 250, enemigo_frames, archivos))
        enemigos_nameless.add(Enemigo(200, 500, enemigo_frames, archivos))
        enemigos_nameless.add(Enemigo(600, 200, enemigo_frames, archivos))
        
        

    elif nivel == 3:
        enemigos_nameless.add(Enemigo(200, 250, enemigo_frames, archivos))
        enemigos_nameless.add(Enemigo(350, 400, enemigo_frames, archivos))
        enemigos_nameless.add(Enemigo(800, 400, enemigo_frames, archivos))
    
        
    elif nivel == 4:
        enemigos_nameless.add(Enemigo(50, 400, enemigo_frames, archivos))
        enemigos_nameless.add(Enemigo(50, 100, enemigo_frames, archivos))
        enemigos_nameless.add(Enemigo(350, 250, enemigo_frames, archivos))
        enemigos_nameless.add(Enemigo(550,  50, enemigo_frames, archivos))
       
configurar_enemigos(nivel_juego)

# Crear meta
meta_rect = pygame.Rect(750, 0, 50, 50)

# Variables del juego
reloj = pygame.time.Clock()
ejecutar = True
pantalla_carga = True
historia_carga = True
menu_inicio = False
mostrando_historia = False
carga_inicial = pygame.time.get_ticks()
total_niveles = config.TOTAL_NIVELES
musica_activada = True
iconomusica_x = 900
iconomusica_y = 20
icono_clickiado = False
cambio_hecho = False

# Variables para controlar la música de fondo
musica_juego_cargada = False
musica_historia_cargada = False

# Definir los posibles estados del juego
game_state = 'carga'  # Puede ser: 'carga', 'menu', 'historia', 'jugando', 'fin'

# Funciones para cada estado

def mostrar_pantalla_carga():
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - carga_inicial < 3000:
        ventana.blit(logospygameaseprite, (0, 0))
    elif 3000 <= tiempo_actual - carga_inicial < 6000:
        ventana.blit(logoghost, (0, 0))
    else:
        return False
    pygame.display.update()
    return True

def mostrar_menu():
    ventana.blit(menu_imagen, (0, 0))
    if musica_activada:
        ventana.blit(parlanteon, (iconomusica_x, iconomusica_y))
    else:
        ventana.blit(parlanteoff, (iconomusica_x, iconomusica_y))
    if btn_jugar.dibujar(ventana):
        pygame.mixer.music.stop()
        return 'historia'
    if btn_puntuaciones.dibujar(ventana):
        mostrar_puntajes(ventana)
    if btn_salir.dibujar(ventana):
        respuesta = tkinter.messagebox.askyesno(title='Salir', message='Confirma salir del juego?')
        if respuesta:
            return 'fin'
    pygame.display.update()
    return 'menu'

def mostrar_historia_estado():
    if not mostrar_historia(pygame.time.get_ticks(), carga_inicial):
        return 'jugando'
    return 'historia'

# Funcion para reiniciar el juego
def reiniciar_juego():
    global mundo, nivel_juego, nameless, enemigos_nameless 
    nivel_juego =  1
    archivo_nivel = os.path.join(carpeta, f'nivel{nivel_juego}.pkl')
    with open(archivo_nivel, 'rb') as picle_dato:
        datos = pickle.load(picle_dato)
    mundo = Mundo(datos, archivos)
    
    nameless.rect.topleft = (50, 450)
    nameless.salud = nameless.salud_maxima
    nameless.vidas = 3
    nameless.muerto = False
    enemigos_nameless.empty()
    configurar_enemigos(nivel_juego) 
    #enemigos_nameless.add(
    #    Enemigo(50, 450, enemigo_frames, archivos), 
    #    Enemigo(600, 450, enemigo_frames, archivos)
    #)


# Mensaje 'moriste'
def mostrar_mensaje_moriste(ventana):
    fuente = pygame.font.SysFont(None, 75)
    texto = fuente.render("Moriste", True, (255, 0, 0))
    ventana.blit(texto, (ancho // 2 - texto.get_width() // 2, alto // 2 - texto.get_height() // 2))
    pygame.display.flip()
    
def mostrar_historia(tiempo_actual, carga_inicial):
    if tiempo_actual - carga_inicial < 3000:
        ventana.blit(historia1, (0, 0))
    elif 3000 <= tiempo_actual - carga_inicial < 12000:
        ventana.blit(historia2, (0, 0))
    else:
        return False  
    pygame.display.update()
    return True

# Funcion mutear o desmutear musica
def musicaon_off():
    global musica_activada
    musica_activada = not musica_activada
    if musica_activada:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()



tiempo_puntaje=TiempoPuntaje()

# Nueva función para mostrar créditos

def mostrar_creditos(ventana):
    ventana.fill((0, 0, 0))
    fuente = pygame.font.SysFont(None, 60)
    texto_creditos = fuente.render("Créditos", True, (255, 255, 255))
    # --- EDITA AQUÍ TUS DATOS ---
    desarrollador = "Desarrollado con Python, Pygame, Aseprite, SQL"
    curso1 = "Créditos: A quien corresponda por imágenes de internet,"
    curso2 = "diseños de Nameless Ghouls, Imagen del Menu Principal,"
    curso3 = "Video del final de Ghost."
    curso4 = "Canciones en 8 Bits de la banda Ghost"
    proyecto1 = "Proyecto diseñado como examen final de curso"
    proyecto2 = "de Programacion de Python y SQL."
    proyecto3 = "Este Proyecto no tiene beneficio comercial"
    proyecto4 = "Es estudiantil para demostrar conocimientos"
    anio = "Año: 2024"
    fuente2 = pygame.font.SysFont(None, 36)                                         
    y = 100
    ventana.blit(texto_creditos, (ancho // 2 - texto_creditos.get_width() // 2, y))
    y += 70
    textos = [desarrollador, curso1, curso2, curso3, curso4, proyecto1, proyecto2, proyecto3, proyecto4, anio]
    for texto in textos:
        t = fuente2.render(texto, True, (200, 200, 200))
        ventana.blit(t, (ancho // 2 - t.get_width() // 2, y))
        y += 45
    pygame.display.update()

# Variables para controlar el flujo de créditos
mostrar_creditos_flag = False
creditos_timer = 0
CREDITOS_DURACION = 15000  # milisegundos (15 segundos)

# Bucle principal del juego
while ejecutar:
    tiempo_actual = pygame.time.get_ticks()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutar = False

        # Detección de clics en el menú principal
        if game_state == 'menu':
            if btn_jugar.esta_clickeado(evento):
                pygame.mixer.music.stop()
                game_state = 'historia'
                carga_inicial = pygame.time.get_ticks()
                tiempo_puntaje.iniciar_tiempo()
                musica_juego_cargada = False  # Reset para que se cargue al entrar en 'jugando'
            if btn_puntuaciones.esta_clickeado(evento):
                resultado_puntajes = mostrar_puntajes(ventana)
                if resultado_puntajes == 'salir':
                    ejecutar = False
            if btn_salir.esta_clickeado(evento):
                respuesta = tkinter.messagebox.askyesno(title='Salir', message='Confirma salir del juego?')
                if respuesta:
                    ejecutar = False
        # Botón de música (funciona en cualquier estado)
        mouse_pos = pygame.mouse.get_pos()
        icono_rect = parlanteon.get_rect(topleft=(iconomusica_x, iconomusica_y))
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if icono_rect.collidepoint(evento.pos):
                musicaon_off()

    if game_state == 'carga':
        if not mostrar_pantalla_carga():
            game_state = 'menu'
    elif game_state == 'menu':
        ventana.blit(menu_imagen, (0, 0))
        btn_jugar.dibujar(ventana)
        btn_puntuaciones.dibujar(ventana)
        btn_salir.dibujar(ventana)
        if musica_activada:
            ventana.blit(parlanteon, (iconomusica_x, iconomusica_y))
        else:
            ventana.blit(parlanteoff, (iconomusica_x, iconomusica_y))
        # Música de menú (solo si no está sonando)
        if not pygame.mixer.music.get_busy() and musica_activada:
            try:
                pygame.mixer.music.load(os.path.join(archivos, 'genesis.wav'))
                pygame.mixer.music.play(-1)
            except pygame.error as e:
                print(f'No se pudo cargar la musica del menu: {e}')
        pygame.display.update()
    elif game_state == 'historia':
        # Eliminar la carga de música aquí
        game_state = mostrar_historia_estado()
    elif game_state == 'jugando':
        if not musica_juego_cargada and musica_activada:
            try:
                pygame.mixer.music.load(os.path.join(archivos, 'monstranceclock.wav'))
                pygame.mixer.music.play(-1)
                musica_juego_cargada = True
            except pygame.error as e:
                print(f'No se pudo cargar la musica del juego: {e}')
        # --- Lógica principal del juego ---
        # Fondo según nivel
        if nivel_juego == 1:
            ventana.blit(cementerio, (0, 0))
        elif nivel_juego == 2:
            ventana.blit(cielo, (0, 0))
        elif nivel_juego == 3:
            ventana.blit(cielo2, (0, 0))
        elif nivel_juego == 4:
            ventana.blit(cielo3, (0, 0))
        elif nivel_juego == 5:
            ventana.blit(cielo_final, (0, 0))
            jesucristo.update(mundo, nameless)
            if jesucristo.salud <= 0:
                jesucristo.morir()
            jesucristo.dibujar(ventana)
            emeritus.update(mundo)
            emeritus.dibujar(ventana)
            if nameless.rect.colliderect(emeritus.rect):
                pygame.mixer.music.stop()
                tiempo_puntaje.finalizar_tiempo()
                tiempo_puntaje.guardar_puntaje(jugador)
                video_path = os.path.join(archivos, 'finalpapaonacross.mp4')
                emeritus.reproducir_video(video_path)
                ventana = pygame.display.set_mode((ancho, alto))  # Restaurar tamaño de ventana
                mostrar_creditos_flag = True
                creditos_timer = pygame.time.get_ticks()
                game_state = 'creditos'
            if nameless.rect.colliderect(jesucristo.cabeza_rect) and nameless.velocidad_y > 0:
                jesucristo.recibir_daño(25)
                nameless.velocidad_y = -10
        mundo.dibujo(ventana)
        # Dibujar la meta
        if nameless.rect.colliderect(meta_rect.inflate(20, 20)):
            ventana.blit(escalera, meta_rect)
        # Actualizar y dibujar sprites
        nameless.update(mundo, niveles=[], nivel_actual=0, enemigos=enemigos_nameless, pantalla=ventana)
        ventana.blit(nameless.image, nameless.rect)
        nameless.dibujar_corazones(ventana)
        enemigos_nameless.update(mundo)
        enemigos_nameless.draw(ventana)
        # Corazones
        corazones_recogidos = pygame.sprite.spritecollide(nameless, corazones_nameless, True)
        for corazon in corazones_recogidos:
            nameless.recolectar_corazon()
        corazones_nameless.update()
        corazones_nameless.draw(ventana)
        # Caídas y reinicio
        if nameless.rect.y > 500:
            print(f'Has perdido en el nivel {nivel_juego}, volviendo al nivel 1')
            reiniciar_juego()
            continue
        # Cambio de nivel
        try:
            if nameless.rect.colliderect(meta_rect.inflate(20, 20)):
                if nivel_juego < total_niveles:
                    nivel_juego += 1
                    archivo_nivel = os.path.join(carpeta, f'nivel{nivel_juego}.pkl')
                    with open(archivo_nivel, 'rb') as picle_dato:
                        datos = pickle.load(picle_dato)
                    mundo = Mundo(datos, archivos)
                    if nivel_juego in config.POSICIONES_INICIALES:
                        posicion_x, posicion_y = config.POSICIONES_INICIALES[nivel_juego]
                        nameless.rect.x = posicion_x
                        nameless.rect.y = posicion_y
                    else:
                        nameless.rect.x = 50
                        nameless.rect.y = 400
                    configurar_enemigos(nivel_juego)
                    configurar_corazones(nivel_juego)
                else:
                    print('No hay más niveles')
        except Exception as e:
            print(f'Error en el cambio de nivel: {e}')
        if nameless.muerto:
            mostrar_mensaje_moriste(ventana)
            tiempo_puntaje.finalizar_tiempo()
            tiempo_puntaje.guardar_puntaje(jugador)
            pygame.time.get_ticks()
            reiniciar_juego()
            continue
        pygame.display.update()
    elif game_state == 'creditos':
        mostrar_creditos(ventana)
        if pygame.time.get_ticks() - creditos_timer > CREDITOS_DURACION:
            game_state = 'menu'
    elif game_state == 'fin':
        ejecutar = False
    reloj.tick(config.FPS)

pygame.quit()