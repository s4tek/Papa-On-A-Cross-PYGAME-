import pygame
from modelo import listar_jugadores
import config






def mostrar_puntajes(ventana):
    corriendo = True
    reloj = pygame.time.Clock()
    fuente_titulo = pygame.font.Font(None, 48)
    fuente_puntajes = pygame.font.Font(None, 36)
    fuente_salida = pygame.font.Font(None, 30)

    exito, jugadores = listar_jugadores()
    ultimo_refresh = pygame.time.get_ticks()
    intervalo_refresh_ms = 2000

    while corriendo:
        ventana.fill((255, 255, 255))  # Fondo blanco

        # Título de la ventana
        texto_titulo = fuente_titulo.render("Puntajes", True, config.COLOR_PUNTAJES)
        ventana.blit(texto_titulo, (400, 50))

        # Refresca puntajes cada cierto tiempo para evitar consultas por frame.
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - ultimo_refresh >= intervalo_refresh_ms:
            exito, jugadores = listar_jugadores()
            ultimo_refresh = tiempo_actual

        if exito:
            y_offset = 150
            for jugador, puntos, fecha in jugadores[:10]:  # Mostrar los 10 mejores
                texto_puntaje = fuente_puntajes.render(
                    f"{jugador} - {puntos:.2f} segundos - {fecha}", True, config.COLOR_PUNTAJES
                )
                ventana.blit(texto_puntaje, (200, y_offset))
                y_offset += 40
        else:
            texto_error = fuente_titulo.render("Error al cargar los puntajes.", True, config.COLOR_PUNTAJES_ERROR)
            ventana.blit(texto_error, (300, 200))

        # Mensaje para salir
        texto_salida = fuente_salida.render("Presione ESC para salir", True, config.COLOR_PUNTAJES)
        ventana.blit(texto_salida, (350, 550))  # Coordenadas ajustadas al final de la pantalla

        # Eventos para salir de la ventana
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return 'salir'
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                corriendo = False

        pygame.display.flip()
        reloj.tick(60)
    return 'menu'
        
