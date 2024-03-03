"""
¿Como funciona el codigo?
Basicamente existen unas clases que son los personajes, los monstruos y las armas, no hacer especial caso en los detalles de las clases debido a
que muchos no se han usado debido a la simplificacion para crear el modelo de ML.
Basicamente los personajes tienen 200 puntos repartidos en daño, velocidad y armadura; tienen 3 clases (Mago, guerrero o acechador), cada clase potenciara
algo de sus atributos (por ejemplo, un guerrero tendra mas vida y armadura de base), dichos personajes deberan escoger un arma que corresponda con su clase
(por ejemplo: los magos solo pueden usar bastones), y pelearan con un monstruo que tendra vida, daño y velocidad; tanto monstruos como arnas
estan creadas de forma predeterminada, solo los personajes seran creados de forma aleatoria, se seleccionara un arma aleatoria (de las que pueda usar cada clase)
y se luchara contra un monstruo que sera seleccionado de la lista y que asignaremos como parametro en una funcion del ML, es decir,
el monstruo contra el que se combate no sera asignado de forma aleatoria.

Una vez se haya creado todo se dara lugar al combate que sera un sistema de turnos aleatorios donde quien tenga mas velocidad tendra mas
probabilidad de ser elegido en el turno, se hara un bucle llamando a la funcion de turnos hasta que uno de los dos muera (el personaje o el monstruo),
una vez esto ocurra, la funcion final (la funcion lucha()), devolvera como parametro un diccionario con toda la informacion de todos los elementos del combate, 
para su posterior estudio en el archivo .py demonimado ML.py .

El arma elegida potencia al personaje, y el personaje luchara contra el monstruo sin habilidades, es decir el monstruo solo recibira el daño
que el personaje tenga como propiedad, las habilidades no se han utilizado en este modelo.
"""


import random

# asignacion de clases

lista_personajes = [] # lista vacia donde guardaremos todos los personajes que vayamos creando

class Personaje:
    estado = True # Es tru si el personaje esta vivo, False si murio
    def __init__(self, nombre, vida, daño_base, velocidad_de_ataque, armadura, nivel=1):
        self.nombre = nombre
        self.vida = vida
        self.nivel = nivel
        self.daño = daño_base
        self.velocidadAtaque = velocidad_de_ataque
        self.armadura = armadura

    def __repr__(self): # Con esto definimos como queremos que nos devuelva un objeto
        return f'{self.nombre} |   clase: {self.clase} |   vida: {self.vida} |  nivel: {self.nivel} |  daño: {self.daño} |  velocidad de ataque: {self.velocidadAtaque} |  armadura: {self.armadura}'

    def subir_de_nivel(self, aumento):
        self.nivel = self.nivel + aumento

    def perder_vida(self, daño_recibido): # Todos los aumentos pueden ser decrementos siempre que usemos numeros negativos
        self.vida = self.vida - daño_recibido
        if self.vida <= 0:
            self.estado = False
            print("Su personaje murio, creese otro o resucitelo")
    
    def aumentar_daño(self, aumento):
        self.vida = self.vida + aumento

    def aumentar_velocidad_de_ataque(self, aumento):
        self.vida = self.vida + aumento

    def aumentar_armadura(self, aumento):
        self.vida = self.vida + aumento

    def restar_puntos_en_la_creacion(puntos, resta):
        puntos = puntos - resta
        if puntos <= 0:
            print("Se paso de sus puntos, repita la creacion de personaje")
            
        return puntos

    def mostrar_personajes(lista_personajes): # Muestra todos los personajes creados de la forma que asignamos en __repr__
        for i in lista_personajes:
            print(i)

#--------------Creacion de clases para los personajes------------------------

