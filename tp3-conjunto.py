import soundPlayer as pysounds
import cmd

FUN_SOUND={'SQ':pysounds.SoundFactory.get_square_sound,
'TRIA':pysounds.SoundFactory.get_triangular_sound,
'SINE':pysounds.SoundFactory.get_sine_sound,
'NOISE':pysounds.SoundFactory.get_noise_sound}


comandos_archivos = {canal : 'C',
tiempo : 'T', descripcion_track : 'S',
descripcion_marca : 'N',
apagado = '#',
prendido = '.'}

###################

class _Nodo:
	def __init__(self, dato = None, prox = None):
		self.dato = dato
		self.prox = prox
	def __str__(self):
		return str(self.dato)


class Pila:
	"""REPRESENTA UNA PILA CON OPERACIONES DE APILAR, DESAPILAR Y VERIFICAR SI ESTA VACIA."""
	def __init__(self):
		"""INICIALIZA LA PILA"""
		self.contenido=[]

	def apilar(self,elem):
		"""APILA UN ELEMENTO DE LA PILA"""
		self.contenido.append(elem)

	def esta_vacia(self):
		"""DEVUELVE TRUE SI LA PILA ESTA VACIA"""
		return len(self.contenido)==0

	def desapilar(self):
		"""DESAPILA UN ELEMENTO DE LA PILA"""
		if self.esta_vacia():
			raise Exception('la pila esta vacia')
		return self.contenido.pop()
	def ver_tope(self):
		"""DEVUELVE EL TOPE DE LA PILA"""
		if self.esta_vacia():
			raise Exception('la pila esta vacia')
		return self.contenido[-1]

#Lista Enlazada

class ListaEnlazada:
	"""MODELA UNA LISTA ENLAZADA"""
	def __init__(self):
		"""CREA UNA LISTA ENLAZADA VACIA"""
		self.prim = None
		self.len = 0
	
	def pop(self, i=None ):
		"""ELIMINA EL NODO DE LA POSICION I Y DEVUELVE EL DATO OCNTENIDO.
		SI I ESTA FUERA DE RANGO SE LEVANTA LA EXCEPCION INDEXERROR
		SI NO SE RECIBE LA POSICION, DEVUELVE EL ULTIMO ELEMENTO"""
		if i is None:
			i = self.len - 1
		if i < 0 or i > self.len:
			raise IndexError("Indice fuera de rango")
		if i == 0:
			dato = self.prim.dato
			self.prim = self.prim.prox
		else:
			n_ant = self.prim
			n_act = n_ant.prox
			for pos in range(1, i):
				n_ant = n_act
				n_act = n_ant.prox

			dato = n_act.dato
			n_ant.prox = n_act.prox
		self.len -= 1
		return dato

	def remove(self,x):
		"""BORRA LA PRIMERA APARICION DEL VALOR X EN LA LISTA.
		 SI X NO ESTA EN LA LISTA, LEVANTA VALUERROR"""
		if self.len == 0:
			raise ValueError("Lista vacia")
		if self.prim.dato == x:
			self.prim=self.prim.prox
		else:
			n_ant = self.prim
			n_act = n_ant.prox
			while n_act is not None and n_act.dato != x:
				n_ant = n_act
				n_act = n_ant.prox
			if n_act == None:
				raise ValueError("El valor no esta en la lista")

			n_ant.prox = n_act.prox
		self.len -= 1


	def insert(self,i,x):
		"""INSERTA EL ELEMENTO X EN LA POSICION I. SI LA POSICION ES INVALIDA,
		LEVANTA INDEXERROR"""
		if i < 0 or i > self.len:
			raise IndexError("Posicion invalida")

		nuevo = _Nodo(x)

		if i == 0:
			nuevo.prox = self.prim
			self.prim = nuevo

		else:
			n_ant = self.prim
			for pos in range(1, i):
				n_ant = n_ant.prox
			nuevo.prox = n_ant.prox
			n_ant.prox = nuevo

		self.len += 1


	def append(self,x):
		"""AGREGA UN ELEMENTO AL FINAL DE LA LISTA"""
		nuevo = _Nodo(x)

		if self.len == 0:
			self.prim = nuevo
		
		else:
			n_ant = self.prim
			while n_ant.prox != None:
				n_ant = n_ant.prox
			n_ant.prox = nuevo

		self.len +=1


	def index(self,x):
		"""DEVUELVE EL INDICE DE LA PRIMER APARICION DE X"""
		if self.prim.dato == x:
			return 0

		n_ant = self.prim
		contador = 1
		while n_ant.prox != None and n_ant.prox.dato != x:
			n_ant = n_ant.prox
			contador += 1
		if n_ant.prox is None:
			raise ValueError("No se encuentra el elemento en la lista")

		return contador

	def __iter__(self):
		return _IteradorLE(self.prim)

class _IteradorLE:
    '''Iterador de Lista Enlazada'''
    
    def __init__(self,prim):
        '''Crea un iterador a partir del parametro prim '''
        self.actual=prim
        self.ant=Pila()
        
    def __next__(self):
        '''Avanza, si es posible, el iterador'''
        if not self.actual:
            raise StopIteration
        dato=self.actual.dato
        self.ant.apilar(self.actual)
        self.actual=self.actual.prox
        return dato

    def anterior(self):
        '''Retrocede,si es posible, el iterador'''
        if self.ant.esta_vacia():
            raise StopIteration
        nodo=self.ant.desapilar()
        self.actual=nodo
        return nodo.dato

    def iter_insertar(self,elem):
        '''inserta un elemento en la posicion actual del iterador'''
        nodo=_Nodo(elem)
        nodo.prox=self.actual.prox
        self.actual.prox=nodo
        self.__next__()




