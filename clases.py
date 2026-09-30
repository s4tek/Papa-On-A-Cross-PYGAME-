import pygame
from pygame.locals import *
import os
import math
import cv2
import config

# Funciones utilitarias para cargar recursos

def cargar_imagen(ruta, tamano=None):
    imagen = pygame.image.load(os.path.join(config.ARCHIVOS, ruta))
    if tamano:
        imagen = pygame.transform.scale(imagen, tamano)
    return imagen

def cargar_sonido(ruta):
    return pygame.mixer.Sound(os.path.join(config.ARCHIVOS, ruta))

pygame.init()

# Carga de recursos usando funciones centralizadas
papa = cargar_imagen('papaemeritus.png')
municion = cargar_imagen('bala.png')
imagen_jesucristo = cargar_imagen('cristo_m4.png')
imagen_bala = cargar_imagen('bala.png')
papacelda = cargar_imagen('celdapapa.png')
celda = cargar_imagen('celda.png')
risapapa = cargar_sonido('paparisa.mp3')
icono = cargar_imagen('papaicono.png')

ancho = config.ANCHO_PANTALLA
alto = config.ALTO_PANTALLA
ancho_pantalla = config.ANCHO_PANTALLA
alto_pantalla = config.ALTO_PANTALLA
carpeta = config.CARPETA
archivos = config.ARCHIVOS

# Clase base para entidades del juego
class Entidad(pygame.sprite.Sprite):
    """Entidad base para Jugador, Enemigo y Jesucristo."""
    def __init__(self, x, y, frames=None, salud=100, velocidad_x=0, velocidad_y=0, gravedad=1):
        super().__init__()
        self.frames = frames if frames else []
        self.current_frame = 0
        self.image = self.frames[self.current_frame] if self.frames else None
        self.rect = self.image.get_rect(topleft=(x, y)) if self.image else pygame.Rect(x, y, 50, 50)
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y
        self.gravedad = gravedad
        self.en_suelo = False
        self.salud = salud
        self.esta_vivo = True
        self.last_update = pygame.time.get_ticks()
        self.angulo_rotacion = 0

    def aplicar_gravedad(self):
        self.velocidad_y += self.gravedad

    def actualizar_animacion(self, intervalo=300):
        now = pygame.time.get_ticks()
        if self.frames and now - self.last_update > intervalo:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_update = now

    def mover_horizontal(self, dx):
        self.rect.x += dx

    def mover_vertical(self, dy):
        self.rect.y += dy

    def recibir_daño(self, cantidad):
        self.salud -= cantidad
        if self.salud <= 0:
            self.esta_vivo = False

