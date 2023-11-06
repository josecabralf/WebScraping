from threading import Thread

from src.Scrapers.Archivos.Logger import LoggeableOperator
from src.Scrapers.Archivos.Archiver import Archiver
from src.Scrapers.Archivos.Revision import Revision
from src.Scrapers.Archivos.Dater import Dater

from src.Scrapers.PaginaWeb.FactoryPaginaWeb import FactoryPaginaWeb
from src.Scrapers.PaginaWeb import PaginaWeb


class ThreadedScraper(LoggeableOperator):
    def __init__(self, directorio: str, factory: FactoryPaginaWeb) -> None:
        self._archiver = Archiver(directorio)
        self._pagina_web : PaginaWeb = factory.crear_pagina_web()
        
    def crear_archivo(self) -> str:
        nom = self._archiver.nombre_archivo()
        self._archiver.actualizar_archivos_creados()
        return nom
    
    def comprimir_archivos(self) -> None: self._archiver.comprimir_archivos()
        
    def scrap_hilo(self, i: int, archivo: str, publicaciones: list = []) -> None:
        self._pagina_web.escribir_listado(i, archivo, publicaciones)

    def scrap_multi_hilo(self, nros_listado: list, archivos: list) -> None:
        threads = [None] * len(nros_listado)
        for i in range(len(threads)): threads[i] = Thread(target=self.scrap_hilo, args=([nros_listado[i], archivos[i]]))
        for i in range(len(threads)): threads[i].start()
        for i in range(len(threads)): threads[i].join()
             
    @property
    def cant_paginas(self) -> int: return self._pagina_web.cantidad_paginas         

    def scrap_pagina_web(self) -> None:
        cant_pags = self.cant_paginas
        for i in range(1, cant_pags-1, 3): self.scrap_multi_hilo([i, i+1, i+2], [self.crear_archivo() for _ in range(3)])
        if cant_pags % 3 == 1: self.scrap_multi_hilo([cant_pags], [self.crear_archivo()])
        elif cant_pags % 3 == 2: self.scrap_multi_hilo([cant_pags-1, cant_pags], [self.crear_archivo() for _ in range(2)])
        self.escribir_revisiones()
    
    def execute(self) -> None:
        self.crear_log_operacion('INICIO SCRAP', self._pagina_web.__class__)
        self.scrap_pagina_web()
        self.comprimir_archivos()
        self.crear_log_operacion('FIN SCRAP', self._pagina_web.__class__)
        self.actualizar_fecha_ultimo_scrap()
        
    def lista_revisiones(self): return Revision().listar_revisiones()
    
    def eliminar_revisiones(self): Revision().eliminar_revisiones()
    
    def escribir_revisiones(self):
        revisiones = self.lista_revisiones()
        if not revisiones: return
        self.scrap_hilo(-1, self.crear_archivo(), revisiones)
        self.eliminar_revisiones()
        
    def actualizar_fecha_ultimo_scrap(self): Dater().set_fecha(self._pagina_web.__class__)