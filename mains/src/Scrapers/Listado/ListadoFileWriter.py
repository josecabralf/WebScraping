from config import cols, linea_null


class ListadoFileWriter:
  _cols = cols
  _linea_null = linea_null
  def __init__(self, archivo: str) -> None:
    self._archivo = archivo
    
  def escribir_archivo_csv(self, listado) -> None:
    if not self.validar_listado(listado): return
    with open(self._archivo, 'w', encoding='utf-8') as file:
        file.write(self._cols)
        for p in self.stream_str_publicaciones(listado): file.write(p)
        file.write(self._linea_null)
    
  def stream_str_publicaciones(self, listado) -> str:
    for url in listado.publicaciones():
        try: p = listado.crear_publicacion(url)
        except Exception as err: 
            listado.crear_log_error(f"error no controlado al crear publicacion", err)
            continue
        if p.is_valid(): yield str(p)
          
  def validar_listado(self, listado):
    if listado.publicaciones() != []: return True
    listado.crear_log_error(f"no se pudo crear archivo {self._archivo} porque no hay publicaciones")
    return False
      