class _Marca:
	'''Representacion de una marca musical, con atributos de tiempo de duracion
	y notas a sonar en este'''
	def __init__(self,tiempo):
		'''Crea el objeto marca recibiendo el atributo tiempo'''
		self.tiempo = tiempo
		self.audio = []

	def agregar_audio(self,refnota):
		'''Agrega una referencia numerica a la posicion del track de nota a sonar'''
		self.audio.append(refnota)

	def quitar_audio(self,refnota):
		'''Modifica la configuracion de una nota existente'''
		if refnota in self.audio:
			self.audio.remove(refnota)


class _Track:
	'''Representacion de un track de sonido formado por la funcion que lo genera,
	la frecuencia del sonido y el volumen de este'''
	def __init__(self,funcion,frecuencia,volumen):
		'''Crea un track recibiendo los atributos funcion, frecuencia, volumen'''
		self.fun=funcion
		self.frec=frecuencia
		self.vol=volumen


class Cancion:
	'''OBJETO QUE REPRESENTA LOS ELEMENTOS DE UNA CANCION Y UNA FORMA DE RECORRERLOS, SIENDO ESTOS ELEMENTOS
	TRACKS DE SONIDOS Y MARCAS DE TIEMPO'''
	def __init__(self):
		"""INICA EL OBJETO CANCION VACIO"""
		self.tracks =[]
		self.marcas = ListaEnlazada()
		self.pos = None #iterador de la lista enlazada de marcas, se actualiza al agregar 
						#marcas y comienza como None ya que la lista comienza vacia en una
						#nueva cancion

	def agregar_track(self,lctrack,posicion=None):
		"""AGREGA UN TRACK RECIBIDO COMO UNA LISTA DE CADENAS"""
		n_track=_Track(lctrack[0],float(lctrack[1]),float(lctrack[2]))
		if posicion is None:
			self.tracks.append(n_track)
		else:
			self.tracks.insert(posicion,n_track)

	def quitar_track(self,posicion):
		"""QUITA UN TRACK"""
		self.tracks.pop(posicion)

	def agregar_marca(self,tiempo,antosig=None):
		"""AGREGA UNA MARCA EN UNA CANCION"""
		Nuevo  = _Marca(tiempo)
		if antosig=='ant':
			self.mov_atras()
		elif antosig=='sig':
			self.mov_adelante()
		if self.marcas.prim == None:
			self.marcas.append(Nuevo)
			self.pos = iter(self.marcas)
		else:		
			self.pos.iter_insertar(Nuevo)

	def trackonoff(self,n,onoff):
		"""HABILITA O NO UN TRACK"""
		if onoff == "on":
			next(self.pos).agregar_audio(n)
		else:
			next(self.pos).quitar_audio(n)
		self.pos.anterior()

	def mov_adelante(self,cantmov=1):
		"""MUEVA UNA O MAS POSICIONES ADELANTE AL CURSOR"""
		try :
			while cantmov>0:
				next(self.pos)
				cantmov -=1
		except StopIteration:
			return

	def mov_atras(self,cantmov=1):
		"""MUEVE  UNA O MAS POSICIONES ATRAS AL REPRODUCTOR"""
		try:
			while cantmov>0:
				self.pos.anterior()
				cantmov-=1
		except StopIteration:
			return	

		
