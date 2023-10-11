import pandas as pd
import os

class Archiver:
    def __init__(self, dir) -> None:
        self.set_dir(dir)
        self._nro_actual = self.asignar_nro()
        self._archivos_creados = 0
        
    def nombre_archivo(self):
        nom = f"{self._dir}{self._nro_actual}-pagina{self._archivos_creados}.csv"
        return nom
      
    def asignar_nro(self):
        dir = os.listdir(self._dir)
        if dir == []:
            return 1
        dir = [int(n.split('-')[0]) for n in dir]
        return max(dir) + 1

    def comprimir_archivos(self):
        dir = os.listdir(self._dir)
        df_main = pd.DataFrame()
        comprimidos = []
        for archivo in dir:
            try:
                path = f"{self._dir}{archivo}"
                df_i = pd.read_csv(path, sep=';')
                df_i = self.rellenar_activo_fecha(df_i)
                df_main = df_main._append(df_i, ignore_index=True)      
                comprimidos.append(archivo)
            except: continue
        self.eliminar_archivos(comprimidos)
        path = f"{self._dir}{self.asignar_nro()}-result.csv"
        df_main.to_csv(path, index=False, sep=';')

    def rellenar_activo_fecha(self, df):
        df.loc[df['activo'].isna(), 'activo'] = False
        df.loc[df['fechaUltimaActualizacion'].isna(), 'fechaUltimaActualizacion'] = '1900-01-01'
        return df
    
    def actualizar_nro_actual(self): self._nro_actual = self.asignar_nro()
    
    def actualizar_archivos_creados(self): self._archivos_creados += 1
    
    def eliminar_archivos(self, archivos: list):
        for archivo in archivos: os.remove(f"{self._dir}{archivo}")
        
    def get_dir(self): return self._dir
    def set_dir(self, dir): self._dir = dir if dir.endswith('/') else dir + '/'