from bs4 import BeautifulSoup
import requests
from config import URL


# Accedemos a contenidos de URL
pagina_trabajos = requests.get(URL) 
# Instanciamos BS colocando content de url y formato
soup = BeautifulSoup(pagina_trabajos.content, 'html.parser') 

# Buscamos el contenedor que tiene la informacion que buscamos
trabajos_encontrados = soup.find(id = 'ResultsContainer')

# Buscamos los trabajos especificos
elementos_trabajos = trabajos_encontrados.find_all('div', class_='card-content')

# Listamos los trabajos individuales
"""for trabajo in elementos_trabajos:
    title_element = trabajo.find("h2", class_="title").text.strip()
    company_element = trabajo.find("h3", class_="company").text.strip()
    location_element = trabajo.find("p", class_="location").text.strip()
    print(title_element)
    print(company_element)
    print(location_element)
    print()
"""

# Vamos a crear un filtro para solo buscar los que sean de Python
trabajos_con_python = trabajos_encontrados.find_all(
    "h2", string=lambda text: "python" in text.lower()
) # Con este solo obtenemos los H2 que poseen Python en su nombre

trabajos_con_python_elementos = [
    h2_element.parent.parent.parent for h2_element in trabajos_con_python
] # Ahora hay que encontrar los elementos de trabajos que tengan Python


for trabajo in trabajos_con_python_elementos:
    titulo = trabajo.find("h2", class_="title")
    compania = trabajo.find("h3", class_="company")
    lugar = trabajo.find("p", class_="location")
    url = trabajo.find_all('a')[1]['href']
    
    print(titulo.text.strip())
    print(compania.text.strip())
    print(lugar.text.strip())
    print(f'Apply Here - {url}')
    print()