class Reproductor:
	'''INTERPRETE DEL OBJETO CANCION, CAPAZ DE CREAR SONIDOS A PARTIR DE ESTE'''

	def __init__(self):
		"""INICIA EL OBJETO REPRODUCTOR VACIO"""
		self.cancion = Cancion()
		self.sonidos = []
		self.cursor = None 
		self.nom_cancion = None

	def reiniciar_cursor(self):
		"""REINICIA EL CURSOR DEL REPRODUCTOR"""
		try:
			while True:
				self.cursor.anterior()
		except StopIteration:
			 return


	def cargar_de_archivo(self,archivoplp):
		"""CARGA A MEMORIA Y VALIDA UN ARCHIVO CON FORMATO PPL"""
		cancionarch=Cancion()
		with open(archivoplp,'r') as archivo:
			archivo.readline()#salteo el header del archivo
			for linea in archivo:
				line = linea.rstrip('\n')
				field , data = line.split(",")
				if field == comandos_archivos[canal]:
					continue
				elif field == comandos_archivos[descripcion_track]:
					if not validar_track(data,'|'):
						raise IOError
					track=data.split('|')
					cancionarch.agregar_track(track)
				elif field ==comandos_archivos[tiempo]:
					if not is_float(data):
						raise IOError
					tiempo = float(data)
				elif field == comandos_archivos[descripcion_marca]:
					sonidos=data
					if len(sonidos)>len(cancionarch.tracks):
						raise IOError
					cancionarch.agregar_marca(tiempo)
					for i in range (len(sonidos)):
						if sonidos[i] == comandos_archivos[apagado]:
							cancionarch.trackonoff(i,"on")
						elif sonidos[i] not in '#·':
							raise IOError
		self.nom_cancion=archivoplp
		self.cancion=cancionarch
		self.cursor = self.cancion.pos



	def guardar_archivo(self,nombre=None):
		"""GUARDA EN EL DIRECTORIO EL ARCHIVO"""
		if not nombre:
			nombre=self.nom_cancion
		if self.cursor==None:
			raise Exception('Cancion vacia')
		self.reiniciar_cursor()
		with open(nombre,'w') as archivo:
			archivo.write('FIELD,DATA\n')
			archivo.write(comandos_archivos[canal]+',{}\n'.format(len(self.cancion.tracks)))
			for track in self.cancion.tracks:
				archivo.write(comandos_archivos[descripcion_track]+',{}|{}|{}\n'.format(track.fun,track.frec,track.vol))
			tiempos=Pila()
			tiempos.apilar(0)
			for marca in self.cancion.marcas:
				if marca.tiempo!=tiempos.ver_tope():
					archivo.write(comandos_archivos[tiempo]+',{}\n'.format(marca.tiempo))
				tiempos.apilar(marca.tiempo)
				notasplp=[]
				for i in range(len(self.cancion.tracks)):
					if i in marca.audio:
						notasplp.append(comandos_archivos[apagado])
					else:
						notasplp.append(comandos_archivos[prendido])
				archivo.write(comandos_archivos[descripcion_marca]+',{}\n'.format(''.join(notasplp)))



	def crear_cancion(self,nombre=None):
		"""CREA UNA CANCION VACIA"""
		self.cancion=Cancion()
		self.nom_cancion= nombre


	def crear_sonidos(self):
		"""CREA SONIDOS SEGUN MODULO PYSOUND"""
		for track in (self.cancion.tracks):
			if 'SQ' in track.fun:
				func=FUN_SOUND["SQ"]
				A=int(track.fun.strip('SQ'))/100#parametro de sonido 'square' no se que signifique
				i=func(float(track.frec),float(track.vol),A)
			else:
				func=FUN_SOUND[track.fun]
				i=func(float(track.frec),float(track.vol))
			self.sonidos.append(i)

	def _reproducirsonidos(self,player):
		'''Recibe un reproductor con sonidos,y reproduce la marca actual y avanza una marca si es posible'''
		marca=next(self.cursor)
		if not marca:
			raise StopIteration
		sonidos=[]
		for i in marca.audio:
			if i < len(self.sonidos):
				sonidos.append(self.sonidos[i])
			else:
				marca.audio.remove(i)
		player.play_sounds(sonidos,marca.tiempo)

	def reproducir(self,cuanto=(None,None)):
		"""DEVUELVE LA REPRODUCCION DEL ARCHIVO. LA FORMA EN LA QUE SE REPRODUZCA DEPENDE DEL
		PARAMETRO CUANTO INGRESADO"""
		self.crear_sonidos()
		sp = pysounds.SoundPlayer(len(self.sonidos))
		if cuanto[0]==None:
			self.cursor=self.cancion.pos
			self._reproducirsonidos(sp)
			self.cursor.anterior()

		elif cuanto[0]=="all":
			self.reiniciar_cursor()
			try:
				while True:
					self._reproducirsonidos(sp)
			except StopIteration:
				self.reiniciar_cursor()
		elif cuanto[0] == "marcas":
			acum=0
			try:
				self.cursor=self.cancion.pos
				while True:
					self._reproducirsonidos(sp)
					acum += 1
					if acum > cuanto[1]:
						break
			except StopIteration:
				print('Fin de cancion')
			finally:
				while acum > 0:
					acum -= 1
					self.cancion.mov_atras()
		elif cuanto[0] == "tiempo":
			acum=0
			self.reiniciar_cursor()
			try:
				while True:
					self._reproducirsonidos(sp)
					acum += self.cursor.anterior().tiempo
					next(self.cursor)
					if acum >= cuanto[1]:
						break
			except StopIteration:
				print('fin de cancion')
			finally:
				self.reiniciar_cursor()

def validar_track(trackstr,separador):
	'''Verifica que un track ingresado como cadena sea correcto'''
	validar=False
	for funcion in ('SQ','TRIA','SINE','NOISE'):
		if funcion in trackstr:
			if validar==True:#no se debe ingresar mas de una funcion por track
				return False
			validar=True
	if not validar:
		return False
	track = trackstr.split(separador)
	if 'SQ' in track[0]:
		if not track[0][2:].isdigit():
			return False
	if len(track)!= 3:
		return False
	track[0]=track[0]
	if not is_float(track[1]):
		return False
	if not is_float(track[2]):
		return False
	return True 

def is_float(cadena): #creo esta funcion para validar numeros flotantes ingresados
	'''Verifica si una cadena se puede transformar en float'''
	try:
		float(cadena)
		return True
	except ValueError:
		return False

