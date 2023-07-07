from bs4 import BeautifulSoup
import requests
import json

def scrapLaVoz(URL,archivo):
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    descripciones_casas = soup.find_all('div', class_ = 'card-body md-mh sm-py1 md-py0 px1 px-md-1 flex flex-column flex-auto relative justify-top pb0 border-silver border rounded-bottom')
    ultima = descripciones_casas[-1]

    with open(archivo, 'w', encoding='utf-8') as archivoJSON:
        archivoJSON.write('[')
        for casa in descripciones_casas:            
            
            # Extraccion precio
            try:
                precio = casa.find('span', class_="price").text.strip()
                precio = int(precio.split()[1].replace('.',''))
            except:
                continue

            try:
                ubicacion = casa.find('div', class_="h5 mx0 mt0 mb1 col-12 font-light title-1lines").text.strip()
            except:
                ubicacion = '' # Si no tiene ubicacion le asignamos ''


            # Extraccion de datos de interes
            datos_interes = casa.find('div', class_="gray").text.split() # Cant Dormitorios, Cant Banos, Terreno m2
            posibles = ['FichaInmueble_dormitorios', 'FichaInmueble_bano', 'FichaInmueble_superficie']
            nums = [-1, -1, -1]
            for dato in datos_interes:
                try:
                    dato = int(dato)
                except:
                    dato_ant = dato
                else:
                    for i in range(len(posibles)):
                        if dato_ant == posibles[i]:
                            nums[i] = dato
                            break

            objetoJSON = {
                "ubicacion" : ubicacion,
                "precioUSD" : precio,
                "habitaciones" : nums[0],
                "banos" : nums[1],
                "terreno" : nums[2],
            } # Creamos el objeto a escribir
            json.dump(objetoJSON, archivoJSON, indent=6) # Lo escribimos en el archivo
            if casa != ultima:
                archivoJSON.write(',')
        archivoJSON.write(']')