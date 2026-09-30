import pygame
import os
import pickle
import importlib
import importlib.util
from typing import List, Dict

if importlib.util.find_spec("tileset_manager") is not None:
    tileset_manager = importlib.import_module("tileset_manager")
    TilesetManager = tileset_manager.TilesetManager
    AdvancedMundo = tileset_manager.AdvancedMundo
else:
    class TilesetManager:
        """Fallback local para gestionar tilesets si no existe tileset_manager.py."""

        def __init__(self, tileset_path: str, tile_size: int = 50):
            self.tileset_path = tileset_path
            self.tile_size = tile_size
            self.tile_mapping = create_tileset_mapping()
            self.tiles = []
            self._load_tiles()

        def _load_tiles(self):
            imagen = pygame.image.load(self.tileset_path)
            width = imagen.get_width()
            for x in range(0, width, self.tile_size):
                tile = imagen.subsurface((x, 0, self.tile_size, self.tile_size))
                self.tiles.append(tile)

        def get_tile(self, value: int):
            idx = self.tile_mapping.get(value)
            if idx is None:
                return None
            if 0 <= idx < len(self.tiles):
                return self.tiles[idx]
            return None

        def set_tile_mapping(self, mapping: Dict[int, int]):
            self.tile_mapping = mapping

        def get_tileset_info(self):
            return {
                "tileset_path": self.tileset_path,
                "tile_size": self.tile_size,
                "tiles_count": len(self.tiles),
                "mapping": self.tile_mapping,
            }

    class AdvancedMundo:
        """Representacion basica de mundo usando un tileset combinado."""

        def __init__(self, nivel_data: List[List[int]], tileset_path: str, tile_size: int = 50):
            self.nivel_data = nivel_data
            self.tile_size = tile_size
            self.tileset_manager = TilesetManager(tileset_path, tile_size=tile_size)
            self.lista_mosaico = []
            self._build_world()

        def _build_world(self):
            self.lista_mosaico.clear()
            for fila, row in enumerate(self.nivel_data):
                for columna, mosaico in enumerate(row):
                    image = self.tileset_manager.get_tile(mosaico)
                    if image is None:
                        continue
                    image_rect = image.get_rect()
                    image_rect.x = columna * self.tile_size
                    image_rect.y = fila * self.tile_size
                    self.lista_mosaico.append((image, image_rect))

        def dibujo(self, ventana):
            for item in self.lista_mosaico:
                ventana.blit(item[0], item[1])

def create_tileset_from_existing_images(archivos_path: str, output_path: str = "tileset_combinado.png"):
    """
    Crea un tileset combinado a partir de las imágenes existentes.
    
    Args:
        archivos_path: Ruta a la carpeta de archivos
        output_path: Ruta donde guardar el tileset combinado
    """
    # Lista de imágenes a combinar en el tileset
    imagenes_tileset = [
        'plataforma1.png',
        'piedramusgo.png', 
        'piedras.png',
        'escalera.png',
        'plat_musgo_izq.png',
        'plat_musgo_centro.png',
        'plat_musgo_der.png'
    ]
    
    tile_size = 50
    tiles_per_row = 7  # Una fila con todos los tiles
    
    # Crear superficie para el tileset
    tileset_surface = pygame.Surface((tiles_per_row * tile_size, tile_size), pygame.SRCALPHA)
    
    for i, imagen_nombre in enumerate(imagenes_tileset):
        try:
            imagen_path = os.path.join(archivos_path, imagen_nombre)
            imagen = pygame.image.load(imagen_path)
            imagen_escalada = pygame.transform.scale(imagen, (tile_size, tile_size))
            
            # Colocar en el tileset
            x = i * tile_size
            tileset_surface.blit(imagen_escalada, (x, 0))
            
        except Exception as e:
            print(f"Error cargando {imagen_nombre}: {e}")
    
    # Guardar el tileset
    pygame.image.save(tileset_surface, output_path)
    print(f"Tileset guardado en: {output_path}")
    
    return output_path

def convert_existing_mundo_to_advanced(archivos_path: str, nivel_data: List[List[int]], tileset_path: str = None):
    """
    Convierte el sistema actual de Mundo al nuevo AdvancedMundo.
    
    Args:
        archivos_path: Ruta a la carpeta de archivos
        nivel_data: Datos del nivel
        tileset_path: Ruta al tileset (se crea automáticamente si es None)
        
    Returns:
        Instancia de AdvancedMundo
    """
    if tileset_path is None:
        tileset_path = create_tileset_from_existing_images(archivos_path)
    
    # Crear el mundo avanzado
    advanced_mundo = AdvancedMundo(nivel_data, tileset_path, tile_size=50)
    
    return advanced_mundo

def load_level_data(archivo_nivel: str) -> List[List[int]]:
    """
    Carga los datos de nivel desde un archivo pickle.
    
    Args:
        archivo_nivel: Ruta al archivo de nivel
        
    Returns:
        Datos del nivel como matriz 2D
    """
    with open(archivo_nivel, 'rb') as f:
        return pickle.load(f)

def create_tileset_mapping() -> Dict[int, int]:
    """
    Crea el mapeo estándar para el tileset.
    
    Returns:
        Diccionario con el mapeo de tipos a índices
    """
    return {
        0: None,  # Espacio vacío
        1: 0,     # Plataforma básica (plataforma1.png)
        2: 1,     # Plataforma con musgo (piedramusgo.png)
        3: 2,     # Ladrillos (piedras.png)
        4: 3,     # Escalera (escalera.png)
        5: 4,     # Musgo izquierdo (plat_musgo_izq.png)
        6: 5,     # Musgo centro (plat_musgo_centro.png)
        7: 6,     # Musgo derecho (plat_musgo_der.png)
    }

def create_custom_tileset_mapping(tileset_info: Dict) -> Dict[int, int]:
    """
    Crea un mapeo personalizado basado en la información del tileset.
    
    Args:
        tileset_info: Información del tileset
        
    Returns:
        Mapeo personalizado
    """
    # Aquí puedes personalizar el mapeo según tu tileset
    # Por ejemplo, si tienes un tileset con diferentes tipos de tiles
    return {
        0: None,  # Espacio vacío
        1: 0,     # Suelo básico
        2: 1,     # Suelo con textura
        3: 2,     # Pared
        4: 3,     # Escalera
        5: 4,     # Decoración izquierda
        6: 5,     # Decoración centro
        7: 6,     # Decoración derecha
        # Puedes añadir más mapeos según necesites
    }

def example_usage():
    """
    Ejemplo de cómo usar el nuevo sistema de tilesets.
    """
    # Configuración
    archivos_path = "archivos"
    nivel_archivo = "nivel1.pkl"
    
    # Cargar datos del nivel
    nivel_data = load_level_data(nivel_archivo)
    
    # Crear tileset combinado
    tileset_path = create_tileset_from_existing_images(archivos_path)
    
    # Crear mundo avanzado
    advanced_mundo = AdvancedMundo(nivel_data, tileset_path, tile_size=50)
    
    # Personalizar mapeo si es necesario
    custom_mapping = create_custom_tileset_mapping(advanced_mundo.tileset_manager.get_tileset_info())
    advanced_mundo.tileset_manager.set_tile_mapping(custom_mapping)
    
    return advanced_mundo

if __name__ == "__main__":
    # Ejemplo de uso
    mundo = example_usage()
    print("Mundo creado exitosamente!")
    print(f"Información del tileset: {mundo.tileset_manager.get_tileset_info()}") 