class Shell(cmd.Cmd):
	
	intro = "Bienvenido a Sounds of Cyber City.\n"
	"Ingrese help o ? para listar los comandos.\n"
	prompt = "*>>" 
	def do_LOAD(self,archivo):
		"""CARGA ARCHIVO PLP"""
			rp.cargar_de_archivo(archivo)
		if Exception:
			print('Error al cargar el archivo, verifique el formato y la ubicacion de este')
	def do_STORE(self,archivo):
		"""GUARDA ARCHIVO PLP"""
		if archivo:
			rp.guardar_archivo(archivo)
		elif rp.nom_cancion == None:
			raise Exception('''Debe ponerle nombre a su cancion para guardarla: STORE <nombre>''')
		else:
			rp.guardar_archivo()
		if Exception:
			print("Error")
	def do_STEP(self,parametro = None):
		"""AVANZA UNA POSICION DE MARCA SI ES POSIBLE"""
		if rp.cancion.pos==None:
				raise Exception('Cancion Vacia')
			rp.cancion.mov_adelante()
			rp.cursor=rp.cancion.pos
		if Exception:
			print("Error")
	def do_BACK(self,parametro = None):
		"""RETROCEDE A LA MARCA DE TIMPO ANTEROIR SI ES POSIBLE"""
		if rp.cancion.pos == None:
			raise Exception('Cancion vacia')
		rp.cancion.mov_atras()
		rp.cursor=rp.cancion.pos
		if Exception:
			print("Error")
	def do_STEPM(self,n):
		"""AVANZA N MARCAS HACIA ADELANTE"""
		if not n.isdigit():
			raise ValueError('Debe ingresar un numero valido')
		if rp.cancion.pos == None:
			raise Exception('Cancion vacia')
		rp.cancion.mov_adelante(int(n))
		rp.cursor=rp.cancion.pos
		if Exception:
			print ("Error")
	def do_BACKM(self,n):
		"""RETROCEDE N MARCAS HACIA ATRAS"""
		if not n.isdigit():
			raise ValueError('Debe ingresar un numero valido')
		if rp.cancion.pos==None:
			raise Exception('Cancion vacia')
		rp.cancion.mov_atras(int(n))
		rp.cursor=rp.cancion.pos
		if Exception:
			print ("Error")
	def do_TRACKADD(self,trackingresado):
		"""AGREGA UN TRACK DE SONIDO INDICADO, DEBE ESTAR EN FORMATO <FUNCION> <FRECUENCIA> <VOLUMEN>
		SEPARADOS SOLO POR ESPACIOS, LAS FUNCIONES DEBEN SER INGRESADAS EN MAYUSCULAS"""
		if not validar_track(trackingresado," "):
			raise ValueError('Error al ingresar os datos, verifique que haya ingresado el track correctamente') 
		track=trackingresado.split(' ')
		rp.cancion.agregar_track(track)
		if Exception:
			print("Error")
	def do_TRACKDEL(self,n):
		"""ELIMINA TRACK POR NUMERO"""
		if not n.isdigit():
			raise Exception('Debe ingresar un numero valido')
		elif int(n)> len(rp.cancion.tracks) or int(n) < 1:
			raise ValueError('No existe el track indicado')
		respuesta=input('''Advertencia esto eliminara el track en la posicion {} 
y el track en la posicion {} ,si existe, tomara su lugar, y asi con los siguientes.
Si solo desea desactivar el track en una marca use el comando TRACKOFF 
¿Esta seguro que desea seguir? s/n \n'''.format(n,int(n)+1))
		if respuesta.upper() == 'S':
			rp.cancion.quitar_track(int(n)-1)
		if Exception:
			print("Error")
	def do_MARKADD(self,tiempo):
		"""AGREGA UNA MARCA DE TIEMPO DE LA DURACION ESTABLECIDA. ORIGINALMENTE TODOS LOS TRACKS ARRANCAN COMO 
		DESHABILITADOS"""
		if not is_float(tiempo):
			raise ValueError('Verifique el valor de tiempo ingresado')
		rp.cancion.agregar_marca(float(tiempo))
		if rp.cursor==None:
			rp.cursor=rp.cancion.pos
		if Exception:
			print("Error")
	def do_MARKADDNEXT(self,tiempo):
		"""IGUAL QUE MARKADD PERO LA INSERTA LUEGO DE LA MARCA EN LA CUAL ESTA ACTUALMENTE EL CURSOR"""
		if not is_float(tiempo):
			raise ValueError('Verifique el valor de tiempo ingresado')
		rp.cancion.agregar_marca(float(tiempo),"sig")
		rp.cursor=rp.cancion.pos
		if Exception:
			print("Error")
	def do_MARKADDPREV(self,tiempo):
		"""IGUAL QUE MARKADD PERO LA INSERTA EN LA ANTERIOR EN LA CUAL ESTA ACTUALMENTE EL CURSOR"""
		if not is_float(tiempo):
			raise ValueError('Verifique el valor de tiempo ingresado')
		rp.cancion.agregar_marca(float(tiempo),"ant")
		rp.cursor=rp.cancion.pos
		if Exception:
			print ("Error")
	def do_TRACKON(self,n):
		"""HABILITA EL TRACK DURANTE LA MARCA DE TIEMPO EN LA CUAL ESTA PARADA EL CURSOR"""
		if not n.isdigit():
			raise ValueError('Debe ingresar un numero de track valido')
		if int(n)<1 or int(n)>len(rp.cancion.tracks):
			raise ValueError('No se encuentra el track, verifique el valor ingresado')
		rp.cancion.trackonoff(int(n)-1,"on")
		if Exception:
			print("Error")
	def do_TRACKOFF(self,n):
		"""OPERACION INVERSA A TRACKON"""
		if not n.isdigit():
			raise ValueError('Debe ingresar un numero de track valido')
		if int(n)<1 or int(n)>len(rp.cancion.tracks):
			raise ValueError('No se encuentra el track, verifique el valor ingresado')
		rp.cancion.trackonoff(int(n)-1,"off")
		if Exception:
			print("Error")
	def do_PLAY(self, parametro = None):
		"""REPRODUCE LA MARCA ACTUAL"""
		if rp.cursor==None:
			raise Exception('El reproductor esta vacio')
		rp.reproducir()
		if Exception:
			print("Error")
	def do_PLAYALL(self, parametro = None):
		"""REPRODUCE LA CANCION COMPLETA DESDE EL INICIO"""
		if rp.cursor==None:
			raise Exception('El reproductor esta vacio')
		rp.reproducir(('all',None))
		if Exception:
			print("Error")
	def do_PLAYMARKS(self,nmarcas):
		"""REPRODUCE LA CANTIDAD DE MARCAS ESTABLECIDAS"""
		if not nmarcas.isdigit():
			raise ValueError('Verifique el valor ingresado')
		if rp.cursor==None:
			raise Exception('El reproductor esta vacio')
		rp.reproducir(("marcas",int(nmarcas)))
		if Exception:
			print("Error")
	def do_PLAYSECONDS(self,nsegundos):
		"""REPRODUCE EL INICIO HASTA LA CANTIDAD DE N TIEMPO ESTABLECIDA EN SEGUNDOS"""
		if not is_float(nsegundos):
			raise ValueError('Verifique el valor ingresado para los segundos')
		if rp.cursor==None:
			raise Exception('El reproductor esta vacio')
		rp.reproducir(("tiempo",float(nsegundos)))
		if Exception:
			print("Error")
	def do_exit(self,arg):
		"""SALIDA DEL PROGRAMA"""
		return True
	def do_NEW(self, nombre = None):
		"""CREA UNA CANCION NUEVA VACIA"""
		resp= input('Esto creara una nueva cancion vacia en el lugar de la actual ¿esta seguro que desea seguir? S/N\n').upper()
		if resp == 'S':
			rp.crear_cancion(nombre)