#  Clase Corazon
class Corazon(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = imagen
        self.rect = self.image.get_rect(topleft=(x, y))
        
    def update(self):
        pass

# Clase Boton
class Boton(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = pygame.transform.scale(imagen, (200, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.accion = False
    
    def dibujar(self, ventana):
        ventana.blit(self.image, (self.rect.x, self.rect.y))

    def esta_clickeado(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                return True
        return False
    
# Clase Papa Emeritus(A rescatarlo)    

class Emeritus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = pygame.transform.scale(papacelda, (200, 200))  # Imagen inicial
        self.rect = self.image.get_rect()  # Obtener rectángulo de la imagen
        self.rect.x = x
        self.rect.y = y
        self.rect_invisible = pygame.Rect(self.rect.x + 50, self.rect.y + 50, 100, 100)
        
    def cambiar_imagen(self, papa):
        """Cambia la imagen de Emeritus."""
        self.image = pygame.transform.scale(papa, (100, 100))  # Redimensiona a 100x100
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.y = 550 - self.rect.height  # Ajusta la posición en 'y'

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect.topleft)  # Dibuja la imagen
        

    def reproducir_video(self, video_path):
        """Reproduce un video al final del juego con música de fondo."""
        pygame.display.set_caption("Papa on a Cross")
        pantalla = pygame.display.set_mode((800, 600))
        
        # Cargar y reproducir música de fondo
        musica_final = os.path.join(archivos, 'musica_final.mp3')
        try:
            pygame.mixer.music.load(musica_final)
            pygame.mixer.music.play(-1)  # -1 para reproducir en bucle
        except pygame.error as e:
            print(f"Error al cargar la música: {e}")
        
        video = cv2.VideoCapture(video_path)
        reloj = pygame.time.Clock()
        
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)  # Corregir la orientación del video
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (800, 600))
            frame_surface = pygame.surfarray.make_surface(frame)
            
            pantalla.blit(pygame.transform.rotate(frame_surface, -90), (0, 0))
            pygame.display.update()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    video.release()
                    pygame.mixer.music.stop()  # Detener la música si el usuario cierra el juego
                    pygame.quit()
                    return
            
            reloj.tick(30)
        
        # Liberar recursos y detener música
        video.release()
        pygame.mixer.music.stop()  # Detener la música al finalizar el video
        return True








# Clase Enemigo 

class Enemigo(Entidad):
    def __init__(self, x, y, frames, archivos, limite_izquierdo=50, limite_derecho=400):
        super().__init__(x, y)
        self.esta_vivo = True
        self.salud = 50
        self.frames = frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad_x = 2
        self.velocidad_y = 0
        self.gravedad = 1
        self.en_suelo = False
        self.last_update = pygame.time.get_ticks()
        self.limite_izquierdo = limite_izquierdo
        self.limite_derecho = limite_derecho
        self.grito_enemigo = cargar_sonido(os.path.join(archivos, 'gritomonje.mp3'))
        self.angulo_rotacion = 0
        self.sonido_muerte_reproducido = False
        self.invulnerable = False  # Nuevo atributo
        self.tiempo_ultimo_golpe = 0
        self.tiempo_invulnerabilidad = 400  # ms

    def recibir_daño(self, cantidad):
        ahora = pygame.time.get_ticks()
        if not self.invulnerable:
            self.salud -= cantidad
            if self.salud <= 0 and not self.sonido_muerte_reproducido:
                self.grito_enemigo.play()
                self.esta_vivo = False
                self.sonido_muerte_reproducido = True
            self.invulnerable = True
            self.tiempo_ultimo_golpe = ahora

    def update(self, mundo):
        ahora = pygame.time.get_ticks()
        if self.invulnerable and ahora - self.tiempo_ultimo_golpe > self.tiempo_invulnerabilidad:
            self.invulnerable = False
        if self.esta_vivo:
            # Movimiento horizontal
            self.rect.x += self.velocidad_x

            # Movimiento en Y (gravedad)
            if not self.en_suelo:
                self.velocidad_y += self.gravedad
            self.rect.y += self.velocidad_y

            # Colisiones con plataformas
            self.en_suelo = False
            for item in mundo.lista_mosaico:
                plataforma_rect = item[1]
                if plataforma_rect.colliderect(self.rect.x, self.rect.y + self.velocidad_y, self.rect.width, self.rect.height):
                    if self.velocidad_y > 0:
                        self.rect.bottom = plataforma_rect.top
                        self.velocidad_y = 0
                        self.en_suelo = True

                
            # Detectar la cercanía a los bordes de las plataformas
            if not self.en_suelo:  # Si el enemigo está en el aire
                # Comprobar si el enemigo está cerca del borde de la plataforma a la izquierda
                izquierda_rect = pygame.Rect(self.rect.left - 5, self.rect.bottom, 10, 1)
                derecha_rect = pygame.Rect(self.rect.right-5, self.rect.bottom, 10, 1)
                colision_izquierda = False
                colision_derecha = False

                for item in mundo.lista_mosaico:
                    plataforma_rect = item[1]
                    if izquierda_rect.colliderect(plataforma_rect):
                        colision_izquierda = True
                    if derecha_rect.colliderect(plataforma_rect):
                        colision_derecha = True

                # Si no hay plataformas a la izquierda o derecha, cambiamos la dirección del enemigo
                if not colision_izquierda and self.velocidad_x < 0:  # Si no hay plataforma a la izquierda y el enemigo se mueve a la izquierda
                    self.velocidad_x = abs(self.velocidad_x)  # Mover a la derecha
                elif not colision_derecha and self.velocidad_x > 0:  # Si no hay plataforma a la derecha y el enemigo se mueve a la derecha
                    self.velocidad_x = -abs(self.velocidad_x)  # Mover a la izquierda

            # Animación
            now = pygame.time.get_ticks()
            if now - self.last_update > 500:  # Cambiar cada 500 ms
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.last_update = now

            # Dirección del sprite
            self.image = self.frames[self.current_frame]
            if self.velocidad_x < 0:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            # Comportamiento al morir
            self.rect.y += 5
            self.angulo_rotacion += 5
            if self.angulo_rotacion >= 360:
                self.angulo_rotacion = 0
            self.image = pygame.transform.rotate(self.frames[self.current_frame], self.angulo_rotacion)
            self.rect = self.image.get_rect(center=self.rect.center)
  
    
        
# Clase Jugador
class Jugador(Entidad):
    def __init__(self, x, y, frames, archivos):
        super().__init__(x, y)
        self.frames = frames  
        self.current_frame = 0
        self.image = self.frames[self.current_frame] 
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidad_y = 0  
        self.velocidad_x = 4  
        self.gravedad = 1
        self.en_suelo = False
        self.direccion = 1
        self.direccion_anterior = 1
        self.last_update = pygame.time.get_ticks()

        # Salud y vidas
        self.salud = 100  # Agregar este atributo
        self.vidas = 3
        self.salud_maxima = 100
        self.muerto = False
        self.tiempo_ultimo_daño = 0
        self.duracion_invulnerabilidad = 50
        
        self.ancho_pantalla = ancho_pantalla
        
        # Sonidos
        self.grito_muerte = cargar_sonido(os.path.join(archivos, 'namelessmuerte.mp3'))

        # Cargar el sprite sheet de los corazones
        sheet_corazones = cargar_imagen(os.path.join(archivos, 'sheetcorazones.png'))
        ancho_corazon = sheet_corazones.get_width() // 3
        alto_corazon = sheet_corazones.get_height()
        
        self.corazon_lleno = sheet_corazones.subsurface((0, 0, ancho_corazon, alto_corazon))
        self.corazon_medio = sheet_corazones.subsurface((ancho_corazon, 0, ancho_corazon, alto_corazon))
        self.corazon_vacio = sheet_corazones.subsurface((ancho_corazon * 2, 0, ancho_corazon, alto_corazon))

        # Rotación continua (angulo de rotacion)
        self.angulo_rotacion = 0  

    def dibujar_corazones(self, pantalla):
        tamaño_corazon = (40, 40)
        posicion_x, posicion_y = 10, 10 

        for i in range(3):  
            if i < self.vidas - 1:  
                imagen_corazon = self.corazon_lleno
            elif i == self.vidas - 1:  
                if self.salud > 50:
                    imagen_corazon = self.corazon_lleno
                elif 0 < self.salud <= 50:
                    imagen_corazon = self.corazon_medio
                else:
                    imagen_corazon = self.corazon_vacio
            else:  
                imagen_corazon = self.corazon_vacio
        
            pantalla.blit(pygame.transform.scale(imagen_corazon, tamaño_corazon), (posicion_x + i * (tamaño_corazon[0] + 5), posicion_y))

    def recibir_daño(self, cantidad):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_ultimo_daño >= self.duracion_invulnerabilidad:
            self.salud -= cantidad
            self.tiempo_ultimo_daño = tiempo_actual
            
            if self.salud <= 0:
                self.vidas -= 1
                self.salud = self.salud_maxima if self.vidas > 0 else 0
            
            if self.vidas <= 0:
                self.muerto = True
                print("Moriste")
                self.grito_muerte.play()

    def recolectar_corazon(self):
        # Solo suma vida si no está al máximo
        if self.vidas < 3 or (self.vidas == 3 and self.salud < self.salud_maxima):
            if self.vidas < 3:
                self.vidas += 1
                self.salud = self.salud_maxima
            elif self.vidas == 3 and self.salud < self.salud_maxima:
                self.salud = self.salud_maxima


    def update(self, mundo, niveles, nivel_actual, enemigos, pantalla):
        if self.muerto:
            # Si el jugador está muerto, continuar con la animación de muerte
            self.angulo_rotacion += 5  
            if self.angulo_rotacion >= 360:
                self.angulo_rotacion = 0  

            # Rotar la imagen según el ángulo
            self.image = pygame.transform.rotate(self.frames[self.current_frame], self.angulo_rotacion)
            self.rect = self.image.get_rect(center=self.rect.center)  
            return

        tecla = pygame.key.get_pressed()
        dx = 0 
        dy = 0 

        # Verificar colisiones con los enemigos en general
        self.verificar_colision_con_enemigos(enemigos)

        # Salto
        if tecla[pygame.K_SPACE] and self.en_suelo:  
            self.velocidad_y = -20  

        # Aplicar gravedad
        self.velocidad_y += self.gravedad
        dy += self.velocidad_y

        # Movimiento hacia los lados
        if tecla[pygame.K_LEFT]:
            dx = -self.velocidad_x
            if self.direccion != -1:
                self.direccion = -1
                self.image = pygame.transform.flip(self.frames[self.current_frame], True, False)
        
        if tecla[pygame.K_RIGHT]:
            dx = self.velocidad_x
            if self.direccion != 1:
                self.direccion = 1
                self.image = self.frames[self.current_frame]  

        # Verificar colisiones con plataformas
        self.en_suelo = False  
        for item in mundo.lista_mosaico:
            plataforma_rect = item[1]
            
            # Verificar colisiones en Y (saltando y cayendo)
            if plataforma_rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.velocidad_y > 0:  
                    dy = plataforma_rect.top - self.rect.bottom
                    self.velocidad_y = 0
                    self.en_suelo = True
                elif self.velocidad_y < 0:  
                    dy = plataforma_rect.bottom - self.rect.top
                    self.velocidad_y = 0

            # Verificar colisiones en X (movimiento horizontal)
            if plataforma_rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0  

        # Actualizar posición del jugador
        self.rect.x += dx
        self.rect.y += dy

        # Restricción de movimiento en los bordes laterales
        if self.rect.left < 0:  
            self.rect.left = 0
        elif self.rect.right > self.ancho_pantalla:  
            self.rect.right = self.ancho_pantalla

        # Actualizar la animación
        now = pygame.time.get_ticks()
        if now - self.last_update > 300:  
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame] if self.direccion == 1 else pygame.transform.flip(self.frames[self.current_frame], True, False)
            self.last_update = now

            
    def verificar_colision_con_enemigos(self, enemigos):
        for enemigo in enemigos:
            if self.rect.colliderect(enemigo.rect):
                if enemigo.esta_vivo and self.velocidad_y > 0 and self.rect.bottom <= enemigo.rect.top + 10:
                    enemigo.recibir_daño(50)
                    self.velocidad_y = -10
                else:
                    if enemigo.esta_vivo and not enemigo.invulnerable:
                        self.recibir_daño(10)
                    
    def verificar_colision_con_cristo(self, jesucristo):
        if self.rect.colliderect(jesucristo.rect):
            if self.velocidad_y > 0 and self.rect.bottom <= jesucristo.rect.top + 10:
                jesucristo.recibir_daño(50)
                self.velocidad_y = -10
            else:
                self.recibir_daño(10)
            
    def cargar_siguiente_nivel(self, niveles, nivel_actual):
        # Cambiar al siguiente nivel
        nivel_actual += 1
        if nivel_actual >= len(niveles):
            nivel_actual = 0  
        return nivel_actual
   
# Clase Jesucristo
    
class Jesucristo(Entidad):
    def __init__(self, x, y, imagen_jesucristo, imagen_bala, limite_izquierdo=0, limite_derecho=1000, emeritus=Emeritus):
        super().__init__(x, y)
        self.image_derecha = pygame.transform.scale(imagen_jesucristo, (100, 100))
        self.image_izquierda = pygame.transform.flip(self.image_derecha, True, False)
        self.image = self.image_derecha  # Imagen inicial
        self.rect = self.image.get_rect()
        self.esta_vivo = True
        self.salud = 200
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 1
        self.velocidad_x = 1
        self.velocidad_y = 0
        self.gravedad = 1
        self.en_suelo = False
        self.derrotado = False
        self.last_update = pygame.time.get_ticks()
        self.limite_izquierdo = limite_izquierdo
        self.limite_derecho = limite_derecho
        self.balas = pygame.sprite.Group()  # Para almacenar las balas disparadas
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()  # Para controlar la cadencia de disparo
        self.imagen_bala = imagen_bala  # Imagen de la bala
        self.cabeza_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height // 8)
        self.emeritus = emeritus
        self.sonido_disparo = cargar_sonido(archivos+ '\\metra.mp3')
        self.sonido_risa = cargar_sonido(archivos+ '\\paparisa.mp3')
        self.animacion_muerte = False  # Atributo para controlar la animación de muerte
        self.tiempo_inicio_muerte = 0  # Tiempo de inicio de la animación de muerte
        
        # Canal de disparo: se crea un canal para evitar que el sonido se interrumpa
        self.canal_disparo = pygame.mixer.Channel(1)  # Usar el canal 1 o cualquier canal libre
        
        # Control para evitar que la risa se repita
        self.ya_reprodujo_risa = False
        
        # Fuente para el cartel
        self.font = pygame.font.SysFont('Arial', 36)  # Fuente para el texto del cartel
        self.mostrar_cartel = False  # Control para mostrar el cartel
        self.tiempo_cartel = 0  # Para manejar el tiempo de visualización del cartel

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect.topleft)
        self.balas.draw(pantalla)
        
        # Mostrar el cartel si es necesario
        if self.mostrar_cartel:
            texto = self.font.render("¡Papa Emeritus fue rescatado!", True, (128, 0, 32))
            texto2 = self.font.render("Acercate a Emeritus para continuar..", True, (128, 0, 32)) 
            texto_rect = texto.get_rect(center=(500, 250))  # Posición del texto (centrado en la pantalla)
            texto_rect2 = texto.get_rect(center=(500, 450))  # Posición del texto (centrado en la pantalla)
            pantalla.blit(texto, texto_rect) 
            pantalla.blit(texto2, texto_rect2)

    def recibir_daño(self, cantidad):
        self.salud -= cantidad
        if self.salud <= 0:
            self.esta_vivo = False
            self.morir()
    
    def morir(self):
        if self.ya_reprodujo_risa:
            return  # No hacer nada si ya se ha reproducido la risa

        self.esta_vivo = False
        self.animacion_muerte = True  # Activar la animación de muerte (fade out)
        self.tiempo_inicio_muerte = pygame.time.get_ticks()  # Marcar el tiempo en que comenzó la animación
        self.balas.empty()  # Evita balas congeladas durante la animacion de muerte

        if self.canal_disparo.get_busy():
            self.canal_disparo.stop()

        # Reproducir la risa solo una vez
        self.sonido_risa.play()
        self.ya_reprodujo_risa = True

        self.emeritus.cambiar_imagen(papa)  # Cambiar imagen del emeritus
        self.mostrar_cartel = True  # Activar el cartel
        self.tiempo_cartel = pygame.time.get_ticks()  # Marcar el tiempo en que comenzó a mostrar el cartel
        

    def disparar(self, jugador):
        if self.derrotado:
            return  # No hacer nada si está derrotado

        now = pygame.time.get_ticks()
        if now - self.tiempo_ultimo_disparo >= 500:  # Controla el tiempo entre disparos
            jugador_x, jugador_y = jugador.rect.center
            enemigo_x, enemigo_y = self.rect.center

            distancia_x = jugador_x - enemigo_x
            distancia_y = 0

            distancia = math.sqrt(distancia_x**2 + distancia_y**2)

            if distancia != 0:
                direccion_x = distancia_x / distancia
                direccion_y = 0

                flip = direccion_x < 0
                ancho_bala = 5
                altura_bala = 5
                desplazamiento_y = -13

                if flip:
                    desplazamiento_x = -55
                else:
                    desplazamiento_x = 55

                bala = Bala(self.imagen_bala, enemigo_x, enemigo_y, direccion_x, direccion_y, flip, ancho_bala, altura_bala, desplazamiento_x, desplazamiento_y)
                self.balas.add(bala)

                # Reproducir el sonido de disparo en el canal específico
                if not self.canal_disparo.get_busy():  # Solo si el canal está libre
                    self.canal_disparo.play(self.sonido_disparo)

                self.tiempo_ultimo_disparo = now


    def perseguir(self, jugador):
        jugador_x, jugador_y = jugador.rect.center
        distancia_x = jugador_x - self.rect.centerx
        distancia_y = jugador_y - self.rect.centery
        distancia_total = math.sqrt(distancia_x**2 + distancia_y**2)

        if distancia_total != 0:
            direccion_x = distancia_x / distancia_total
            direccion_y = distancia_y / distancia_total
        else:
            direccion_x = 0
            direccion_y = 0

        # Actualizar la velocidad según la dirección hacia el jugador
        self.velocidad_x = direccion_x * self.velocidad
        self.rect.x += self.velocidad_x * self.velocidad
        self.rect.y += direccion_y * self.velocidad

    def update(self, mundo, jugador):
        if self.derrotado:
            self.balas.empty()
            return

        if not self.esta_vivo and not self.animacion_muerte:
            return

        # Animación de muerte (desvanecimiento)
        if self.animacion_muerte:
            tiempo_actual = pygame.time.get_ticks()
            self.balas.empty()

            # Verificar si la animación ha terminado
            if tiempo_actual - self.tiempo_inicio_muerte > 10000:  # Duración total de la animación
                self.kill()  # Eliminar el sprite al finalizar
                return

            # Calcula el tiempo transcurrido
            tiempo_transcurrido = tiempo_actual - self.tiempo_inicio_muerte

            # Reducir la opacidad (fade out)
            alpha = max(0, 255 - int((tiempo_transcurrido / 2000) * 255))
            imagen_con_alpha = self.image.copy()
            imagen_con_alpha.set_alpha(alpha)  # Cambiar la opacidad de la imagen

            # Actualizar imagen
            self.image = imagen_con_alpha

            # Movimiento hacia arriba (borde superior)
            velocidad_subida = -3  # Velocidad de movimiento hacia arriba
            self.rect.y += velocidad_subida

            # Reducir el tamaño del rectángulo de colisión progresivamente
            self.rect.size = (max(1, self.rect.width - 1), max(1, self.rect.height - 1))
            self.cabeza_rect.size = (1, 1)

            return  # Terminar aquí para evitar ejecutar código adicional

        # Comprobar si el cartel debe desaparecer después de 2 segundos
        if self.mostrar_cartel and pygame.time.get_ticks() - self.tiempo_cartel >= 2000:
            self.mostrar_cartel = False  # Desactivar el cartel después de 2 segundos

        # Actualizar movimiento y disparos
        self.perseguir(jugador)
        self.disparar(jugador)
        self.cabeza_rect.y = self.rect.y
        self.cabeza_rect.x = self.rect.x

        # Actualizar balas
        self.balas.update()
        for bala in self.balas:
            if bala.rect.colliderect(jugador.rect):  # Verificar colisión con el jugador
                jugador.recibir_daño(50)  # Infligir daño
                bala.kill()  # Eliminar la bala después de la colisión

        # Movimiento vertical y gravedad
        self.rect.x += self.velocidad_x
        self.velocidad_y += self.gravedad
        self.rect.y += self.velocidad_y

        # Detección de suelo
        self.en_suelo = False
        for item in mundo.lista_mosaico:
            plataforma_rect = item[1]
            if plataforma_rect.colliderect(self.rect.x, self.rect.y + self.velocidad_y, self.rect.width, self.rect.height):
                if self.velocidad_y > 0:
                    self.rect.bottom = plataforma_rect.top
                    self.velocidad_y = 0
                    self.en_suelo = True

        # Caída cuando no está en suelo
        if not self.en_suelo:
            self.velocidad_y += self.gravedad

        # Flip de la imagen según la dirección del movimiento
        if self.velocidad_x > 0:  # Si se mueve a la derecha
            self.image = self.image_derecha
        else:  # Si se mueve a la izquierda
            self.image = self.image_izquierda

        self.rect = self.image.get_rect(topleft=self.rect.topleft)  # Mantener la posición del rect

            
