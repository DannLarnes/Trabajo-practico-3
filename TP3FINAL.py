import soundPlayer as pysounds
import cmd
import listae_pilas as lep

FUN_SOUND={'SQ':pysounds.SoundFactory.get_square_sound,
'TRIA':pysounds.SoundFactory.get_triangular_sound,
'SINE':pysounds.SoundFactory.get_sine_sound,
'NOISE':pysounds.SoundFactory.get_noise_sound}

FORMATO_ARCHIVO = {'header':'FIELD,DATA',
'canal' : 'C',
'tiempo' : 'T', 
'descripcion_track' : 'S',
'descripcion_marca' : 'N',
'separador_campodato':',',
'separador_tracks':'|',
'formato_notas':'·#',
'nota_apagada':'·',
'nota_prendida' : '#'}

FORMATO_TRACK={'pos_funcion':0,
'pos_frecuencia':1,
'pos_volumen':2}

class _Marca:
	'''Representacion de una marca musical'''
	def __init__(self,tiempo):
		'''Crea el objeto marca recibiendo la duracion de la misma, se inicia sin notas a sonar'''
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
		'''Crea un track recibe funcion, frecuencia y volumen'''
		self.fun=funcion
		self.frec=frecuencia
		self.vol=volumen


class Cancion:
	'''OBJETO QUE REPRESENTA LOS ELEMENTOS DE UNA CANCION Y UNA FORMA DE RECORRERLOS, SIENDO ESTOS ELEMENTOS
	TRACKS DE SONIDOS Y MARCAS DE TIEMPO'''
	def __init__(self):
		"""INICA EL OBJETO CANCION VACIO"""
		self.tracks =[]
		self.marcas = lep.ListaEnlazada()
		self.pos = iter(self.marcas)

	def agregar_track(self,lctrack,posicion=None):
		"""AGREGA UN TRACK RECIBIDO COMO UNA LISTA DE CADENAS EN LA POSICION INDICADA"""
		n_track=_Track(lctrack[FORMATO_TRACK['pos_funcion']],float(lctrack[FORMATO_TRACK['pos_frecuencia']]),float(lctrack[FORMATO_TRACK['pos_volumen']]))
		if posicion is None:
			self.tracks.append(n_track)
		else:
			self.tracks.insert(posicion,n_track)

	def quitar_track(self,posicion):
		"""QUITA UN TRACK"""
		self.tracks.pop(posicion)

	def agregar_marca(self,tiempo):
		"""AGREGA UNA MARCA EN LA POSICION ACTUAL DE LA CANCION"""
		nuevo  = _Marca(tiempo)
		if self.marcas.esta_vacia():
			self.marcas.append(nuevo)
			self.pos = iter(self.marcas)
		else:		
			self.pos.iter_insertar(nuevo)

	def trackon(self,n):
		"""RECIBE LA POSICION DE UN TRACK Y LO HABILITA"""
		next(self.pos).agregar_audio(n)
		self.pos.anterior()
	
	def trackoff(self,n):
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

	def esta_vacia(self):
		'''devuelve el valor de verdad de si la cancion tiene marcas'''
		return self.marcas.esta_vacia()

		
