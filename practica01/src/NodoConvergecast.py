import simpy
import Canales.CanalGenerico as CanalGenerico
from Nodo import Nodo

class NodoConvergecast(Nodo):
    '''Implementa la interfaz de Nodo para el algoritmo de Arbol Generador.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        '''Inicializa los atributos del nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        # Atributos extra para convergecast
        self.data = None
        self.parent = None
        self.nodoRaiz = False
        self.child = set()
        self.buffer = []

    def convergecast(self, env):
        self.buffer += [(self.id_nodo, self.data)]
        # Valores iniciales para hojas.
        if (len(self.vecinos) == 1): # Si es hoja
            self.canal_salida.envia({'s':self.id_nodo, 'm':'B','buffer': self.buffer}, self.vecinos)

        finished = False
        while (not finished):
            yield env.timeout(1)
            msg = yield self.canal_entrada.get()
            sndr = msg['s']
            call = msg['m']
            buff = msg['buffer']
            if (call == 'B'): # Si llega un back, agrega el nodo a los hijos.
                self.buffer += buff
                self.child.add(sndr)
            if (len(self.child) == len(self.vecinos) - 1 and (not self.nodoRaiz)): # Si ya llegaron todos tus hijos.
                for i in self.vecinos:  # El que no mando nada es tu padre.
                    if (not (i in self.child)):
                        self.parent = i # Seleccionalo como tal.
                # Mandale todo lo que recibiste al padre.
                self.canal_salida.envia_uno({'s':self.id_nodo,'m':'B','buffer': self.buffer}, self.parent)
            elif (len(self.child) == len(self.vecinos)): # Si eres la raiz.
                finished = True

    def get_id(self):
        '''Regresa el id del nodo.'''
        return self.id_nodo;

def main():
    # Ejemplo de uso
    env = simpy.Environment()
    bc_pipe = CanalGenerico.CanalGenerico(env)

    grafica = []
    ady = [[1,2],[0],[0,3],[2]]
    for i in range(len(ady)):
        grafica.append(NodoConvergecast(i,ady[i], bc_pipe.crea_canal_de_entrada(), bc_pipe))

    # Tuve que modificar el algoritmo ya que no sabemos quienes son padres o hijos.
    # Solo sabemos que estamos en un arbol y quienes son hojas.
    # La unica informacion extra que se necesita par hacer que el algoritmo funcione
    # es indicar quien es la raiz, sino el algoritmo asumira que es el nodo mas a la
    # mitad del arbol.

    grafica[0].nodoRaiz = True

    for i in range(len(ady)):
        env.process(grafica[i].convergecast(env))

    env.run()

if __name__ == '__main__':
    main()
