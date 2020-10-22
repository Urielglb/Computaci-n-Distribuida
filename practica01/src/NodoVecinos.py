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
        conjunto_vecinos = set(self.vecinos)
        self.canal_salida.envia(conjunto_vecinos,self.vecinos)
        while True:
            yield env.timeout(1)
            mensaje = yield self.canal_entrada.get()
            self.identifiers = self.identifiers.union(mensaje)


    def get_id(self):
        """" 
        Regresa el id del nodo
        """
        return self.id_nodo

if __name__ == "__main__":
    env = simpy.Environment()
    bc_pipe = CanalGenerico.CanalGenerico(env)
    grafica = []
    ady = [[1,3],[0,4],[3],[0,2],[1,5],[4]]
    for i in range (len(ady)):
        grafica.append(NodoVecinos(i,ady[i],bc_pipe.crea_canal_de_entrada(),bc_pipe))
    for i in range (len(ady)):
        env.process(grafica[i].manda_vecinos(env))
    env.run()
    for nodo in grafica:
        print(("Nodo {} con identifiers {}").format(nodo.get_id(),nodo.identifiers))