rp = Reproductor()
Shell().cmdloop()import soundPlayer as pysounds
import cmd

FUN_SOUND={'SQ':pysounds.SoundFactory.get_square_sound,
'TRIA':pysounds.SoundFactory.get_triangular_sound,
'SINE':pysounds.SoundFactory.get_sine_sound,
'NOISE':pysounds.SoundFactory.get_noise_sound}

###################

class _Nodo:
	def __init__(self, dato = None, prox = None):
		self.dato = dato
		self.prox = prox
	def __str__(self):
		return str(self.dato)


class Pila:
	"""REPRESENTA UNA PILA CON OPERACIONES DE APILAR, DESAPILAR Y VERIFICAR SI ESTA VACIA."""
	def __init__(self):
		"""INICIALIZA LA PILA"""
		self.contenido=[]

	def apilar(self,elem):
		"""APILA UN ELEMENTO DE LA PILA"""
		self.contenido.append(elem)

	def esta_vacia(self):
		"""DEVUELVE TRUE SI LA PILA ESTA VACIA"""
		return len(self.contenido)==0

	def desapilar(self):
		"""DESAPILA UN ELEMENTO DE LA PILA"""
		if self.esta_vacia():
			raise Exception('la pila esta vacia')
		return self.contenido.pop()
	def ver_tope(self):
		"""DEVUELVE EL TOPE DE LA PILA"""
		if self.esta_vacia():
			raise Exception('la pila esta vacia')
		return self.contenido[-1]

#Lista Enlazada

class ListaEnlazada:
	"""MODELA UNA LISTA ENLAZADA"""
	def __init__(self):
		"""CREA UNA LISTA ENLAZADA VACIA"""
		self.prim = None
		self.len = 0
	
	def pop(self, i=None ):
		"""ELIMINA EL NODO DE LA POSICION I Y DEVUELVE EL DATO OCNTENIDO.
		SI I ESTA FUERA DE RANGO SE LEVANTA LA EXCEPCION INDEXERROR
		SI NO SE RECIBE LA POSICION, DEVUELVE EL ULTIMO ELEMENTO"""
		if i is None:
			i = self.len - 1
		if i < 0 or i > self.len:
			raise IndexError("Indice fuera de rango")
		if i == 0:
			dato = self.prim.dato
			self.prim = self.prim.prox
		else:
			n_ant = self.prim
			n_act = n_ant.prox
			for pos in range(1, i):
				n_ant = n_act
				n_act = n_ant.prox

			dato = n_act.dato
			n_ant.prox = n_act.prox
		self.len -= 1
		return dato

	def remove(self,x):
		"""BORRA LA PRIMERA APARICION DEL VALOR X EN LA LISTA.
		 SI X NO ESTA EN LA LISTA, LEVANTA VALUERROR"""
		if self.len == 0:
			raise ValueError("Lista vacia")
		if self.prim.dato == x:
			self.prim=self.prim.prox
		else:
			n_ant = self.prim
			n_act = n_ant.prox
			while n_act is not None and n_act.dato != x:
				n_ant = n_act
				n_act = n_ant.prox
			if n_act == None:
				raise ValueError("El valor no esta en la lista")

			n_ant.prox = n_act.prox
		self.len -= 1


	def insert(self,i,x):
		"""INSERTA EL ELEMENTO X EN LA POSICION I. SI LA POSICION ES INVALIDA,
		LEVANTA INDEXERROR"""
		if i < 0 or i > self.len:
			raise IndexError("Posicion invalida")

		nuevo = _Nodo(x)

		if i == 0:
			nuevo.prox = self.prim
			self.prim = nuevo

		else:
			n_ant = self.prim
			for pos in range(1, i):
				n_ant = n_ant.prox
			nuevo.prox = n_ant.prox
			n_ant.prox = nuevo

		self.len += 1


	def append(self,x):
		"""AGREGA UN ELEMENTO AL FINAL DE LA LISTA"""
		nuevo = _Nodo(x)

		if self.len == 0:
			self.prim = nuevo
		
		else:
			n_ant = self.prim
			while n_ant.prox != None:
				n_ant = n_ant.prox
			n_ant.prox = nuevo

		self.len +=1


	def index(self,x):
		"""DEVUELVE EL INDICE DE LA PRIMER APARICION DE X"""
		if self.prim.dato == x:
			return 0

		n_ant = self.prim
		contador = 1
		while n_ant.prox != None and n_ant.prox.dato != x:
			n_ant = n_ant.prox
			contador += 1
		if n_ant.prox is None:
			raise ValueError("No se encuentra el elemento en la lista")

		return contador

	def __iter__(self):
		return _IteradorLE(self.prim)

class _IteradorLE:
    '''Iterador de Lista Enlazada'''
    
    def __init__(self,prim):
        '''Crea un iterador a partir del parametro prim '''
        self.actual=prim
        self.ant=Pila()
        
    def __next__(self):
        '''Avanza, si es posible, el iterador'''
        if not self.actual:
            raise StopIteration
        dato=self.actual.dato
        self.ant.apilar(self.actual)
        self.actual=self.actual.prox
        return dato

    def anterior(self):
        '''Retrocede,si es posible, el iterador'''
        if self.ant.esta_vacia():
            raise StopIteration
        nodo=self.ant.desapilar()
        self.actual=nodo
        return nodo.dato

    def iter_insertar(self,elem):
        '''inserta un elemento en la posicion actual del iterador'''
        nodo=_Nodo(elem)
        nodo.prox=self.actual.prox
        self.actual.prox=nodo
        self.__next__()




