import simpy
import random
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoDFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida,numero_procesos):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        #Atributos para dfs
        self.padre = id_nodo #Al inicializar el padre de un nodo es el mismo
        self.hijos = []
        self.reloj = [0] * (numero_procesos) #El reloj vectorial dentro de cada proceso
        self.eventos = [] #Lista donde se llevará cuenta de como sucedieron los eventos

    def dfs(self, env):
        ''' Algoritmo DFS. '''
        if (self.id_nodo == 0): # Luke, yo soy tu padre.
            yield env.timeout(random.randint(0,10))
            self.reloj[self.id_nodo] = self.reloj[self.id_nodo] + 1 #Actualizamos el reloj
            chico = min(self.vecinos)
            msg = {'visited':[self.id_nodo],'nodo':self.id_nodo, 'call':'G','reloj':self.reloj}
            self.canal_salida.envia(msg, [chico])
            self.hijos.append(chico)
            self.agrega_evento('G','E',self.id_nodo,chico)
            

        while True:
            yield env.timeout(random.randint(0,10))
            msg = yield self.canal_entrada.get()
            emisor = msg['nodo']
            visited = msg['visited']
            call = msg['call']
            msg['nodo'] = self.id_nodo
            self.compara_relojes(msg['reloj'])#Actualizamos el reloj
            self.agrega_evento(call,'R',emisor,self.id_nodo)
            # GO
            if (call == 'G'):
                self.padre = emisor
                visited.append(self.id_nodo)
                if (self.__esSubsetLista(self.vecinos, visited)):
                    msg['call'] = 'B'
                    self.reloj[self.id_nodo] = self.reloj[self.id_nodo]+1
                    msg['reloj'] = self.reloj
                    self.canal_salida.envia(msg, [emisor])
                    self.agrega_evento('B','E',self.id_nodo,emisor)
                else:
                    msg['call'] = 'G'
                    chico = min(self.__diferenciaLista(self.vecinos, visited))
                    self.reloj[self.id_nodo] = self.reloj[self.id_nodo]+1
                    msg['reloj'] = self.reloj
                    self.canal_salida.envia(msg, [chico])
                    self.hijos.append(chico)
                    self.agrega_evento('G','E',self.id_nodo,chico)
            # BACK
            elif (call == 'B'):
                if (self.__esSubsetLista(self.vecinos, visited)):
                    if (self.padre == self.id_nodo):
                        pass #Terminamos, pero el algoritmo dice que asi esta bien.
                    else:
                        msg['call'] = 'B'
                        self.reloj[self.id_nodo] = self.reloj[self.id_nodo]+1
                        msg['reloj'] = self.reloj
                        self.canal_salida.envia(msg, [self.padre])
                        self.agrega_evento('B','E',self.id_nodo,self.padre)
                        
                else:
                    msg['call'] = 'G'
                    chico = min(self.__diferenciaLista(self.vecinos, visited))
                    self.reloj[self.id_nodo] = self.reloj[self.id_nodo]+1
                    msg['reloj'] = self.reloj
                    self.canal_salida.envia(msg, [chico])
                    self.hijos.append(chico)
                    self.agrega_evento('G','E',self.id_nodo,chico)

    def compara_relojes(self,reloj_recibido):
        """
        Función auxiliar para comparar el reloj de un proceso con el que recibe y actualizar los valores según 
        sea el caso
        Paramters
        ---------
        reloj_recibido:  list
        El reloj vectorial que recibimos
        """
        for i in range(0,len(self.reloj)):
            if i==self.id_nodo:
                self.reloj[i]  = max (self.reloj[i],reloj_recibido[i])+1
            self.reloj[i]  = max (self.reloj[i],reloj_recibido[i])


    def agrega_evento(self,tipo,mensaje,emisor,receptor):
        """
        Función auxiliar para agregar eventos a nuestra lista de eventos
        Parameters
        ----------
        tipo: dicctionary 
        El mensaje que se mandó
        mensaje: char
        Si el mensaje es envio o recepción
        emisor:int 
        El nodo que mandó el mensaje
        receptor: int
        El nodo que recibe el mensaje
        """
        reloj_actual = self.reloj.copy() #Copiamos el reloj para que no se modifique después
        self.eventos.append([reloj_actual,mensaje,tipo,emisor,receptor])

    # Buena idea manejar a los hijos y vecinos como listas. ;)
    def __esSubsetLista(self, lista1, lista2):
        return set(lista1).issubset(set(lista2))

    def __diferenciaLista(self, lista1, lista2):
        return [x for x in lista1 if x not in lista2]