class Mago(Personaje):
    def __init__(self, nombre, vida, daño_base, velocidad_de_ataque, armadura, arma = None, clase = "Mago" , nivel=1, mana = 500):
        super().__init__(vida, daño_base, velocidad_de_ataque, armadura, nivel)
        self.nombre = nombre
        self.vida = vida
        self.nivel = nivel
        self.daño = daño_base
        self.velocidadAtaque = velocidad_de_ataque
        self.armadura = armadura
        self.clase = clase
        self.arma = arma
        self.mana = mana + self.nivel*2 + 200 # Cada habilidad tiene un costo en mana para evitar que se use la habilidad mas poderosa, y tengas que usar estrategia
        self.habilidades = {
            "bola de fuego": {
                "daño": 25 + self.nivel*0.1 + daño_base,
                "mana": -15, 
                "vida": 0,
                "armadura": 0,
            },
            "barrera": {
                "daño": 0,
                "mana": -15, 
                "vida": 20,
                "armadura": 50,
            },
            "bola de hielo": {
                "daño": 25 + self.nivel*0.1 + daño_base,
                "mana": -30, 
                "vida": 0,
                "armadura": 0,
            },
            "recuperar mana": {
                "mana": 200
            }
        }
        self.armas = ["baston"] # Armas que puede utilizar el personaje

class Guerrero(Personaje):
    def __init__(self, nombre, vida, daño_base, velocidad_de_ataque, armadura, arma = None, clase = "Guerrero" , nivel=1, mana = 100):
        super().__init__(vida, daño_base, velocidad_de_ataque, armadura, nivel)
        self.nombre = nombre
        self.vida = vida
        self.nivel = nivel
        self.daño = daño_base
        self.velocidadAtaque = velocidad_de_ataque
        self.armadura = armadura
        self.clase = clase
        self.mana = mana + self.nivel*1.5
        self.armadura = self.armadura + 500
        self.vida = self.vida + 100
        self.arma = arma
        self.habilidades = {
            "embate": {
                "daño": 35 + self.nivel*0.1 + daño_base,
                "mana": -15, 
                "vida": 0,
                "armadura": 0,
            },
            "defensa": {
                "daño": 0,
                "mana": -15, 
                "vida": 20,
                "armadura": 50,
            },
            "golpe mortal": {
                "daño": 80 + self.nivel*0.1  + daño_base,
                "mana": -60, 
                "vida": 0,
                "armadura": 0,
            },
            "recuperar mana": {
                "mana": 200
            }
        }
        self.armas = ["espada", "maza", "hacha"]


class Acechador(Personaje):
    def __init__(self, nombre, vida, daño_base, velocidad_de_ataque, armadura, arma = None, clase = "Acechador" ,nivel=1, mana = 300):
        super().__init__(vida, daño_base, velocidad_de_ataque, armadura, nivel)
        self.nombre = nombre
        self.vida = vida
        self.nivel = nivel
        self.daño = daño_base
        self.velocidadAtaque = velocidad_de_ataque
        self.armadura = armadura
        self.clase = clase
        self.arma = arma
        self.mana = mana + self.nivel*1.5
        self.velocidadAtaque = self.velocidadAtaque + 200
        self.habilidades = {
            "puñalada": {
                "daño": 20 + self.nivel*0.1  + daño_base,
                "mana": -15, 
                "vida": 0,
                "armadura": 0,
            },
            "esfumar": {
                "daño": 0,
                "mana": -100, 
                "vida": 200,
                "armadura": 0,
            },
            "afilar": {
                "daño": 0 + self.nivel*0.1 + daño_base,
                "mana": -40, 
                "vida": 0,
                "armadura": 0,
            },
            "recuperar mana": {
                "mana": 200
            }
        }
        self.armas = ["daga"] 

#--------------- Creacion de armas para los personajes ------------------------

class Armas:
    def __init__(self, nombre, tipo, daño, velocidad):
        self.nombre = nombre
        self.tipo = tipo
        self.daño = daño
        self.velocidad = velocidad

    def __repr__(self):
        return f'{self.nombre} |   tipo: {self.tipo} |  daño: {self.daño} |  velocidad de ataque: {self.velocidad}'

class Bastones(Armas):
    def __init__(self, nombre, tipo = "baston", daño = 10, velocidad = 10):
        super().__init__(nombre, tipo, daño, velocidad)
        self.nombre = nombre

