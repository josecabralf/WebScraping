from ScrapConfig import revision
from os import path

class Revision:
  _archivo_revisiones = revision
  _instance = None
  @classmethod
  def get_instance(self):
      if self._instance is None:
          self._instance = self()
      return self._instance
  
  def agregar_revision(self, url: str): open(self._archivo_revisiones, 'a').write(f'{url}\n')
    
  def eliminar_revisiones(self): open(self._archivo_revisiones, 'w').close()
  
  def listar_revisiones(self):
    if not path.exists(self._archivo_revisiones): return
    with open(self._archivo_revisiones, 'r') as f: return [line.replace('\n', '') for line in f.readlines()]