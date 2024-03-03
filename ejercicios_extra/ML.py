"""
El modelo consistira en una serie de funciones que nos permitiran modificar los datos, filtrarlos y analizarlos, de los diccionarios 
obtenidos del archivo clases.py.

Basicamente obtendremos el diccionario que vemos abajo al llamar a la funcion seleccion de muestras, y obtendremos una lista de diccionarios
aleatorios que se crearon de los combates, mas adelante especificaremos que queremos analizar, es decir, si queremos ver que clases funcionan mejor,
que armas son mas poderosas, o que combinacion de daño, velocidad, armadura, arma y clase tiene el porcentaje de victoria mas alto.

La primera parte de este archivo es la creacion de las funciones y la segunda es  una prueba con las mismas funciones, buscando que clases
tienen mas porcentaje de victorias.

Cosas a comentar: muchas de las funciones tienen valores por defecto y todas tiene comentarios explicadno cada funcionalidad; los filtros de muestras
no los he usado para mi ensayo, pero si que funcionan; la parte del ensayo, es decir, la parte donde visualizamos los datos que hemos obtenido
despues dek proceso es algo que dependera de lo que queramos estudiar, no es una funcion que hace todo el proceso de forma automatica.

Este modelo no aprende automaticamente, simplemente analiza los datos que se obtienen del juego, los cambios de balances se tendran que hacer
de forma manual en el codigo (de momento jejeje).

La funcion clasificacion_de_muestras ha sido obtenida mediante chat gpt, debido a que la complejidad de determinar cuanto gana un personaje, 
cuantas replicas de la misma combinacion en una lista de diccionarios existen, ademas de eliminar dichos duplicados, era muy elevada.
"""

import clases

""" EL TIPO DE DICCIONARIO SOBRE EL QUE ITERAREMOS
dicc_resultados = { este es el diccionario que devuelve la funcion seleccion_de_batalla()
        "personaje": {
            "nombre": personaje.nombre,
            "daño": personaje.daño,
            "armadura": personaje.armadura,
            "velocidad": personaje.velocidadAtaque,
            "vida": personaje.vida,
            "clase": personaje.clase,
            "Arma usada": arma.nombre,
            "Monstruo combatido": monstruo.nombre,
        },
        "monstruo": {
            "nombre": monstruo.nombre,
            "daño": monstruo.daño,
            "vida": monstruo.vida,
            "velocidad": monstruo.velocidad,
        },
        "arma usada": {
            "nombre": arma.nombre,
            "daño": arma.daño,
            "velocidad": arma.velocidad,
            "tipo": arma.tipo
        },
        "ganador": depende de quien haya ganado si el monstruo o el personaje,
} 
"""
#-----------------------------Obtencion de datos-----------------------------------------------

def obtencion_de_muestras(num_muestras:int) -> list: # numero de pruebas que quieres
    informacion_total = [] # lista donde guardaremos cada uno de los diccionaros con la informacion de los combates aleatorios 
    for i in range(num_muestras):
        personaje = clases.crear_personaje(i) # creamos un personaje siendo i el id que poseera su nombre (algo meramente estetico)
        resultado = clases.seleccion_de_batalla(personaje, 2) #el 2 representa el indice dentro de la lista de monstruos
        informacion_total.append(resultado)
    return informacion_total # Esto es una lista de diccionarios como el que se muestra arriba


#----------------------------------------------funciones de filtrado-----------------------------------------------------------------------------------------------------

#le pasaremos una lista como parametro y lo que queremos filtrar y nos devolvera la lista filtrada, por si queremos conocer algun aspecto especifico

def filtro_muestras(muestras:list, entidad:str, a_filtrar:str, filtro:str) -> list: # cuando queremos filtrar un diccionario dentro de otro, por ejemplo: info {personaje: {daño : 5, velocidad: 6}}
    muestra_filtrada = [filtrado for filtrado in muestras if filtrado[entidad][a_filtrar] == filtro]
    return muestra_filtrada