class _Marca:
	'''Representacion de una marca musical, con atributos de tiempo de duracion
	y notas a sonar en este'''
	def __init__(self,tiempo):
		'''Crea el objeto marca recibiendo el atributo tiempo'''
		self.tiempo = tiempo
		self.audio = []

	def agregar_audio(self,refnota):
		'''Agrega una referencia numerica a la posicion del track de nota a sonar'''
		self.audio.append(refnota)

	def quitar_audio(self,refnota):
		'''Modifica la configuracion de una nota existente'''
		if refnota in self.audio:
			self.audio.remove(refnota)


class _Track:
	'''Representacion de un track de sonido formado por la funcion que lo genera,
	la frecuencia del sonido y el volumen de este'''
	def __init__(self,funcion,frecuencia,volumen):
		'''Crea un track recibiendo los atributos funcion, frecuencia, volumen'''
		self.fun=funcion
		self.frec=frecuencia
		self.vol=volumen


class Cancion:
	'''OBJETO QUE REPRESENTA LOS ELEMENTOS DE UNA CANCION Y UNA FORMA DE RECORRERLOS, SIENDO ESTOS ELEMENTOS
	TRACKS DE SONIDOS Y MARCAS DE TIEMPO'''
	def __init__(self):
		"""INICA EL OBJETO CANCION VACIO"""
		self.tracks =[]
		self.marcas = ListaEnlazada()
		self.pos = None #iterador de la lista enlazada de marcas, se actualiza al agregar 
						#marcas y comienza como None ya que la lista comienza vacia en una
						#nueva cancion

	def agregar_track(self,lctrack,posicion=None):
		"""AGREGA UN TRACK RECIBIDO COMO UNA LISTA DE CADENAS"""
		n_track=_Track(lctrack[0],float(lctrack[1]),float(lctrack[2]))
		if posicion is None:
			self.tracks.append(n_track)
		else:
			self.tracks.insert(posicion,n_track)

	def quitar_track(self,posicion):
		"""QUITA UN TRACK"""
		self.tracks.pop(posicion)

	def agregar_marca(self,tiempo,antosig=None):
		"""AGREGA UNA MARCA EN UNA CANCION"""
		Nuevo  = _Marca(tiempo)
		if antosig=='ant':
			self.mov_atras()
		elif antosig=='sig':
			self.mov_adelante()
		if self.marcas.prim == None:
			self.marcas.append(Nuevo)
			self.pos = iter(self.marcas)
		else:		
			self.pos.iter_insertar(Nuevo)

	def trackonoff(self,n,onoff):
		"""HABILITA O NO UN TRACK"""
		if onoff == "on":
			next(self.pos).agregar_audio(n)
		else:
			next(self.pos).quitar_audio(n)
		self.pos.anterior()

	def mov_adelante(self,cantmov=1):
		"""MUEVA UNA O MAS POSICIONES ADELANTE AL CURSOR"""
		try :
			while cantmov>0:
				next(self.pos)
				cantmov -=1
		except StopIteration:
			return

	def mov_atras(self,cantmov=1):
		"""MUEVE  UNA O MAS POSICIONES ATRAS AL REPRODUCTOR"""
		try:
			while cantmov>0:
				self.pos.anterior()
				cantmov-=1
		except StopIteration:
			return	

		
class Reproductor:
	'''INTERPRETE DEL OBJETO CANCION, CAPAZ DE CREAR SONIDOS A PARTIR DE ESTE'''

	def __init__(self):
		"""INICIA EL OBJETO REPRODUCTOR VACIO"""
		self.cancion = Cancion()
		self.sonidos = []
		self.cursor = None 
		self.nom_cancion = None

	def reiniciar_cursor(self):
		"""REINICIA EL CURSOR DEL REPRODUCTOR"""
		try:
			while True:
				self.cursor.anterior()
		except StopIteration:
			 return

	def cargar_de_archivo(self,archivoplp):
		"""CARGA A MEMORIA Y VALIDA UN ARCHIVO CON FORMATO PPL"""
		cancionarch=Cancion()
		with open(archivoplp,'r') as archivo:
			archivo.readline()#salteo el header del archivo
			for linea in archivo:
				line = linea.rstrip('\n')
				field , data = line.split(",")
				if field == 'C':
					continue
				elif field == 'S':
					if not validar_track(data,'|'):
						raise IOError
					track=data.split('|')
					cancionarch.agregar_track(track)
				elif field =='T':
					if not is_float(data):
						raise IOError
					tiempo = float(data)
				elif field == 'N':
					sonidos=data
					if len(sonidos)>len(cancionarch.tracks):
						raise IOError
					cancionarch.agregar_marca(tiempo)
					for i in range (len(sonidos)):
						if sonidos[i] == '#':
							cancionarch.trackonoff(i,"on")
						elif sonidos[i] not in '#·':
							raise IOError
		self.nom_cancion=archivoplp
		self.cancion=cancionarch
		self.cursor = self.cancion.pos

	def guardar_archivo(self,nombre=None):
		"""GUARDA EN EL DIRECTORIO EL ARCHIVO"""
		if not nombre:
			nombre=self.nom_cancion
		if self.cursor==None:
			raise Exception('Cancion vacia')
		self.reiniciar_cursor()
		with open(nombre,'w') as archivo:
			archivo.write('FIELD,DATA\n')
			archivo.write('C,{}\n'.format(len(self.cancion.tracks)))
			for track in self.cancion.tracks:
				archivo.write('S,{}|{}|{}\n'.format(track.fun,track.frec,track.vol))
			tiempos=Pila()
			tiempos.apilar(0)
			for marca in self.cancion.marcas:
				if marca.tiempo!=tiempos.ver_tope():
					archivo.write('T,{}\n'.format(marca.tiempo))
				tiempos.apilar(marca.tiempo)
				notasplp=[]
				for i in range(len(self.cancion.tracks)):
					if i in marca.audio:
						notasplp.append('#')
					else:
						notasplp.append('·')
				archivo.write('N,{}\n'.format(''.join(notasplp)))



	def crear_cancion(self,nombre=None):
		"""CREA UNA CANCION VACIA"""
		self.cancion=Cancion()
		self.nom_cancion= nombre


	def crear_sonidos(self):
		"""CREA SONIDOS SEGUN MODULO PYSOUND"""
		for track in (self.cancion.tracks):
			if 'SQ' in track.fun:
				func=FUN_SOUND["SQ"]
				A=int(track.fun.strip('SQ'))/100#parametro de sonido 'square' no se que signifique
				i=func(float(track.frec),float(track.vol),A)
			else:
				func=FUN_SOUND[track.fun]
				i=func(float(track.frec),float(track.vol))
			self.sonidos.append(i)

	def _reproducirsonidos(self,player):
		'''Recibe un reproductor con sonidos,y reproduce la marca actual y avanza una marca si es posible'''
		marca=next(self.cursor)
		if not marca:
			raise StopIteration
		sonidos=[]
		for i in marca.audio:
			if i < len(self.sonidos):
				sonidos.append(self.sonidos[i])
			else:
				marca.audio.remove(i)
		player.play_sounds(sonidos,marca.tiempo)

	def reproducir(self,cuanto=(None,None)):
		"""DEVUELVE LA REPRODUCCION DEL ARCHIVO. LA FORMA EN LA QUE SE REPRODUZCA DEPENDE DEL
		PARAMETRO CUANTO INGRESADO"""
		self.crear_sonidos()
		sp = pysounds.SoundPlayer(len(self.sonidos))
		if cuanto[0]==None:
			self.cursor=self.cancion.pos
			self._reproducirsonidos(sp)
			self.cursor.anterior()

		elif cuanto[0]=="all":
			self.reiniciar_cursor()
			try:
				while True:
					self._reproducirsonidos(sp)
			except StopIteration:
				self.reiniciar_cursor()
		elif cuanto[0] == "marcas":
			acum=0
			try:
				self.cursor=self.cancion.pos
				while True:
					self._reproducirsonidos(sp)
					acum += 1
					if acum > cuanto[1]:
						break
			except StopIteration:
				print('Fin de cancion')
			finally:
				while acum > 0:
					acum -= 1
					self.cancion.mov_atras()
		elif cuanto[0] == "tiempo":
			acum=0
			self.reiniciar_cursor()
			try:
				while True:
					self._reproducirsonidos(sp)
					acum += self.cursor.anterior().tiempo
					next(self.cursor)
					if acum >= cuanto[1]:
						break
			except StopIteration:
				print('fin de cancion')
			finally:
				self.reiniciar_cursor()

