#lista enlazada
class _Nodo:
    '''...'''
    def __init__:(self,dato,sig=None):
        '''...'''
        self.dato=dato
        self.prox=sig
		
class ListaEnlasada:
    '''...'''
    def __init__(self):
        '''...'''
        self.prim=None
        self.len=0 #!!!!!!!
        
    def __len__(self):
        '''...'''
        return self.len
    
    def insert(self,dato,pos):
        '''...'''
        if not 0<= pos <len(self):
            raise IndexError('Fuera de rango')
        nodo=_Nodo(x)
        self.len +=1
        ant=None
        act=self.prim
        cont=0
        while act and cont!=pos:
            ant=act
            act=self.prox
            cont+=1
        if len(self)==0:
            self.prim==nodo
        elif pos==0:
            nodo.prox=self.prim
            self.prim=nodo
        else:
            nodo.prox=act
            ant.prox=nodo
    
    def extender(self,B):
        if not B.prim:
            return
        primer=_Nodo(B.prim.dato)
        act=B.prim
        ant=primer
        while act.prox:
            act=act.prox
            nodo=_Nodo(act.dato)
            ant.prox=nodo
            ant=nodo#ant.prox
        acta=self.prim
        if not acta:
            self.prim=primer
            self.len+= B.len
            return
        while acta.prox:
            acta=acta.prox
        acta.prox=primer
        self.len += B.len 
       
    def pop(self,i=None):
        if i is None:
            i = self.len - 1
        if i < 0 or i >= self.len:
            raise IndexError("Índice fuera de rango")
        if i == 0:
            # Caso particular: saltear la cabecera de la lista
            dato = self.prim.dato
            self.prim = self.prim.prox
        else:
            # Buscar los nodos en las posiciones (i-1) e (i)
            n_ant = self.prim
            n_act = n_ant.prox
            for pos in range(1, i):
                n_ant = n_act
                n_act = n_ant.prox
            # Guardar el dato y descartar el nodo
            dato = n_act.dato
            n_ant.prox = n_act.prox
        self.len -= 1
        return dato 

#Iterador---------------------------------------------------------------        
    def __iter__(self):
        return _IteradorLE(self.primer)
        
    def invertir(self):
		'''...'''
		if len(self)<=1:
			return
		ant=None
		act=self.prim
		sig=act.prox
		while act:
			act.ṕrox=ant
			ant=act
			act=sig
			if sig:
				sig=sig.prox
		self.prim=ant
			
			
        
class _IteradorLE:
    
    def __init__(self,primer):
        self.actual=primer
        
    def __next__(self):
        if not self.actual:
            raise StopIteration
        dato=self.actual.dato
        self.actual=self.actual.prox
        return dato

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
#Cola
def Cola:
	'''...'''
	def __init__(self):
		self.prim=None
		self.ult=None
		
	def esta_vacia(self):
		return (not self.prim and not self.ultimo)
		
	def ver_primero(self):
		if self.esta.vacia():
			raise Exception('cola vacia')
		return self.primero.dato
		
	def encolar(self.elem):
		nodo=_Nodo(elem)
		if self.estavacia():
			self.prim=nodo
			self.ult=nodo
		else:
			self.ultimo.prox=nodo
			self.ultimo=nodo	
