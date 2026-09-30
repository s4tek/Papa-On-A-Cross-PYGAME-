import pygame
import config
import time

def ingresar_nombre(ventana, ancho, alto):
    jugador = ""
    ingresando = True
    fuente = pygame.font.Font(None, 50)

    while ingresando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None  # Si se cierra la ventana, terminamos el programa
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Confirmar nombre con Enter
                    if jugador.strip():
                        ingresando = False
                        print(f"Nombre del jugador: {jugador}")
                        # Mostrar animación de cargando antes de retornar
                        for i in range(9):  # 3 ciclos de 'Cargando.', 'Cargando..', 'Cargando...'
                            ventana.fill(config.COLOR_FONDO)
                            puntos = '.' * ((i % 3) + 1)
                            texto_cargando = fuente.render(f"Cargando{puntos}", True, config.COLOR_TEXTO)
                            ventana.blit(texto_cargando, (ancho // 2 - texto_cargando.get_width() // 2, alto // 2))
                            pygame.display.update()
                            pygame.time.delay(300)
                        return jugador
                    else:
                        print("Debe ingresar un nombre válido.")
                elif evento.key == pygame.K_BACKSPACE:  # Borrar un carácter
                    jugador = jugador[:-1]
                else:
                    jugador += evento.unicode  # Agregar carácter ingresado

        # Dibujar pantalla de ingreso
        ventana.fill(config.COLOR_FONDO)
        texto_ingreso = fuente.render("Ingrese su nombre:", True, config.COLOR_TEXTO)
        nombre_ingresado = fuente.render(jugador, True, config.COLOR_TEXTO)
        presione_enter = fuente.render("Presione Enter para continuar", True, config.COLOR_TEXTO_SECUNDARIO)

        ventana.blit(texto_ingreso, (ancho // 2 - texto_ingreso.get_width() // 2, alto // 3))
        ventana.blit(nombre_ingresado, (ancho // 2 - nombre_ingresado.get_width() // 2, alto // 2))
        ventana.blit(presione_enter, (ancho // 2 - presione_enter.get_width() // 2, alto // 1.5))

        pygame.display.update()
