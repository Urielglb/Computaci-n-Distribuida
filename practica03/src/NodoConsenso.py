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

    def consenso(self, env, f):
        '''El algoritmo de consenso.'''
        # Aquí va su implementación
        if self.id_nodo<f: #Si estoy dentro de las fallas cambio mi valor y termino el proceso
            self.fallare = True
            return
        while env.now <= f: #env.now comienza conteo de ronda desde 0 por lo que solo llegamos hasta el número f de rondas
            if not self.New: #Si tenemos mensaje que enviar terminamos ejecución
                break
            message = {"msg":self.New,"id":self.id_nodo} #El mensaje que debo mandar y mi identificador
            self.canal_salida.envia(message,self.vecinos)
            yield env.timeout(TICK)
            expected_msgs = len(self.vecinos)-f #Como nuestro procesos fallan desde el inicio solo recibiremos mensajes de los vecinos que no fallaron
            while expected_msgs: 
                recived_msg = yield self.canal_entrada.get()
                self.rec_from[recived_msg.get("id")] = recived_msg.get("msg") #El mensaje id me mando los valores en su mensaje
                expected_msgs = expected_msgs-1
            self.New = set()
            for vecino in self.vecinos:
                if self.rec_from[vecino]:
                    for value in self.rec_from[vecino]:
                        if(self.V[value] == None):
                            self.V[value] = value
                            self.New = self.New.union(set([value]))  
        for value in self.V:
            if value != None and not self.fallare:
                self.lider = value
                break
            
       