import simpy
import random
from Canales.CanalRecorridos import *
from Nodo import Nodo



class NodoBroadcast(Nodo):
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
    Methods
    -------
    broadcast
    El método principal que implementa cada nodo de la gráfica
    """
    def __init__(self,id_nodo,vecinos,canal_entrada,canal_salida):
        """
        Inicializa los atributos del nodo
        """
        self.id_nodo = id_nodo
        self.hijos = vecinos #Esto gracias a que las graficas que nos pasan suponemos son árboles
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        #Atributos para el algoritmo
        self.mensaje = ""
        #Atributos para el reloj.
        self.reloj = 0
        self.eventos = [] #Lista donde se llevará cuenta de como sucedieron los eventos

    def broadcast(self,env):
        """
        Método con el nodo espacial mandará un mensaje a sus hijos y los demás nodos aguardarán a recibir un mensaje y reenviarlo
        a sus hijos
        Parameters
        ----------
        env: simpy.Enviroment
        El ambiente de simpy donde se está llevando a cabo la ejecución de todos los nodos
        """
        if(self.id_nodo == 0):
            yield env.timeout(random.randint(0,10))
            for hijo in self.hijos:
                self.reloj += 1
                data = {"message": "mensaje", "id": self.id_nodo, "reloj": self.reloj}
                self.mensaje = data.get("message")
                self.canal_salida.envia(data, [hijo])
                self.agrega_evento(data['message'], "E", self.id_nodo, hijo)

        while True:
            yield env.timeout(random.randint(0,10))
            data = yield self.canal_entrada.get()
            self.mensaje = data.get("message")
            emisor = data['id']
            relojTemp = data['reloj']
            self.reloj = max(relojTemp, self.reloj) + 1
            self.agrega_evento(data['message'], "R", emisor, self.id_nodo)
            for hijo in self.hijos:
                if hijo != emisor: # Este caso es el que la adyacencia es el padre
                    self.reloj += 1
                    dataC = {"message": "mensaje", "id": self.id_nodo, "reloj": self.reloj}
                    self.canal_salida.envia(dataC, [hijo])
                    self.agrega_evento(dataC['message'], "E", self.id_nodo, hijo)


    def get_id(self):
        """
        Metodo que regresa el id del nodo
        Returns
        -------
        int
            EL id del nodo
        """
        return self.id_nodo

    def agrega_evento(self,tipo,mensaje,emisor,receptor):
        self.eventos.append([self.reloj, mensaje, tipo, emisor, receptor])
