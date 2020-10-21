import simpy
import Canales.CanalGenerico as CanalGenerico
from Nodo import Nodo

class NodoFlooding(Nodo):
    '''Implementa la interfaz de Nodo para el algoritmo de flooding.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        # Atributo extra para flooding
        self.seen_msg = False

    def broadcast(self, envi):
        '''Función de broadcast para nodos. Resuelto por el algoritmo de flooding.'''
        if self.id_nodo == 0: # Solo el nodo raiz (representado con id = 0) envia el primer msj
            # Esperamos la siguiente transmisión
            yield envi.timeout(1)
            self.seen_msg = True
            self.canal_salida.envia(self.id_nodo, self.vecinos)
        else:
            while True:
                if self.seen_msg is not True:
                    mensaje = yield self.canal_entrada.get()
                    # Esperamos a que nos llegue el mensaje
                    self.seen_msg = True
                    print('%d recibío mensaje de %d en el %d' %(self.id_nodo, mensaje, envi.now))
                    # Lo reenvíamos a los vecinos
                    yield envi.timeout(1)
                    self.canal_salida.envia(self.id_nodo, self.vecinos)
                    break

if __name__ == "__main__":
    # Inicializamos ambiente y canal
    envi = simpy.Environment()
    bc_pipe = CanalGenerico.CanalGenerico(envi)

    # Creamos los nodos
    grafica = []
    adyacencias = [[1, 2], [0, 2, 7], [0, 1, 3, 7], [2, 4, 6], [2, 3, 5], [4], [3, 7], [1, 2, 6]]
    for i in range(0, len(adyacencias)):
        grafica.append(NodoFlooding(i, adyacencias[i], bc_pipe.crea_canal_de_entrada(), bc_pipe))

    # Y le decimos al ambiente que lo procese
    for i in range(0, len(adyacencias)):
        envi.process(grafica[i].broadcast(envi))
