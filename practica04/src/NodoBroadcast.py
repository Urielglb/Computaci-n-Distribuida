import simpy
import Canales.CanalGenerico as CanalGenerico
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

    def broadcast(self,env):
        """
        Método con el nodo espacial mandará un mensaje a sus hijos y los demás nodos aguardarán a recibir un mensaje y reenviarlo 
        a sus hijos
        Parameters
        ----------
        env: simpy.Enviroment
        El ambiente de simpy donde se está llevando a cabo la ejecución de todos los nodos
        """
        if(self.get_id()==0):
            data = {"message":"Un proceso para gobernarlos a todos \n Un proceso para encontrarlos, \n un anillo para atraerlos a todos y atraerlos en las tinieblas",
                    "id":self.get_id()}
            self.mensaje = data.get("message")
            self.canal_salida.envia(data,self.hijos)
        while True:
            yield env.timeout(1)
            data =  yield self.canal_entrada.get()
            self.mensaje = data.get("message")
            for hijo in self.hijos:
                if hijo == data.get("id"):#Este caso es el que la adyacencia es el padre
                    continue
                self.canal_salida.envia_uno({"message":data.get("message"),"id":self.get_id()},hijo)


    def get_id(self):
        """
        Metodo que regresa el id del nodo
        Returns
        -------
        int
            EL id del nodo
        """
        return self.id_nodo

if __name__ == "__main__":
    env = simpy.Environment()
    bc_pipe = CanalGenerico.CanalGenerico(env)
    grafica = []
    ady = [[1,2],[0,3,4],[0,5,6],[1],[1],[2],[2]]
    for i in range (len(ady)):
        grafica.append(NodoBroadcast(i,ady[i],bc_pipe.crea_canal_de_entrada(),bc_pipe))
    for i in range (len(ady)):
        env.process(grafica[i].broadcast(env))
    env.run()
    for nodo in grafica:
        print(("Nodo {} con mensaje {}").format(nodo.get_id(),nodo.mensaje))