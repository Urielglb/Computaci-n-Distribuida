import simpy
from Canales.Canal import Canal

class CanalGenerico(Canal):
    '''
    Clase que modela un canal, permite enviar mensajes one-to-many.
    '''
    def __init__(self, env, capacidad=simpy.core.Infinity):
        self.env = env
        self.capacidad = capacidad
        self.canales = []
        self.canal_de_salida = None

    def envia(self, mensaje, vecinos):
        '''
        Envia un mensaje a los canales de salida de los vecinos.
        '''
        if not self.canales:
            raise RuntimeError('No hay canales de salida.')
        eventos = list()
        for i in range(len(self.canales)):
            if i in vecinos:
                eventos.append(self.canales[i].put(mensaje))
        return self.env.all_of(eventos)

    def envia_uno(self, mensaje, vecino):
        '''
        Envia un mensaje a el canal de salida de un vecino.
        '''
        if not self.canales:
            raise RuntimeError('No hay canales de salida.')
        eventos = list()
        if vecino in range(len(self.canales)):
            eventos.append(self.canales[vecino].put(mensaje))
        return self.env.all_of(eventos)

    def crea_canal_de_entrada(self):
        '''
        Creamos un objeto Store en el cual recibiremos los mensajes.
        '''
        canal = simpy.Store(self.env, capacity=self.capacidad)
        self.canales.append(canal)
        self.canal_de_salida = canal
        return canal

    def get_canal_de_salida(self):
        '''
        Regresa el objeto Store en el cual recibiremos los mensajes.
        '''
        return self.canal_de_salida
