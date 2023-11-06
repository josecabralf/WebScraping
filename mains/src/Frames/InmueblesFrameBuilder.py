import os
from src.Frames.InmueblesFrame import InmueblesFrame

class InmueblesFrameBuilder:
  def __init__(self, path, frame: str|InmueblesFrame = None) -> None:
    self.set_dir(path)
    self.set_frame(frame)
  
  def crear_frame(self):
    if os.listdir(self._dir):
        self._load_frame()
        self._frame_main.format()

  def _load_frame(self):
    dir = os.listdir(self._dir)
    for archivo in dir:
        df_i = InmueblesFrame(path=f"{self._dir}{archivo}")
        self._frame_main.concat([df_i.get_activos()])
  
  def get_frame(self): return self._frame_main
  def set_frame(self, frame: str|InmueblesFrame):
    if not frame: self._frame_main = InmueblesFrame()
    elif isinstance(frame, InmueblesFrame): self._frame_main = frame
    elif isinstance(frame, str): self._frame_main = InmueblesFrame(path=frame)
    else: self._frame_main = InmueblesFrame()
  
  def guardar_frame(self, path, excel = False, activos = False): 
    self._frame_main.guardar_df(path, excel=excel, activos=activos)
    
  def set_dir(self, dir): self._dir = dir if dir.endswith('/') else dir + '/'