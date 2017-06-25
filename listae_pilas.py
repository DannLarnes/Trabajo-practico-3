#Pila
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

#listaenlazada
class _Nodo:
	def __init__(self, dato = None, prox = None):
		self.dato = dato
		self.prox = prox
	def __str__(self):
		return str(self.dato)

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

	def esta_vacia(self):
		if self.len==0 or self.prim == None:
			return True
		return False

class _IteradorLE:
    '''Iterador de Lista Enlazada'''
    
    def __init__(self,prim):
        '''Crea un iterador a partir del parametro prim '''
        self.actual=prim
        self.anteriores=Pila()
        
    def __next__(self):
        '''Avanza, si es posible, el iterador'''
        if not self.actual:
            raise StopIteration
        dato=self.actual.dato
        self.anteriores.apilar(self.actual)
        self.actual=self.actual.prox
        return dato

    def anterior(self):
        '''Retrocede,si es posible, el iterador'''
        if self.anteriores.esta_vacia():
            raise StopIteration
        nodo=self.anteriores.desapilar()
        self.actual=nodo
        return nodo.dato

    def iter_insertar(self,elem):
        '''inserta un elemento en la posicion siguiente a la actual del iterador'''
        nodo=_Nodo(elem)
        nodo.prox=self.actual.prox
        self.actual.prox=nodo
        self.__next__()

