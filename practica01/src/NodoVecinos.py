import simpy
import Canales.CanalGenerico as CanalGenerico
from Nodo import Nodo

class NodoVecinos(Nodo):
    """
    Implementa la interfaz Nodo para el algortimo de mandar los vecinos 
    Atributes
    ---------
    id_nodo:int
    El identificador del nodo
    vecinos:list
    Una lista con los vecinos del nodo
    canal_entrada:simpy.Store
    El objeto Store de la biblioteca simpy para recibir mensajes de los distintos nodos
    canal_salida:simpy.Store
    El objeto Store de la biblioteca simpy para recibir mensajes de los distintos nodos
    identifiers: set
    La estructura set que nos servirá para guardar los conjuntos de vecinos  de toda nuestra gráfica
    Methods
    -------
    manda_vecino
    El método principal que implementa cada nodo de la gráfica
    -------
    """
    def __init__(self,id_nodo,vecinos,canal_entrada,canal_salida):
        """
        Inicializa los atributos del nodo
        """
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        #Atributos para el algoritmo
        self.identifiers = set() 
    
    def manda_vecinos(self,env):
        """
        Método con el cual los nodos mandrán a cada uno de sus vecinos su lista propia de vecino y a su vez guardará 
        los nodos de los vecinos que reciba en identifiers
        Parameters
        ----------
        env: simpy.Enviroment
        El ambiente de simpy donde se está llevando a cabo la ejecución de todos los nodos
        """
        conjunto_vecinos = set(self.vecinos)
        self.canal_salida.envia(conjunto_vecinos,self.vecinos)
        while True:
            yield env.timeout(1)
            mensaje = yield self.canal_entrada.get()
            self.identifiers = self.identifiers.union(mensaje)


    def get_id(self):
        """
        Metodo que regresa el id del nodo
        Returns
        -------
        int
            EL id del nodo
        """
        return self.id_nodo
