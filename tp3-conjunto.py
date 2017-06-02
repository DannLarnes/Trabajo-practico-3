import soundPlayer as pysounds

FUN_SOUND={'SQ':pysounds.SoundFactory.get_square_sound,
'TRIA':pysounds.SoundFactory.get_triangular_sound,
'SINE':pysounds.SoundFactory.get_sine_sound,
'NOISE':pysounds.SoundFactory.get_noise_sound}

###################

class _Nodo:
	def __init__(self,dato=None,prox=None):
		self.dato = dato
		self.prox = prox
	def __str__(self):
		return str(self.dato)

#pila
class Pila:
    '''...'''
    def __init__(self):
        '''...'''
        self.contenido=[]
        
    def apilar(self,elem):
        '''...'''
        self.contenido.append(elem)
        
    def esta_vacia(self):
        '''..'''
        return len(self.contenido)==0
        
    def desapilar(self):
        '''...'''
        if self.esta_vacia():
            raise Exception('la pila esta vacia')
        return self.contenido.pop()
        
    def ver_tope(self):
        '''...'''
        if self.esta_vacia():
            raise Exception('la pila esta vacia')
        return self.contenido[-1]

#Lista Enlazada

class ListaEnlazada:
	def __init__(self):
		self.prim = None
		self.len = 0

	def __str__(self):
		lista = []
		for i in self:
			lista.append(i)
		return str((lista))
	
	def pop(self, i=None ):
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
		nuevo = _Nodo(x)

		if self.len == 0:
			self.prim = nuevo
		
		else:
			n_ant = self.prim
			while n_ant.prox != None:
				n_ant = n_ant.prox
			n_ant.prox = nuevo

		self.len +=1

	def ir_ultimo(self):
		n_act = self.prim
		while n_act.prox != None:
			n_act = n_act.prox
		return n_act

	def ir_posicion(self,i):
		n_act = self.prim
		for pos in range(1,i):
			n_act = n_act.prox
		return n_act



	def index(self,x):
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
    
    def __init__(self,prim):
        self.actual=prim
        self.ant=Pila()
        
    def __next__(self):
        if not self.actual:
            raise StopIteration
        dato=self.actual.dato
        self.ant.apilar(self.actual)
        self.actual=self.actual.prox
        return dato

    def anterior(self):
    	if not self.ant:
    		raise StopIteration
    	nodo=self.ant.desapilar()
    	self.actual=nodo
    	return nodo.dato

    def iter_insertar(self,elem):
    	nodo=_Nodo(elem)
    	nodo.prox=self.actual.prox
    	self.actual.prox=nodo
    	self.__next__()




class _Marca:
	def __init__(self,tiempo):
		self.tiempo = tiempo
		self.audio = []

	def agregar_audio(self,x,pos=None):
		"""interaccion usuario"""
		if pos:
			self.audio.insert(pos,x)
		else:
			self.audio.append(x)

	def modificar_audio(self,posicion,x):
		self.audio[posicion] = x

	def __str__(self):
		return str("audio {}, tiempo {}".format(self.audio,self.tiempo))

class _Track:

	def __init__(self,funcion,frecuencia,volumen):
		self.fun=funcion
		self.frec=frecuencia
		self.vol=volumen

	def __str__(self):
		return str("funcion {}, frecuencia {}, volumen {}".format(self.fun,self.frec,self.vol))

class Cancion:
	def __init__(self):
		self.tracks =[]
		self.marcas = ListaEnlazada()
		self.pos = None

	def __str__(self):
		return ("tracks {}, marca {}, posicion {}".format(self.tracks,self.marcas,self.pos))

	def agregar_track(self,track,posicion=None):
		n_track=_Track(track[0],int(track[1]),float(track[2]))
		if posicion is None:
			self.tracks.append(n_track)
		else:
			self.tracks.insert(posicion,n_track)
		for marca in self.marcas:
				marca.agregar_audio('.',posicion)

	def quitar_track(self,posicion):
		self.tracks.pop(posicion)

	def agregar_marca(self,tiempo,antosig=None):
		Nuevo  = _Marca(tiempo)
		for i in range(len(self.tracks)):
			Nuevo.agregar_audio('.')
		if antosig=='ant':
			mov_atras()
		elif antosig=='sig':
			mov_adelante()
		if self.marcas.prim == None:
			self.marcas.append(Nuevo)
			self.pos = self.marcas.__iter__()
		else:		
			self.pos.iter_insertar(Nuevo)

	def trackonoff(self,n,onoff):
		if onoff == "on":
			self.pos.__next__().modificar_audio(n,'#')
		else:
			self.pos.__next__().modificar_audio(n,'.')
		self.pos.anterior()

	def mov_adelante(self,parametro=1):
		try :
			while parametro:
				self.pos.__next__()
				parametro -=1
		except StopIteration:
			return

	def mov_atras(self,parametro=1):
		try:
			while parametro:
				self.pos.anterior()
		except StopIteration:
			return	

		