def validar_track(trackstr,separador):
	'''Verifica que un track ingresado como cadena sea correcto'''
	validar=False
	for funcion in ('SQ','TRIA','SINE','NOISE'):
		if funcion in trackstr:
			if validar==True:#no se debe ingresar mas de una funcion por track
				return False
			validar=True
	if not validar:
		return False
	track = trackstr.split(separador)
	if 'SQ' in track[0]:
		if not track[0][2:].isdigit():
			return False
	if len(track)!= 3:
		return False
	track[0]=track[0]
	if not is_float(track[1]):
		return False
	if not is_float(track[2]):
		return False
	return True 

def is_float(cadena): #creo esta funcion para validar numeros flotantes ingresados
	'''Verifica si una cadena se puede transformar en float'''
	try:
		float(cadena)
		return True
	except ValueError:
		return False

class Shell(cmd.Cmd):
	
	intro = "Bienvenido a Sounds of Cyber City.\n"
	"Ingrese help o ? para listar los comandos.\n"
	prompt = "*>>" 
	def do_LOAD(self,archivo):
		"""CARGA ARCHIVO PLP"""
		try:
			rp.cargar_de_archivo(archivo)
		except Exception as err:
			print('Error al cargar el archivo, verifique el formato y la ubicacion de este')
	def do_STORE(self,archivo):
		"""GUARDA ARCHIVO PLP"""
		try:
			if archivo:
				rp.guardar_archivo(archivo)
			elif rp.nom_cancion == None:
				raise Exception('''Debe ponerle nombre a su cancion para guardarla: STORE <nombre>''')
			else:
				rp.guardar_archivo()
		except Exception as e:
			print(e)
	def do_STEP(self,parametro = None):
		"""AVANZA UNA POSICION DE MARCA SI ES POSIBLE"""
		try:
			if rp.cancion.pos==None:
				raise Exception('Cancion Vacia')
			rp.cancion.mov_adelante()
			rp.cursor=rp.cancion.pos
		except Exception as err:
			print(err)
	def do_BACK(self,parametro = None):
		"""RETROCEDE A LA MARCA DE TIMPO ANTEROIR SI ES POSIBLE"""
		try:
			if rp.cancion.pos == None:
				raise Exception('Cancion vacia')
			rp.cancion.mov_atras()
			rp.cursor=rp.cancion.pos
		except Exception as err:
			print(err)
	def do_STEPM(self,n):
		"""AVANZA N MARCAS HACIA ADELANTE"""
		try:
			if not n.isdigit():
				raise ValueError('Debe ingresar un numero valido')
			if rp.cancion.pos == None:
				raise Exception('Cancion vacia')
			rp.cancion.mov_adelante(int(n))
			rp.cursor=rp.cancion.pos
		except Exception as err:
			print (err)
	def do_BACKM(self,n):
		"""RETROCEDE N MARCAS HACIA ATRAS"""
		try:
			if not n.isdigit():
				raise ValueError('Debe ingresar un numero valido')
			if rp.cancion.pos==None:
				raise Exception('Cancion vacia')
			rp.cancion.mov_atras(int(n))
			rp.cursor=rp.cancion.pos
		except Exception as err:
			print (err)
	def do_TRACKADD(self,trackingresado):
		"""AGREGA UN TRACK DE SONIDO INDICADO, DEBE ESTAR EN FORMATO <FUNCION> <FRECUENCIA> <VOLUMEN>
		SEPARADOS SOLO POR ESPACIOS, LAS FUNCIONES DEBEN SER INGRESADAS EN MAYUSCULAS"""
		try:
			if not validar_track(trackingresado," "):
				raise ValueError('Error al ingresar os datos, verifique que haya ingresado el track correctamente') 
			track=trackingresado.split(' ')
			rp.cancion.agregar_track(track)
		except Exception as error:
			print(error)
	def do_TRACKDEL(self,n):
		"""ELIMINA TRACK POR NUMERO"""
		try:
			if not n.isdigit():
				raise Exception('Debe ingresar un numero valido')
			elif int(n)> len(rp.cancion.tracks) or int(n) < 1:
				raise ValueError('No existe el track indicado')
			respuesta=input('''Advertencia esto eliminara el track en la posicion {} 
y el track en la posicion {} ,si existe, tomara su lugar, y asi con los siguientes.
Si solo desea desactivar el track en una marca use el comando TRACKOFF 
¿Esta seguro que desea seguir? s/n \n'''.format(n,int(n)+1))
			if respuesta.upper() == 'S':
				rp.cancion.quitar_track(int(n)-1)
		except Exception as error:
			print(error)
	def do_MARKADD(self,tiempo):
		"""AGREGA UNA MARCA DE TIEMPO DE LA DURACION ESTABLECIDA. ORIGINALMENTE TODOS LOS TRACKS ARRANCAN COMO 
		DESHABILITADOS"""
		try:
			if not is_float(tiempo):
				raise ValueError('Verifique el valor de tiempo ingresado')
			rp.cancion.agregar_marca(float(tiempo))
			if rp.cursor==None:
				rp.cursor=rp.cancion.pos
		except Exception as error:
			print(error)
	def do_MARKADDNEXT(self,tiempo):
		"""IGUAL QUE MARKADD PERO LA INSERTA LUEGO DE LA MARCA EN LA CUAL ESTA ACTUALMENTE EL CURSOR"""
		try:
			if not is_float(tiempo):
				raise ValueError('Verifique el valor de tiempo ingresado')
			rp.cancion.agregar_marca(float(tiempo),"sig")
			rp.cursor=rp.cancion.pos
		except Exception as error:
			print(error)
	def do_MARKADDPREV(self,tiempo):
		"""IGUAL QUE MARKADD PERO LA INSERTA EN LA ANTERIOR EN LA CUAL ESTA ACTUALMENTE EL CURSOR"""
		try:	
			if not is_float(tiempo):
				raise ValueError('Verifique el valor de tiempo ingresado')
			rp.cancion.agregar_marca(float(tiempo),"ant")
			rp.cursor=rp.cancion.pos
		except Exception as error:
			print (error)
	def do_TRACKON(self,n):
		"""HABILITA EL TRACK DURANTE LA MARCA DE TIEMPO EN LA CUAL ESTA PARADA EL CURSOR"""
		try:
			if not n.isdigit():
				raise ValueError('Debe ingresar un numero de track valido')
			if int(n)<1 or int(n)>len(rp.cancion.tracks):
				raise ValueError('No se encuentra el track, verifique el valor ingresado')
			rp.cancion.trackonoff(int(n)-1,"on")
		except Exception as error:
			print(error)
	def do_TRACKOFF(self,n):
		"""OPERACION INVERSA A TRACKON"""
		try:
			if not n.isdigit():
				raise ValueError('Debe ingresar un numero de track valido')
			if int(n)<1 or int(n)>len(rp.cancion.tracks):
				raise ValueError('No se encuentra el track, verifique el valor ingresado')
			rp.cancion.trackonoff(int(n)-1,"off")
		except Exception as error:
			print(error)
	def do_PLAY(self, parametro = None):
		"""REPRODUCE LA MARCA ACTUAL"""
		try:
			if rp.cursor==None:
				raise Exception('El reproductor esta vacio')
			rp.reproducir()
		except Exception as error:
			print(error)
	def do_PLAYALL(self, parametro = None):
		"""REPRODUCE LA CANCION COMPLETA DESDE EL INICIO"""
		try:
			if rp.cursor==None:
				raise Exception('El reproductor esta vacio')
			rp.reproducir(('all',None))
		except Exception as error:
			print(error)
	def do_PLAYMARKS(self,nmarcas):
		"""REPRODUCE LA CANTIDAD DE MARCAS ESTABLECIDAS"""
		try:
			if not nmarcas.isdigit():
				raise ValueError('Verifique el valor ingresado')
			if rp.cursor==None:
				raise Exception('El reproductor esta vacio')
			rp.reproducir(("marcas",int(nmarcas)))
		except Exception as error:
			print(error)
	def do_PLAYSECONDS(self,nsegundos):
		"""REPRODUCE EL INICIO HASTA LA CANTIDAD DE N TIEMPO ESTABLECIDA EN SEGUNDOS"""
		try:	
			if not is_float(nsegundos):
				raise ValueError('Verifique el valor ingresado para los segundos')
			if rp.cursor==None:
				raise Exception('El reproductor esta vacio')
			rp.reproducir(("tiempo",float(nsegundos)))
		except Exception as error:
			print(error)
	def do_exit(self,arg):
		"""SALIDA DEL PROGRAMA"""
		return True
	def do_NEW(self, nombre = None):
		"""CREA UNA CANCION NUEVA VACIA"""
		resp= input('Esto creara una nueva cancion vacia en el lugar de la actual ¿esta seguro que desea seguir? S/N\n').upper()
		if resp == 'S':
			rp.crear_cancion(nombre)

rp = Reproductor()
Shell().cmdloop()
