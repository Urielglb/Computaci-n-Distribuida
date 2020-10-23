import simpy
import Canales.CanalGenerico as CanalGenerico
from Nodo import Nodo

class NodoArbolGenerador(Nodo):
    '''Implementa la interfaz de Nodo para el algoritmo de Arbol Generador.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        '''Inicializa los atributos del nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        # Atributos extra para arbol
        self.exptd_msg = 0
        self.parent = None
        self.child = set()

    def genera_arbol(self, env):
        # Valores iniciales.
        if (self.id_nodo == 0):
            self.parent = self.id_nodo
            self.exptd_msg = len(self.vecinos)
            self.canal_salida.envia({'s':self.id_nodo, 'm':'G'}, self.vecinos)
        else:
            pass

        finished = False
        while (not finished):
            yield env.timeout(1)
            msg = yield self.canal_entrada.get()
            sender = msg['s']
            call = msg['m']
            # GO
            if (call == 'G'):
                if (self.parent == None):
                    self.parent = sender
                    self.exptd_msg = len(self.vecinos) - 1
                    if (self.exptd_msg == 0):
                        self.canal_salida.envia_uno({'s':self.id_nodo, 'm':'B', 'vs': self.id_nodo}, self.parent)
                    else:
                        for i in self.vecinos:
                            if (i != sender)  :
                                self.canal_salida.envia_uno({'s':self.id_nodo, 'm':'G'}, i)
                else:
                    self.canal_salida.envia_uno({'s':self.id_nodo, 'm':'B','vs': -1}, sender)
            # BACK
            elif (call == 'B'):
                val_set = msg['vs']
                self.exptd_msg -= 1
                if (val_set != -1):
                    self.child.add(sender)
                if (self.exptd_msg == 0):
                    if (self.parent != self.id_nodo):
                        self.canal_salida.envia_uno({'s':self.id_nodo, 'm':'B', 'vs': self.id_nodo}, self.parent)
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
    ady = [[1,2,3],[0,2,3],[0,1,3],[1,2,3,4],[3]]
    for i in range(len(ady)):
        grafica.append(NodoArbolGenerador(i,ady[i], bc_pipe.crea_canal_de_entrada(), bc_pipe))

    for i in range(len(ady)):
        env.process(grafica[i].genera_arbol(env))

    env.run()

    # Vemos que el arbol construido es el correcto.
    for nodo in grafica:
        print("Nodo %d con hijos %s" % (nodo.get_id(), nodo.child))

if __name__ == '__main__':
    main()