class Espadas(Armas):
    def __init__(self, nombre, tipo = "espada", daño = 70, velocidad = 40):
        super().__init__(nombre, tipo, daño, velocidad)
        self.nombre = nombre

class Dagas(Armas):
    def __init__(self, nombre, tipo = "daga", daño = 60, velocidad = 100):
        super().__init__(nombre, tipo, daño, velocidad)
        self.nombre = nombre

class Hachas(Armas):
    def __init__(self, nombre, tipo = "hacha", daño = 80, velocidad = 10):
        super().__init__(nombre, tipo, daño, velocidad)
        self.nombre = nombre

class Maza(Armas):
    def __init__(self, nombre, tipo = "maza", daño = 100, velocidad = 90):
        super().__init__(nombre, tipo, daño, velocidad)
        self.nombre = nombre

# -------------- Definimos los monstruos con los que lucharemos -----------------

class Monstruos:
    def __init__(self, nombre, dificultad, vida, experiencia, velocidad, daño):
        self.nombre = nombre
        self.dificultad = dificultad
        self.vida = vida
        self.experiencia = experiencia # Cantidad de nivel que subes al derrotarlo
        self.velocidad = velocidad
        self.daño = daño

    def __repr__(self):
        return f'{self.nombre} |   vida: {self.vida} |  dificultado: {self.dificultad} |  daño: {self.daño} |  velocidad de ataque: {self.velocidad} |  recompensa de experiencia: {self.experiencia}'


# -------------------Elementos creados para el juego, monstruos y armas--------------------

cthulhu = Monstruos(nombre="cthulhu", dificultad="dificil", vida= 1000, experiencia= 10, velocidad= 30, daño=30)
Leon_de_Amenea = Monstruos(nombre="Leon de Amenea", dificultad="media", vida= 300, experiencia= 7, velocidad= 20, daño=10)
Minotauro = Monstruos(nombre="Minotauro", dificultad="dificil", vida= 2000, experiencia= 50, velocidad= 30, daño=30)

lista_de_monstruos = [cthulhu, Leon_de_Amenea, Minotauro]

Baston_de_Gandalf = Bastones("Baston de Gandalf", "baston", 200, 10)
Excalibur = Espadas("Escalibur", "espada", 100, 70)
Mjölnir = Maza("Mjölnir", "maza", 90, 40)
Tizona = Dagas("Tizona", "daga", 40, 300)
Fragarach = Hachas("Fragarach", "hacha", 90, 40)

lista_de_armas = [Baston_de_Gandalf, Excalibur, Mjölnir, Tizona, Fragarach]

# ----------------------funciones del juego-----------------

# ----------------------Creacion de Personajes-------------------, he intentado separar la funcion crear_personake() en 3 funciones pero da muchos errores con la herencia (complica las cosas innecesariamente a pesar de ser una buena practica)

def crear_personaje(id): # el id sera un numero identificativo en el nombre
    try:
        nombre_personaje = f'personaje{id}'
        daño_personaje = random.randint(1, 200) #El daño, la velocidad y la armadura tendran 200 puntos que se repartiran de forma aleatoria
        if daño_personaje == 200:
            velocidad_personaje = 0
            armadura_personaje = 0
        else:
            velocidad_personaje = random.randint(0, 200 - daño_personaje)
            armadura_personaje = 200 - daño_personaje - velocidad_personaje
        puntos_totales = 200 - daño_personaje - velocidad_personaje - armadura_personaje
        if puntos_totales < 0: # Por si acaso, aunque es imposible que entre aqui
            crear_personaje(id)
        else: # Para este else podria haber hecho otra funcion pero las he tenido que unir porque daba demasiados errores
            seleccion = random.choices([1, 2, 3])[0] # El cero es necesario porque random.choices siempre devuelve una lista con un elemento
            if seleccion == 1:
                personaje = Guerrero(vida=250, daño_base=daño_personaje, velocidad_de_ataque=velocidad_personaje, armadura=armadura_personaje, nombre=nombre_personaje)
            elif seleccion == 2:
                personaje = Mago(vida=100, daño_base=daño_personaje, velocidad_de_ataque=velocidad_personaje, armadura=armadura_personaje, nombre=nombre_personaje)
            elif seleccion == 3:
                personaje = Acechador(vida=200, daño_base=daño_personaje, velocidad_de_ataque=velocidad_personaje, armadura=armadura_personaje, nombre=nombre_personaje)
        return personaje
    # en cada personaje las caracteristicas escalaran de forma diferente
    except:
        crear_personaje(id)

