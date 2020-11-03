import simpy
import math
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoBFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo BFS. '''
        ''' Aquí va tu implementacion '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        #Atributos para bfs
        self.padre = self.get_id() #Al inicializar el padre de un nodo es el mismo
        self.distancia = math.inf #La distancia de los nodos al inicializar es infinito

    def bfs(self,env):
        """
        Método con el que se recorrerá la gráfica de modo bfs asignando padres a cada nodo
        Parameters
        ----------
        env: simpy.Enviroment
        El ambiente de simpy donde se está llevando a cabo la ejecución de todos los nodos
        """
        if (self.get_id()==0):
            self.distancia = 0
            mensaje = {"distancia":self.distancia,"nodo":self.get_id()}
            self.canal_salida.envia(mensaje,self.vecinos)
        while True:
            yield env.timeout(TICK)
            mensaje = yield self.canal_entrada.get()
            distancia_recivida = mensaje.get("distancia")
            nodo_emisor = mensaje.get("nodo")
            if ((distancia_recivida+1)<self.distancia):
                self.distancia = distancia_recivida+1
                self.padre = nodo_emisor
                mensaje = {"distancia":self.distancia,"nodo":self.get_id()}
                self.canal_salida.envia(mensaje,self.vecinos)

    def get_id(self):
        """
        Metodo que regresa el id del nodo
        Returns
        -------
        int
            EL id del nodo
        """
        return self.id_nodo