class Reproductor:

	def __init__(self):
		self.cancion=None
		self.sonidos=[]
		self.cursor=None
		self.nom_cancion=None

	def __str__(self):
		return str("cancion {}, sonidos {}, cursor {}, nombre_cacion {}".format(self.cancion,self.sonidos,self.cursor,self.nom_cancion))

	def reiniciar_cursor(self):
		try:
			while True:
				self.cursor.anterior()
		except Exception:
			 return

	def cargar_de_archivo(self,archivoplp):
		cancionarch=Cancion()
		with open(archivoplp,'r') as archivo:
			archivo.readline()#salteo el header del archivo
			for linea in archivo:
				line = linea.rstrip('\n')
				field , data = line.split(",")
				if field == 'C':
					continue
				elif field == 'S':
					track=data.split('|')
					cancionarch.agregar_track(track)
				elif field =='T':
					tiempo = float(data)
				elif field == 'N':
					sonidos=data
					cancionarch.agregar_marca(tiempo)
					for i in range (len(sonidos)):
						if sonidos[i] == '#':
							cancionarch.trackonoff(i,"on")
		self.nom_cancion=archivoplp
		self.cancion=cancionarch
		self.cursor = self.cancion.pos

	def guardar_archivo(self,nombre=None):
		if not nombre:
			nombre=nom_cancion
		self.reiniciar_cursor()
		with open(nombre,'w') as archivo:
			archivo.write('Field,Data')
			archivo.write('C,{}'.format(self.canales))
			for track in self.cancion.tracks:
				archivo.write('S,{}|{}|{}'.format(track.fun,track.frec,track.vol))
			tiempos=Pila()
			for marca in self.cancion.marcas:
				if marca.tiempo!=tiempos.ver_tope():
					archivo.write('T,{}'.format(marca.tiempo))
				tiempos.apilar(marca.tiempo)
				archivo.write('N,{}'.format(''.join(marca.audio)))


	def crear_cancion(self):
		self.cancion=Cancion()


	def crear_sonidos(self):
		for i,track in enumerate(self.cancion.tracks):
			if 'SQ' in track.fun:
				func=FUN_SOUND["SQ"]
				A=int(track.fun.strip('SQ'))/100#parametro de sonido 'square' no se que signifique
				i=func(float(track.frec),float(track.vol),A)
			else:
				func=FUN_SOUND[track.fun]
				i=func(float(track.frec),float(track.vol))
			self.sonidos.append(i)

	def reproducir(self,cuanto=None):
		self.crear_sonidos()
		sp = pysounds.SoundPlayer(len(self.sonidos))
		if not cuanto:
			marca=self.cursor.__next__()
			sonidos=[]
			for i in len(marca.audio):
				if marca.audio[i]=='#':
					sonidos.append(self.sonidos[i])
			sp.play_sounds(sonidos,marca.tiempo)
			self.cursor.anterior()

		elif cuanto=="all":
			self.reiniciar_cursor()
			try:
				while self.cursor:
					marca=self.cursor.__next__()
					sonidos=[]
					for i in range (len(marca.audio)):
						if marca.audio[i]=='#':
							sonidos.append(self.sonidos[i])
					sp.play_sounds(sonidos, marca.tiempo)
			except StopIteration:
				self.reiniciar_cursor()

		elif cuanto[0] == "marcas":
			acum=0
			try:
				while self.cursor:
					marca=self.cursor.__next__()
					sonidos=[]
					for i in len(marca.audio):
						if marca.audio[i]=='#':
							sonidos.append(self.sonidos[i])
					sp.play_sounds(sonidos, marca.tiempo)
					acum += 1
					if acum >= cuanto[1]:
						break
			except StopIteration:
				while acum > 0:
					acum -= 1
					self.anterior()

		elif cuanto[0] == "tiempo":
			acum=0
			try:
				while self.cursor:
					marca = self.cursor.__next__()
					sonidos = []
					for i in len(marca.audio):
						if marca.audio[i] == '#':
							sonidos.append(self.sonidos[i])
					sp.play_sounds(sonidos, marca.tiempo)
					acum += marca.tiempo
					if acum >= cuanto[1]:
						break
			except StopIteration:
				self.reiniciar_cursor()