# ----------------------funciones de lucha-------------------

def seleccionar_arma(lista_de_armas, personaje_seleccionado): # El arma da demasiados problemas, dejarla como un objeto no anidado a la clase y pasarlo como parametro a la funcion lucha
    while True:
        decision_arma = random.choices([1, 2, 3, 4, 5])[0] - 1
        arma_seleccionada = lista_de_armas[decision_arma] # las listas tanto de armas como de monstruos, estan ya creadas en esste mismo archivo
        if arma_seleccionada.tipo in personaje_seleccionado.armas: # solo puede elegir un arma que permita su clase usar (ejemplo: si es mago solo puede usar baston, si es acechador solo dagas y si es guerrero, mazas, espadas o hachas) 
            break # Esta es la unica forma de resolver el problema con el NoneType, obligar a que el arma seleccionada sea correcta una vez terminado el while
    return arma_seleccionada 

def seleccion_de_batalla(personaje, monstruo, lista_armas = lista_de_armas): # seleccionamos monstruo personaje y arma para luchar
    # Es necesario instaciar los monstruos aqui para que al hacer la recopilacion de datos se reinnicien sus vidas
    # En cambio con las armas no es necesario porque no cambian ninguna propiedad
    cthulhu = Monstruos(nombre="cthulhu", dificultad="dificil", vida= 1000, experiencia= 10, velocidad= 30, daño=30)
    Leon_de_Amenea = Monstruos(nombre="Leon de Amenea", dificultad="media", vida= 300, experiencia= 7, velocidad= 20, daño=10)
    Minotauro = Monstruos(nombre="Minotauro", dificultad="dificil", vida= 2000, experiencia= 50, velocidad= 30, daño=200)

    lista_de_monstruos = [cthulhu, Leon_de_Amenea, Minotauro]
    
    try:
        monstruo_seleccionado = lista_de_monstruos[monstruo] # por parametro tendra que recibir un entero que funcionara como indice en la lista de monstruos ya creada arriba
        arma = seleccionar_arma(lista_armas, personaje)
        batalla = lucha(personaje, monstruo_seleccionado, arma)
        return batalla
    except:
        seleccion_de_batalla(lista_personajes, monstruo, lista_de_monstruos, lista_de_armas)

def lucha(personaje, monstruo, arma): # Logica del combate
    dicc_resultados = { # asignamos esto aqui porque cuando empiece el combate (el bucle while de abajo) los atributos del personaje y del monstruo van a cambiar
        "personaje": {
            "nombre": personaje.nombre,
            "daño": personaje.daño,
            "armadura": personaje.armadura,
            "velocidad": personaje.velocidadAtaque,
            "vida": personaje.vida,
            "clase": personaje.clase,
            "Arma usada": arma.nombre,
            "Monstruo combatido": monstruo.nombre,
            "victorias": 0 # Esta clave nos ayudara a analizar el ratio de victorias
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
        }
    }  #Aqui estara toda la informacion para posteriormente analizarla en el modelo
    turnos_personaje = 0
    turnos_monstruo = 0
    continuar = True
    while continuar: # El bucle terminara cuando uno de los dos (tu o el monstruo) se quede sin vida, en ese momento continuar = info[1] = False
        turno = seleccionar_turno(personaje.velocidadAtaque + arma.velocidad, monstruo.velocidad) # selecciona de forma aleatoria a quien le toca
        if turno == "tu": # si turno_personaje() ha devuelto "tu", ser tu turno en el que ataques y el monstruo reciba daño
            info = turno_personaje(personaje, monstruo, arma)
            continuar = info[1] # innfo es una lista donde estara el ganador, en caso de haber terminado el combate y un boleano que determina si alguno de los elementos (el monstruo o tu) sigue con una vida superior a 0 puntos
            turnos_personaje += 1
        else:
            info = turno_monstruo(personaje, monstruo) # turno_monstruo retorna una lista donde el primer elemento es un true o in false para ver si se ha terminado el combate o no
            continuar = info[1] 
            turnos_monstruo += 1

    dicc_resultados["ganador"] = info[0]
      # cuando termine el bucle asignaremos la variable ganador dentro de la informacion
    dicc_resultados["personaje"]["turnos"] = turnos_personaje
    dicc_resultados["monstruo"]["turnos"] = turnos_monstruo # turnos usados de cada entidad, ns si lo necesitaremos para el modelo pero siempre esta bien tener esta informacion
    return dicc_resultados