class Bala(pygame.sprite.Sprite):
    def __init__(self, imagen, x, y, direccion_x, direccion_y, flip=False, ancho=5, altura=5, desplazamiento_x=0, desplazamiento_y=0):
        super().__init__()
        # Redimensiona la bala al tamaño especificado
        self.image = pygame.transform.scale(imagen, (ancho, altura))  
        self.rect = self.image.get_rect()

        # Ajustar la posición de la bala con desplazamientos adicionales
        self.rect.center = (x + desplazamiento_x, y + desplazamiento_y)

        # Direcciones de la bala
        # Ajustada para mantener la sensacion de velocidad previa sin doble update por frame.
        self.velocidad_x = direccion_x * 6  # Velocidad de la bala en X
        self.velocidad_y = direccion_y * 6  # Velocidad de la bala en Y

        # Flip de la bala si es necesario
        self.flip = flip
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        # Actualiza la posición de la bala
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Eliminar la bala si sale de la pantalla
        if not (0 <= self.rect.x <= 1000 and 0 <= self.rect.y <= 800):  # Ajusta según tu resolución
            self.kill()
            
# Clase Mundo
class Mundo():
    def __init__(self, datos, archivos):
        self.lista_mosaico = []
        plataforma1 = cargar_imagen(archivos+'\\plataforma1.png')
        plataformamusgo = cargar_imagen(archivos+'\\piedramusgo.png')
        musgo_centro = cargar_imagen(archivos+'\\plat_musgo_centro.png')
        musgo_izq = cargar_imagen(archivos+'\\plat_musgo_izq.png')
        musgo_der = cargar_imagen(archivos+'\\plat_musgo_der.png')
        ladrillos = cargar_imagen(archivos+'\\piedras.png')
        cementerio = cargar_imagen(archivos+'\\cementerio.png')
        cielo = cargar_imagen(archivos+'\\cielocementerio.png')
        escalerameta = cargar_imagen(archivos+'\\escalera.png')
        
        cont_fila = 0
        
        for fila in datos:
            columna = 0
            for mosaico in fila:
                if mosaico == 1:
                    image = pygame.transform.scale(plataforma1, (50, 50))
                    image_rect = image.get_rect()
                    image_rect.x = columna * 50
                    image_rect.y = cont_fila * 50
                    imagen = (image, image_rect)
                    self.lista_mosaico.append(imagen)
                    
                if mosaico == 2:
                    image = pygame.transform.scale(plataformamusgo, (50, 50))
                    image_rect = image.get_rect()
                    image_rect.x = columna * 50
                    image_rect.y = cont_fila * 50
                    imagen = (image, image_rect)
                    self.lista_mosaico.append(imagen)
                    
                if mosaico == 3:
                    image = pygame.transform.scale(ladrillos, (50, 50))
                    image_rect = image.get_rect()
                    image_rect.x = columna * 50
                    image_rect.y = cont_fila * 50
                    imagen = (image, image_rect)
                    self.lista_mosaico.append(imagen)
                
                if mosaico == 4:
                    image = pygame.transform.scale(escalerameta, (50, 50))
                    image_rect = image.get_rect()
                    image_rect.x = columna * 50
                    image_rect.y = cont_fila * 50
                    imagen = (image, image_rect)
                    self.lista_mosaico.append(imagen)
                    
                if mosaico == 5:
                    image = pygame.transform.scale(musgo_izq, (50, 50))
                    image_rect = image.get_rect()
                    image_rect.x = columna * 50
                    image_rect.y = cont_fila * 50
                    imagen = (image, image_rect)
                    self.lista_mosaico.append(imagen)
                    
                if mosaico == 6:
                    image = pygame.transform.scale(musgo_centro, (50, 50))
                    image_rect = image.get_rect()
                    image_rect.x = columna * 50
                    image_rect.y = cont_fila * 50
                    imagen = (image, image_rect)
                    self.lista_mosaico.append(imagen)
                    
                if mosaico == 7:
                    image = pygame.transform.scale(musgo_der, (50, 50))
                    image_rect = image.get_rect()
                    image_rect.x = columna * 50
                    image_rect.y = cont_fila * 50
                    imagen = (image, image_rect)
                    self.lista_mosaico.append(imagen)
                    
                else:
                    columna += 1
                    continue
                      
                columna += 1
            cont_fila += 1
            
    def dibujo(self, ventana):
        for item in self.lista_mosaico:
            ventana.blit(item[0], item[1])