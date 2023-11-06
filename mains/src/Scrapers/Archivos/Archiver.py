import pandas as pd
import os

class Archiver:
    def __init__(self, dir) -> None:
        self.set_dir(dir)
        self._nro_actual = self.asignar_nro()
        self._archivos_actual = 1
        
    def nombre_archivo(self) -> str:
        return f"{self._dir}{self._nro_actual}-pagina{self._archivos_actual}.csv"
      
    def asignar_nro(self) -> int:
        dir = os.listdir(self._dir)
        if dir == []: return 1
        dir = [int(n.split('-')[0]) for n in dir]
        return max(dir) + 1

    def comprimir_archivos(self):
        df_main = pd.DataFrame() 
        comprimidos = []
        for archivo in os.listdir(self._dir):
            try: df_main = self.add_df_to_main(df_main, archivo)    
            except: continue
            comprimidos.append(archivo)
        self.guardar_df_main(df_main)
        self.eliminar_archivos(comprimidos)

    def add_df_to_main(self, df_main: pd.DataFrame, archivo: str):
        df_i = pd.read_csv(f"{self._dir}{archivo}", sep=';')
        self.drop_fechas_null(df_i)
        return df_main._append(df_i, ignore_index=True)
        
    def guardar_df_main(self, df_main):
        self.eliminar_filas_null(df_main)
        df_main.to_csv(f"{self._dir}{self.asignar_nro()}-result.csv", index=False, sep=';')

    def drop_fechas_null(self, df): df.dropna(subset=['fechaUltimaActualizacion'], inplace=True)
    
    def actualizar_nro_actual(self): self._nro_actual = self.asignar_nro()
    
    def actualizar_archivos_creados(self): self._archivos_actual += 1
    
    def eliminar_filas_null(self, df: pd.DataFrame): df.drop(df[df["id"] == 0].index, inplace=True)
    
    def eliminar_archivos(self, archivos: list):
        for archivo in archivos: os.remove(f"{self._dir}{archivo}")
    
    @property
    def dir(self): return self._dir
    def set_dir(self, dir): self._dir = dir if dir.endswith('/') else dir + '/'