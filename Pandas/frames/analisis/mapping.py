import geopandas as gpd
import matplotlib.pyplot as plt
from PDconfig import path_MapaCBA


def mappingCapitalInmuebles(casas, deptos, img):
    """Genera un mapa de la ciudad de Córdoba Capital con las publicaciones de departamentos y casas

    Args:
        casas (DataFrame): DataFrame con las publicaciones de casas
        deptos (DataFrame): DataFrame con las publicaciones de departamentos
        img (str): Ruta donde se guardará la imagen del mapa
    """
    ubicados_d = deptos.loc[deptos['coordX'].notna()]
    ubicados_c = casas.loc[casas['coordX'].notna()]

    latitudes_d, longitudes_d = ubicados_d['coordX'], ubicados_d['coordY']
    latitudes_c, longitudes_c = ubicados_c['coordX'], ubicados_c['coordY']

    barrios = gpd.read_file(path_MapaCBA)

    ax = plt.subplots(figsize=(20, 20))
    barrios.boundary.plot(ax=ax, color='black', label='Barrios')
    ax.scatter(longitudes_d, latitudes_d, color='red',
               label='Departamentos', s=2, alpha=0.5)
    ax.scatter(longitudes_c, latitudes_c, color='blue',
               label='Casas', s=2, alpha=0.5)

    map_padding = 0.0125
    ax.set_xlim(-64.30-map_padding, -64.06 + map_padding)
    ax.set_ylim(-31.52-map_padding, -31.31 + map_padding)

    ax.set_title(
        'Mapa de Publicaciones de Casas y Departamentos en Córdoba Capital')
    ax.legend()
    plt.savefig(img)


def mappingCapitalTerrenosGrandes(terrenos_grandes, img):
    barrios = gpd.read_file(path_MapaCBA)

    ax = plt.subplots(figsize=(20, 20))
    barrios.boundary.plot(ax=ax, color='black', label='Barrios')

    for row in terrenos_grandes.iterrows():
        ax.annotate(str(row['id']), (row['coordY'], row['coordX']), fontsize=12,
                    ha='center', va='center', color='black', backgroundcolor='white', bbox=dict(facecolor='white', edgecolor='black'))

    map_padding = 0.0125  # Increase the padding for more zoom-out effect
    ax.set_xlim(-64.30 - map_padding, -64.06 + map_padding)
    ax.set_ylim(-31.52 - map_padding, -31.31 + map_padding)

    ax.set_title('Mapa de Publicaciones de Terrenos Grandes en Ciudad de CBA')
    ax.legend()
    plt.savefig(img, dpi=300, bbox_inches="tight")
