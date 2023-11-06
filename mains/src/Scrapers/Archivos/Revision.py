from config import revision
from os import path
from src.Singleton import Singleton

class Revision(Singleton):
  _archivo_revisiones = revision
  
  def agregar_revision(self, url: str): open(self._archivo_revisiones, 'a').write(f'{url}\n')
    
  def eliminar_revisiones(self): open(self._archivo_revisiones, 'w').close()
  
  def listar_revisiones(self):
    if not path.exists(self._archivo_revisiones): return
    with open(self._archivo_revisiones, 'r') as f: return [line.replace('\n', '') for line in f.readlines() if line]