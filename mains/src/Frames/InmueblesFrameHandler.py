from src.Frames.InmueblesFrame import InmueblesFrame
from src.Singleton import Singleton
from config import path_df_LV, path_df_ML, path_df_ZP
from src.Filters.StrategyFilter import *

class InmueblesFrameHandler(Singleton):
  _LV = path_df_LV
  _ML = path_df_ML
  _ZP = path_df_ZP

  def open_frames(self) -> InmueblesFrame: 
    frame = InmueblesFrame()
    frame.concat([self.frame_LV, self.frame_ML, self.frame_ZP])
    return frame
  
  @property
  def frame_LV(self) -> InmueblesFrame: 
    frame = InmueblesFrame(self._LV)
    FilterLV().property_filter(frame)
    return frame
  @property
  def frame_ML(self) -> InmueblesFrame:
    frame = InmueblesFrame(self._ML)
    FilterML().property_filter(frame)
    return frame
  @property
  def frame_ZP(self) -> InmueblesFrame:
    frame = InmueblesFrame(self._ZP)
    FilterZP().property_filter(frame)
    return frame
    
  def crear_frame(self, df: pd.DataFrame):
    return InmueblesFrame(df=df)