def filtro_muestras_sencillo(muestras:list, a_filtrar:str, filtro:str) -> list: # cuando queremos filtrar un escalon menos ("personaje", "monstruo", "arma", "ganador", etc...), mirar claves del diccionario para entender
    muestra_filtrada = [filtrado for filtrado in muestras if filtrado[a_filtrar] == filtro]
    return muestra_filtrada

#------------------------------------funciones de resultado-------------------------------------------------------------------------------

# Nos dice en un diccionario las veces que se han repetido los atributos que asignamos y las veces que ha ganado dicha combinacion, eliminando duplicados

def clasificacion_de_muestras(muestras, claves_a_comprobar, entidad="personaje"): # lo que hace esta funcion es contar los repetidos, ver cuantos son, contar las veces que ha ganado el personaje para calcular posteriormente su porcentaje de victorias, ademas de eliminar duplicados, lo he tenido que sacar con ayuda de chat gpt
    combinaciones = {}
    victorias = {}

    # Paso 1: Conteo de combinaciones y victorias
    for diccionario in muestras:
        clave = tuple(diccionario[entidad][key] for key in claves_a_comprobar)
        combinaciones[clave] = combinaciones.get(clave, 0) + 1
        if diccionario["ganador"] == entidad:
            victorias[clave] = victorias.get(clave, 0) + 1

    # Paso 2: Asignar conteos y victorias a cada muestra
    for diccionario in muestras:
        clave = tuple(diccionario[entidad][key] for key in claves_a_comprobar)
        diccionario[entidad]["veces"] = combinaciones[clave]
        diccionario[entidad]["victorias"] = victorias.get(clave, 0)

    # Paso 3: Filtrar duplicados manteniendo el primer elemento de cada combinación única
    lista_filtrada = []
    claves_vistas = set()
    for diccionario in muestras:
        clave = tuple(diccionario[entidad][key] for key in claves_a_comprobar)
        if clave not in claves_vistas:
            lista_filtrada.append(diccionario)
            claves_vistas.add(clave)

    return lista_filtrada

# Esta funcion calculara el porcentaje de victorias de la muestra que le pasemos y lo añadira en cada diccionario, ademas de ordenar la muestra

def calculo_de_porcentajes(muestras:list, orden:bool = True):
    for i in muestras:
        porcentaje_de_victoria = (i["personaje"]["victorias"]/i["personaje"]["veces"])*100 # En pocentaje
        i["win rate"] = porcentaje_de_victoria

    muestras.sort(key=lambda x: x.get("win rate", 0), reverse=orden) # ordenamos la lista de manera que los primeros elementos seran los que mayor win rate tengan
    return muestras

#---------------------------------Ensayo de clases------------------------------------------------------------

# Con estas herramientas podriamos saber casi todo, vamos a hacer un analisis para ver que clase tiene mas porcentaje de victorias:

# primero declaramos la muestra inical:
muestras = obtencion_de_muestras(100_000) # hemos especificado que queremos 100000 muestras 

claves_a_comprobar = ["clase"] # solo queremos comprobar la clase, pero podriamos hacer cualquier combinacion que queramos
muestras_clasificadas = clasificacion_de_muestras(muestras, claves_a_comprobar) # esto va a añadir el numero de veces que se repite una clase y el numero de veces que esta gana

muestras_con_porcentaje_de_victoria = calculo_de_porcentajes(muestras_clasificadas) # tendremos una lista de diccionarios ordenados por porcentaje de victoria

# Mostramos resultados:
print(len(muestras_con_porcentaje_de_victoria)) # Como observamos es 3 porque hay 3 clases

for i in muestras_con_porcentaje_de_victoria:
    print(f"La clase {i["personaje"]["clase"]} tiene un ratio de victorias de {i["win rate"]}% es decir {i["monstruo"]["nombre"]} gana con un ratio del{100- i["win rate"]}%")

# Este es solo un ejemplo en el que queda bastante claro que las clases y los monstruos estan desbalanceados
# Podemos hacerlo con cualquier combinacion
# cambiando el numero de muestras y las claves podemos obtener cualquier combinacion

