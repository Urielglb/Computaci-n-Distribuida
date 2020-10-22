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
        self.parent = None
        self.child = set()
        self.data = None
        self.buffer = []
        self.rcvd_msg = 0

    def convergecast(self, env):
        self.buffer += [(self.id_nodo, self.data)]
        # Valores iniciales para hojas.
        if (len(self.child) == 0):
            self.canal_salida.envia_uno({'m':'B','buffer': self.buffer}, self.parent)

        finished = False
        while (not finished):
            yield env.timeout(1)
            msg = yield self.canal_entrada.get()
            call = msg['m']
            buff = msg['buffer']
            if (call == 'B'):
                self.buffer += buff
                self.rcvd_msg += 1
            if (self.rcvd_msg == len(self.child)):
                if (self.parent != self.id_nodo):
                    self.canal_salida.envia_uno({'m':'B','buffer': self.buffer}, self.parent)
                else:
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

    # Esto es asi porque el algoritmo supone un arbol, pero para eso tendriamos que conectar
    # cada nodo para que tuviera informacion de quien es su padre y quienes son sus hijos,
    # eso es basicamente hacer el algoritmo 7, y eso sale de las reglas de lo requerido.
    # Por la anterior razon, la data del arbol esta hardcodeada.
    # Pero el algoritmo funciona como debe.
    grafica[0].parent = 0
    grafica[1].parent = 0
    grafica[2].parent = 0
    grafica[3].parent = 2
    grafica[0].data = "Soy 0"
    grafica[1].data = "Soy 1"
    grafica[2].data = "Soy 2"
    grafica[3].data = "Soy 3"
    grafica[2].child = {3}
    grafica[0].child = {1,2}

    for i in range(len(ady)):
        env.process(grafica[i].convergecast(env))

    env.run()

if __name__ == '__main__':
    main()
