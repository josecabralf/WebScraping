"""Modulo para ejecutar scrapers en hilos"""
from time import sleep
from threading import Thread
from Scrapers.FactoryPaginaWeb import FactoryPaginaWeb
from Scrapers.PaginaWeb.PaginaWeb import PaginaWeb
from Scrapers.Archiver import Archiver
from Scrapers.Revision import Revision


class ThreadedScraper:
    def __init__(self, directorio, factory: FactoryPaginaWeb) -> None:
        self._archiver = Archiver(directorio)
        self._pagina_web : PaginaWeb = factory.crear_pagina_web()

    def escribir_listado(self, i: int, archivo: str): self._pagina_web.escribir_listado(i, archivo)
    
    def escribir_listado_desde_lista(self, publicaciones: list, archivo: str): 
        self._pagina_web.escribir_listado_desde_lista(publicaciones, archivo)
        
    def crear_archivo(self) -> str:
        nom = self._archiver.nombre_archivo()
        self._archiver.actualizar_archivos_creados()
        return nom
    
    def comprimir_archivos(self): self._archiver.comprimir_archivos()
        
    def scrap_hilo(self, i: int, archivo: str):
        try: self.escribir_listado(i, archivo)
        except:
            sleep(5)
            self.escribir_listado(i, archivo)
    
    def get_cant_paginas(self): return self._pagina_web.cantidad_paginas

    def scrap_multi_hilo(self, nros_listado: list, archivos: list):
        threads = [None] * len(nros_listado)
        for i in range(len(threads)): 
            threads[i] = Thread(target=self.scrap_hilo, args=([nros_listado[i], archivos[i]]))
        for i in range(len(threads)): threads[i].start()
        for i in range(len(threads)): threads[i].join()
             
    def scrap_pagina_web(self):
        cant_pags = self.get_cant_paginas()
        for i in range(1, cant_pags, 3): 
            self.scrap_multi_hilo([i, i+1, i+2], [self.crear_archivo() for _ in range(3)])
        if cant_pags % 3 == 1:
            self.scrap_multi_hilo([cant_pags], [self.crear_archivo()])
        elif cant_pags % 3 == 2:
            self.scrap_multi_hilo([cant_pags-1, cant_pags], [self.crear_archivo() for _ in range(2)])
        self.escribir_revisiones()
        self.comprimir_archivos()
        
    def lista_revisiones(self): return Revision.get_instance().listar_revisiones()
    
    def eliminar_revisiones(self): Revision.get_instance().eliminar_revisiones()
    
    def escribir_revisiones(self):
        revisiones = self.lista_revisiones()
        if not revisiones: return
        self.escribir_listado_desde_lista(revisiones, self.crear_archivo())
        self.eliminar_revisiones()