def seleccionar_turno(velocidad_personaje, velocidad_monstuo): # a pesar de ser aleatoria la eleccion cuanto mas velocidad tengas mas probabilidad tienes de que salte tu turno
    diff = abs(velocidad_monstuo - velocidad_personaje)
    probabilidad_base = 1/(diff + 1)

    probabilidad_personaje = probabilidad_base *(1.0  +  velocidad_personaje*0.01)
    probabilidad_monstruo = probabilidad_base *(1.0  +  velocidad_monstuo*0.01)
    total_probabilidad = probabilidad_monstruo + probabilidad_personaje
    
    probabilidad_personaje /= total_probabilidad
    probabilidad_monstruo /= total_probabilidad
    
    seleccion_de_turno = random.choices(["tu", "monstruo"], weights=[probabilidad_personaje, probabilidad_monstruo])[0] # El 0 es necesario porque devuelve una lista con un elemento
    
    return seleccion_de_turno # devolvera "tu" o "monstruo"

def turno_monstruo(personaje, monstruo): # si ha salido esta funcion es porque es el turno del monstruo (el monstruo ataca y tu recibes daño)
    ataque = monstruo.daño
    vida_personaje = personaje.vida - ataque
    personaje.vida -= ataque
    if vida_personaje < 0: # entra aqui si el monstruo te ha matado
        #print(f"\nEl ataque de {ataque} puntos de daño de {monstruo.nombre} te afecto dejandote sin vida") # Esto no lo he querido borrar por si en algun momento interesa conocer el combate turno por turno
        continuar = False
        ganador = "monstruo"
        info = [ganador, continuar]
        return info
    else:
        #print(f"\nEl ataque de {ataque} puntos de daño de {monstruo.nombre} te afecto dejandote con {vida_personaje} puntos vida")
        continuar = True
        ganador = "nadie" # Este valor es indiferente porque siempre que continuar sea true, la variable ganador no quedara asignada porque el bucle de la funcion lucha() no habra terminado, tiene el valor "nadie" solo para evitar errores de codigo
        info = [ganador, continuar]
        return info 

def turno_personaje(personaje, monstruo, arma): # Aqui entras si ha saltado "tu" en la seleccion de turno, tu haces daño y el monstruo recibe, tambien interactua el arma que tengas
    ataque = personaje.daño + arma.daño
    vida_monstruo = monstruo.vida - ataque
    monstruo.vida -= ataque
    if vida_monstruo < 0:
        #print(f"\nSu ataque de {ataque} de daño afecto a {monstruo.nombre} matandolo completamente y ganando el combate")
        continuar = False
        ganador = "personaje"
        info = [ganador, continuar]
        return info
    else:
        #print(f"\nSu ataque de {ataque} de daño afecto a {monstruo.nombre} dejandole con {monstruo.vida}") # Esto no lo he querido borrar por si en algun momento interesa conocer el combate turno por turno
        continuar = True
        ganador = "nadie"
        info = [ganador, continuar]
        return info