class Reproductor:
	'''INTERPRETE DEL OBJETO CANCION, CAPAZ DE CREAR SONIDOS A PARTIR DE ESTE'''

	def __init__(self):
		"""INICIA EL OBJETO REPRODUCTOR VACIO"""
		self.cancion = Cancion()
		self.sonidos = []
		self.cursor = self.cancion.pos
		self.nom_cancion = None
		self.reproductor = None

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
				if len(line.split(FORMATO_ARCHIVO['separador_campodato']))!= 2:
					raise Exception('InputError')
				field , data = line.split(FORMATO_ARCHIVO['separador_campodato'])
				if field == FORMATO_ARCHIVO['canal']:
					continue
				elif field == FORMATO_ARCHIVO['descripcion_track'] :
					if not validar_track(data, FORMATO_ARCHIVO['separador_tracks']):
						raise Exception('InputError')
					track=data.split(FORMATO_ARCHIVO['separador_tracks'])
					cancionarch.agregar_track(track)
				elif field == FORMATO_ARCHIVO['tiempo']:
					if not is_float(data):
						raise Exception('InputError')
					tiempo = float(data)
				elif field == FORMATO_ARCHIVO['descripcion_marca']:
					sonidos=data
					if len(sonidos)>len(cancionarch.tracks):
						raise Exception('InputError')
					cancionarch.agregar_marca(tiempo)
					for i in range (len(sonidos)):
						if sonidos[i] == FORMATO_ARCHIVO['nota_prendida']:
							cancionarch.trackon(i)
						elif sonidos[i] not in FORMATO_ARCHIVO['formato_notas']:
							raise Exception('InputError')
		self.nom_cancion=archivoplp
		self.cancion=cancionarch
		self.cursor = self.cancion.pos

	def guardar_archivo(self,nombre=None):
		"""GUARDA EN EL DIRECTORIO EL ARCHIVO"""
		if not nombre:
			nombre=self.nom_cancion
		if self.cancion.esta_vacia():
			raise Exception('Cancion vacia')
		self.reiniciar_cursor()
		with open(nombre,'w') as archivo:
			archivo.write(FORMATO_ARCHIVO['header']+'\n')
			archivo.write(FORMATO_ARCHIVO['canal']+FORMATO_ARCHIVO['separador_campodato']+'{}\n'.format(len(self.cancion.tracks)))
			for track in self.cancion.tracks:
				archivo.write(FORMATO_ARCHIVO['descripcion_track']+FORMATO_ARCHIVO['separador_campodato']+'{}{}{}{}{}\n'.format(track.fun,FORMATO_ARCHIVO['separador_tracks'],track.frec,FORMATO_ARCHIVO['separador_tracks'],track.vol))
			tiempos=lep.Pila()
			tiempos.apilar(0)
			for marca in self.cancion.marcas:
				if marca.tiempo!=tiempos.ver_tope():
					archivo.write(FORMATO_ARCHIVO['tiempo']+FORMATO_ARCHIVO['separador_campodato']+'{}\n'.format(marca.tiempo))
				tiempos.apilar(marca.tiempo)
				notasplp=[]
				for i in range(len(self.cancion.tracks)):
					if i in marca.audio:
						notasplp.append(FORMATO_ARCHIVO['nota_prendida'])
					else:
						notasplp.append(FORMATO_ARCHIVO['nota_apagada'])
				archivo.write(FORMATO_ARCHIVO['descripcion_marca']+FORMATO_ARCHIVO['separador_campodato']+'{}\n'.format(''.join(notasplp)))

	def crear_cancion(self,nombre=None):
		"""CREA UNA CANCION VACIA"""
		self.cancion=Cancion()
		self.nom_cancion= nombre
		self.cursor=self.cancion.pos
		self.sonidos=[]
		self.reproductor=None



	def crear_sonidos(self):
		"""CREA SONIDOS SEGUN MODULO PYSOUND"""
		for track in (self.cancion.tracks):
			if 'SQ' in track.fun:
				func=FUN_SOUND["SQ"]
				A=int(track.fun.strip('SQ'))/100#parametro de sonido 'square' no se que signifique
				sound=func(float(track.frec),float(track.vol),A)
			else:
				func=FUN_SOUND[track.fun]
				sound=func(float(track.frec),float(track.vol))
			self.sonidos.append(sound)

	def crear_reproductor(self):
		self.crear_sonidos()
		self.reproductor = pysounds.SoundPlayer(len(self.sonidos))
	
	def _reproducirsonidos(self,tiempo=None):
		'''Recibe un reproductor con sonidos, reproduce la marca actual durante su tiempo o 
		una cantida de tiempo indicada, avanza una marca si es posible'''
		marca=next(self.cursor)
		if not marca:
			raise StopIteration
		sonidos=[]
		for i in marca.audio:
			if i < len(self.sonidos):
				sonidos.append(self.sonidos[i])
			else:
				marca.audio.remove(i)
		if tiempo:
			self.reproductor.play_sounds(sonidos,tiempo)
		else:
			self.reproductor.play_sounds(sonidos,marca.tiempo)

	def reproducir_actual(self):
		"""REPRODUCE LA MARCA ACTUAL"""
		self.crear_reproductor()
		self.cursor=self.cancion.pos
		self._reproducirsonidos()
		self.cursor.anterior()

	def reproducir_todo(self):
		"""REPRODUCE TODA LA CANCION"""
		self.crear_reproductor()	
		self.reiniciar_cursor()
		try:
			while True:
				self._reproducirsonidos()
		except StopIteration:
			self.reiniciar_cursor()
		
	def reproducir_marcas(self,cuantas):
		"""REPRODUCE LA CANTIDAD DE MARCAS INDICADAS"""
		self.crear_reproductor()
		acum=0
		try:
			self.cursor=self.cancion.pos
			while True:
				self._reproducirsonidos()
				acum += 1
				if acum > cuantas:
					break
		except StopIteration:
			print('Fin de cancion')
		finally:
			while acum > 0:
				acum -= 1
				self.cancion.mov_atras()
		
	def reproducir_tiempo(self,tiempo):
		"""REPRODUCE LA CANTIDAD DE TIEMPO INDICIADO DESDE EL INICIO"""
		self.crear_reproductor()
		acum=0
		self.reiniciar_cursor()
		try:
			while True:
				tiempoactual=next(self.cursor).tiempo
				self.cursor.anterior()
				if acum +tiempoactual > tiempo:
					self._reproducirsonidos(tiempo-acum)
					break
				else:
					self._reproducirsonidos()
				acum += self.cursor.anterior().tiempo
				next(self.cursor)
				if acum >= tiempo:
					break
		except StopIteration:
			print('fin de cancion')
		finally:
				self.reiniciar_cursor()

