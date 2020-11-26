import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoDFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        #Atributos para dfs
        self.padre = id_nodo #Al inicializar el padre de un nodo es el mismo
        self.hijos = []

    def dfs(self, env):
        ''' Algoritmo DFS. '''
        if (self.id_nodo == 0): # Luke, yo soy tu padre.
            chico = min(self.vecinos)
            msg = {'visited':[self.id_nodo],'nodo':self.id_nodo, 'call':'G'}
            self.canal_salida.envia(msg, [chico])
            self.hijos.append(chico)

        while True:
            yield env.timeout(TICK)
            msg = yield self.canal_entrada.get()
            emisor = msg['nodo']
            visited = msg['visited']
            call = msg['call']
            msg['nodo'] = self.id_nodo
            # GO
            if (call == 'G'):
                self.padre = emisor
                visited.append(self.id_nodo)
                if (self.__esSubsetLista(self.vecinos, visited)):
                    msg['call'] = 'B'
                    self.canal_salida.envia(msg, [emisor])
                else:
                    msg['call'] = 'G'
                    chico = min(self.__diferenciaLista(self.vecinos, visited))
                    self.canal_salida.envia(msg, [chico])
                    self.hijos.append(chico)
            # BACK
            elif (call == 'B'):
                if (self.__esSubsetLista(self.vecinos, visited)):
                    if (self.padre == self.id_nodo):
                        pass #Terminamos, pero el algoritmo dice que asi esta bien.
                    else:
                        msg['call'] = 'B'
                        self.canal_salida.envia(msg, [self.padre])
                else:
                    msg['call'] = 'G'
                    chico = min(self.__diferenciaLista(self.vecinos, visited))
                    self.canal_salida.envia(msg, [chico])
                    self.hijos.append(chico)

    # Buena idea manejar a los hijos y vecinos como listas. ;)
    def __esSubsetLista(self, lista1, lista2):
        return set(lista1).issubset(set(lista2))

    def __diferenciaLista(self, lista1, lista2):
        return [x for x in lista1 if x not in lista2]
