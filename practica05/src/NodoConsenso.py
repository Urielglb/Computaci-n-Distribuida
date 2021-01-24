import simpy
from Nodo import *
from Canales.CanalRecorridos import *
# La unidad de tiempo
TICK = 1

class NodoConsenso(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Consenso.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo de consenso. '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        # Atributos extra
        self.V = [None] * (len(vecinos) + 1) # Llenamos la lista de Nones
        self.V[id_nodo] = id_nodo
        self.New =  set([id_nodo])
        self.rec_from = [None] * (len(vecinos) + 1)
        self.fallare = False      # Colocaremos esta en True si el nodo fallará
        self.lider = None         # La elección del lider.
        #Atributos para el detector de fallas
        self.suspected = []
        self.crashed = [False] * (len(vecinos) + 1)

    def consenso(self, env, f):
        '''El algoritmo de consenso.'''
        # Aquí va su implementación
        if self.id_nodo<f: #Si estoy dentro de las fallas cambio mi valor y termino el proceso
            self.fallare = True
            return
        #Detector de fallos
        beta = f+2
        delta = f+1
        extra = 0 #La rondas extra a ejecutar
        while True:
            #Si beta es igual a nuestro limite entonces reiniciamos nuestro conteo
            if beta == f+2:
                beta = 0
                for vecino in self.vecinos:
                    if vecino not in self.suspected:
                        self.canal_salida.envia({"msg":"INQ","id":self.id_nodo},[vecino])
                self.crashed = [True] * (len(self.vecinos)+1)
                self.crashed[self.id_nodo] = False

            #Mientras tenga mensajes que procesar   
            while len(self.canal_entrada.items) != 0:
                mensaje = yield self.canal_entrada.get()
                if mensaje["msg"] == "INQ":
                    id = mensaje["id"]
                    self.canal_salida.envia({"msg":"ECHO","id":self.id_nodo}, [id])
                if mensaje["msg"]=="ECHO":
                    self.crashed[mensaje["id"]] = False
            #Cuando se agota el tiempo agregamos a nuestros sospechosos y terminamos
            if delta == 0:
                for (index,crash) in enumerate(self.crashed):
                    if crash:
                        self.suspected.append(index)
                break
                
            yield env.timeout(1)
            beta +=1
            extra +=1
            delta -=1
        #Consenso
        while (env.now <= (f+extra)): #env.now comienza conteo de ronda desde 0 por lo que solo llegamos hasta el número f + extra de rondas
            yield env.timeout(TICK)
            if self.New != set():
                mensaje = {"msg":self.New,"id":self.id_nodo}
                self.canal_salida.envia(mensaje,self.vecinos)#(self.id_nodo,self.New)
            mensaje = yield self.canal_entrada.get()
            self.rec_from[mensaje["id"]] = mensaje["msg"]
            self.New = set()
            for j in range(len(self.rec_from)):
                if self.rec_from[j] != None:
                    for k in self.rec_from[j]:
                        if self.V[k] == None:
                            self.V[k] = k
                            self.New.add(k)
        for value in self.V:
            if value != None and not self.fallare:
                self.lider = value
                break 
        print(("Soy el proceso {}, tengo como fallos a {} y como lider a {}").format(self.id_nodo,self.suspected,self.lider))

if __name__ == "__main__":
    #Probamos que el detector de fallas funcionó ejecutando el algoritmo de la gráfica del test
    adyacencias = [[1, 2, 3, 4, 5, 6], [0, 2, 3, 4, 5, 6], [0, 1, 3, 4, 5, 6],
                   [0, 1, 2, 4, 5, 6], [0, 1, 2, 3, 5, 6], [0, 1, 2, 3, 4, 6],
                   [0, 1, 2, 3, 4, 5]]
    env = simpy.Environment()
    bc_pipe = CanalRecorridos(env)
    grafica = []
    for i in range(0, len(adyacencias)):
        grafica.append(NodoConsenso(i, adyacencias[i],
                                    bc_pipe.crea_canal_de_entrada(), bc_pipe))
    f = 2 
    for nodo in grafica:
        env.process(nodo.consenso(env, f))
    env.run()
  