def validar_track(trackstr,separador):
	'''Verifica que un track ingresado como cadena sea correcto'''
	es_valido=False
	for funcion in FUN_SOUND:
		if funcion in trackstr:
			if es_valido:#no se debe ingresar mas de una funcion por track
				return False
			es_valido=True
	if not es_valido:
		return False
	track = trackstr.split(separador)
	if 'SQ' in track[FORMATO_TRACK['pos_funcion']]:
		if not track[FORMATO_TRACK['pos_funcion']][2:].isdigit():
			return False
	if len(track)!= 3:
		return False
	if not is_float(track[FORMATO_TRACK['pos_frecuencia']]):
		return False
	if not is_float(track[FORMATO_TRACK['pos_volumen']]):
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
			print(err)
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
		if rp.cancion.esta_vacia():
			print('Cancion Vacia')
			return
		rp.cancion.mov_adelante()
		rp.cursor=rp.cancion.pos
	def do_BACK(self,parametro = None):
		"""RETROCEDE A LA MARCA DE TIMPO ANTEROIR SI ES POSIBLE"""
		if rp.cancion.esta_vacia():
			print('Cancion vacia')
			return
		rp.cancion.mov_atras()
		rp.cursor=rp.cancion.pos
	def do_STEPM(self,n):
		"""AVANZA N MARCAS HACIA ADELANTE"""
		if not n.isdigit():
			print('Debe ingresar un numero valido')
			return
		if rp.cancion.esta_vacia():
			print('Cancion vacia')
			return
		rp.cancion.mov_adelante(int(n))
		rp.cursor=rp.cancion.pos
	def do_BACKM(self,n):
		"""RETROCEDE N MARCAS HACIA ATRAS"""
		if not n.isdigit():
			print('Debe ingresar un numero valido')
			return
		if rp.cancion.esta_vacia():
			print('Cancion vacia')
			return
		rp.cancion.mov_atras(int(n))
		rp.cursor=rp.cancion.pos

	def do_TRACKADD(self,trackingresado):
		"""AGREGA UN TRACK DE SONIDO INDICADO, DEBE ESTAR EN FORMATO <FUNCION> <FRECUENCIA> <VOLUMEN>
		SEPARADOS SOLO POR ESPACIOS, LAS FUNCIONES DEBEN SER INGRESADAS EN MAYUSCULAS"""
		if not validar_track(trackingresado," "):
			print('Error al ingresar os datos, verifique que haya ingresado el track correctamente')
			return 
		track=trackingresado.split(' ')
		rp.cancion.agregar_track(track)
	def do_TRACKDEL(self,n):
		"""ELIMINA TRACK POR NUMERO"""
		if not n.isdigit():
			print('Debe ingresar un numero valido')
			return
		elif int(n)> len(rp.cancion.tracks) or int(n) < 1:
			print('No existe el track indicado')
			return
		respuesta=input('''Advertencia esto eliminara el track en la posicion {} 
y el track en la posicion {} ,si existe, tomara su lugar, y asi con los siguientes.
Si solo desea desactivar el track en una marca use el comando TRACKOFF 
¿Esta seguro que desea seguir? s/n \n'''.format(n,int(n)+1))
		if respuesta.upper() == 'S':
			rp.cancion.quitar_track(int(n)-1)
	def do_MARKADD(self,tiempo):
		"""AGREGA UNA MARCA DE TIEMPO DE LA DURACION ESTABLECIDA. ORIGINALMENTE TODOS LOS TRACKS ARRANCAN COMO 
		DESHABILITADOS"""
		if not is_float(tiempo):
			print('Verifique el valor de tiempo ingresado')
			return
		rp.cancion.agregar_marca(float(tiempo))
		rp.cursor=rp.cancion.pos
	def do_MARKADDNEXT(self,tiempo):
		"""IGUAL QUE MARKADD PERO LA INSERTA LUEGO DE LA MARCA EN LA CUAL ESTA ACTUALMENTE EL CURSOR"""
		if not is_float(tiempo):
			print('Verifique el valor de tiempo ingresado')
			return
		rp.cancion.mov_adelante()
		rp.cancion.agregar_marca(float(tiempo))
		rp.cursor=rp.cancion.pos
	def do_MARKADDPREV(self,tiempo):
		"""IGUAL QUE MARKADD PERO LA INSERTA EN LA ANTERIOR EN LA CUAL ESTA ACTUALMENTE EL CURSOR"""	
		if not is_float(tiempo):
			print('Verifique el valor de tiempo ingresado')
			return
		rp.cancion.mov_atras()
		rp.cancion.agregar_marca(float(tiempo))
		rp.cursor=rp.cancion.pos

	def do_TRACKON(self,n):
		"""HABILITA EL TRACK DURANTE LA MARCA DE TIEMPO EN LA CUAL ESTA PARADA EL CURSOR"""
		if not n.isdigit():
			print('Debe ingresar un numero de track valido')
			return
		if int(n)<1 or int(n)>len(rp.cancion.tracks):
			print('No se encuentra el track, verifique el valor ingresado')
			return
		rp.cancion.trackon(int(n)-1)

	def do_TRACKOFF(self,n):
		"""OPERACION INVERSA A TRACKON"""
		if not n.isdigit():
			print('Debe ingresar un numero de track valido')
			return
		if int(n)<1 or int(n)>len(rp.cancion.tracks):
			print('No se encuentra el track, verifique el valor ingresado')
			return
		rp.cancion.trackoff(int(n)-1)

	def do_PLAY(self, parametro = None):
		"""REPRODUCE LA MARCA ACTUAL"""
		if rp.cancion.esta_vacia():
			print('El reproductor esta vacio')
			return
		rp.reproducir_actual()
	def do_PLAYALL(self, parametro = None):
		"""REPRODUCE LA CANCION COMPLETA DESDE EL INICIO"""
		if rp.cancion.esta_vacia():
			print('El reproductor esta vacio')
			return
		rp.reproducir_todo()
	def do_PLAYMARKS(self,nmarcas):
		"""REPRODUCE LA CANTIDAD DE MARCAS ESTABLECIDAS"""
		if not nmarcas.isdigit():
			print('Verifique el valor ingresado')
			return
		if rp.cancion.esta_vacia():
			print('El reproductor esta vacio')
			return
		rp.reproducir_marcas(int(nmarcas))
	def do_PLAYSECONDS(self,nsegundos):
		"""REPRODUCE EL INICIO HASTA LA CANTIDAD DE N TIEMPO ESTABLECIDA EN SEGUNDOS"""
		if not is_float(nsegundos):
			print('Verifique el valor ingresado para los segundos')
			return
		if rp.cancion.esta_vacia():
			print('El reproductor esta vacio')
			return
		rp.reproducir_tiempo(float(nsegundos))
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
