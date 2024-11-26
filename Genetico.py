import numpy as np
from Cerebro import Cerebro
from Analitico import Analitico
import tensorflow as tf
import os

class Genetico:
    def __init__(self, num_poblacion, num_generaciones, usuarios, hist = False):
        self.num_poblacion = num_poblacion
        self.poblacion = []
        self.usuarios = usuarios
        self.generaciones = num_generaciones
        self.mejor = None
        self.elitismo = round(0.2*self.num_poblacion)
        self.cont = 0
    
    def crea_poblacion(self):
        for _ in range(self.num_poblacion):
            self.poblacion.append(Cerebro())
    
    def selecciona_mejores(self, usuarios):
        self.usuarios = usuarios
        if self.mejor != None:
            compara = [self.mejor[0], self.usuarios[0]]
            compara = sorted(compara, key=lambda x: [x[6], x[7], x[8]], reverse=True)
            if compara[0] != self.mejor:
                self.mejor = [self.usuarios[0],
                            Cerebro(clonado=self.poblacion[self.usuarios[0][9]].modelo)]
                self.cont += 1
                Analitico().grafica(self.mejor[1].modelo, self.cont)
        else:
            self.mejor = [self.usuarios[0],
                        Cerebro(clonado=self.poblacion[self.usuarios[0][9]].modelo)]
        
        self.seleccion_por_ranking(self.proba_norm())

    def seleccion_por_ranking(self, proba):
        new_poblacion = []
        for i in range(self.elitismo):
            new_poblacion.append(Cerebro(clonado=self.poblacion[proba[i][0]].modelo))
        for _ in range(0, self.num_poblacion-self.elitismo, 2):
            indices = []
            for _ in range(2):
                limite = np.random.rand()
                temp = 0
                select = False
                for i in range(len(proba)-1):
                    temp += proba[i][1]
                    if temp > limite:
                        indices.append(proba[i][0])
                        proba.pop(i)
                        select = True
                        break
                if not select:
                    indices.append(proba[len(proba)-1][0])
                    proba.pop(len(proba)-1)

            self.mezcla(self.poblacion[indices[0]],self.poblacion[indices[1]])
            self.poblacion[indices[0]].nuevo_interprete()
            self.poblacion[indices[1]].nuevo_interprete()
            new_poblacion.append(self.poblacion[indices[0]])
            new_poblacion.append(self.poblacion[indices[1]])

        self.poblacion = new_poblacion

    def proba_norm(self):
        proba = [round(1/(x+2), 2) for x in range(self.num_poblacion)]
        proba = [[self.usuarios[x][9], 
                (proba[x]-min(proba))/(max(proba)-min(proba))] for x in range(self.num_poblacion)]
        return proba

    def mezcla(self, padre1, padre2):
        for i in range(len(padre1.modelo.layers)):
            pesos_p1 = padre1.modelo.layers[i].get_weights()[0]
            pesos_p2 = padre2.modelo.layers[i].get_weights()[0]
            mitad1 = np.shape(pesos_p1)[0]
            mitad2 = np.shape(pesos_p1)[1]
            salida = np.shape(padre1.modelo.layers[i].get_weights()[1])[0]
            indice1 = round(mitad1/2)
            indice2 = indice1
            mitad1_nuevo_peso1 = pesos_p1[:indice1, :]
            mitad2_nuevo_peso1 = pesos_p1[indice1:, :]
            mitad1_nuevo_peso2 = pesos_p2[:indice2, :]
            mitad2_nuevo_peso2 = pesos_p2[indice2:, :]
            if np.random.rand() < 0.1:
                fusionada1 = np.concatenate((mitad1_nuevo_peso1, mitad1_nuevo_peso2))
                fusionada2 = np.concatenate((mitad2_nuevo_peso1, mitad2_nuevo_peso2))
            else:
                fusionada1 = np.concatenate((mitad1_nuevo_peso1, mitad2_nuevo_peso2))
                fusionada2 = np.concatenate((mitad2_nuevo_peso1, mitad1_nuevo_peso2))
            fusionada1, fusionada2 = self.mutacion(fusionada1, fusionada2)
            peso_hijo1 = [
                fusionada1.reshape(mitad1, mitad2),
                np.zeros((salida,))
            ]
            peso_hijo2 = [
                fusionada2.reshape(mitad1, mitad2),
                np.zeros((salida,))
            ]
            padre1.modelo.layers[i].set_weights(peso_hijo1)
            padre2.modelo.layers[i].set_weights(peso_hijo2)

    def mutacion(self, hijo1, hijo2):
        for hijo in [hijo1, hijo2]:
            if np.random.rand() < 0.1:
                lin = np.random.randint(0, len(hijo)-1)
                col = np.random.randint(0, len(hijo[0])-1)
                hijo[lin][col] += np.random.uniform(-1.0, 1.0)

        return hijo1, hijo2
    
    def exportaMejor(self):
        self.mejor[1].exporta()

    def get_weights_from_model(self, model):
            weights_list = []
            for layer in model.layers:
                weights_list.append(layer.get_weights())
            return weights_list

    def set_weights_to_model(self, model, weights_list):
        current_index = 0
        for layer in model.layers:
            layer.set_weights(weights_list[current_index])
            current_index += 1

    def crea_poblacion_cargada(self, ruta, sigma=0.01):
        
        model = tf.keras.models.load_model(ruta)

        poblacion_variada = []
        initial_weights = self.get_weights_from_model(model)

        for _ in range(self.num_poblacion):
            perturbed_weights = []
            for weights_array in initial_weights:
                perturbed1 = weights_array[0] + np.random.uniform(-sigma, sigma, size=weights_array[0].shape)
                perturbed2 = weights_array[1] + np.random.uniform(-sigma, sigma, size=weights_array[1].shape)
                perturbed_weights.append([perturbed1, perturbed2])
            poblacion_variada.append(perturbed_weights)
        
        for _ in range(self.num_poblacion):
            self.poblacion.append(Cerebro(sobre_carga=True))

        for i in range(len(self.poblacion)):
            if i == 0:
                self.poblacion[i].modelo = model
            else:
                self.set_weights_to_model(self.poblacion[i].modelo, poblacion_variada[i])
            self.poblacion[i].nuevo_interprete()

    def crea_poblacion_historica(self, ruta_abs):
        archivos = os.listdir(ruta_abs)
        archivos = [f for f in archivos if f.endswith(".h5")]
        cont = 0
        self.num_poblacion = len(archivos)
        self.usuarios = self.usuarios[0:self.num_poblacion]
        for i in archivos:
            self.poblacion.append(Cerebro(ruta=f"{ruta_abs}/{i}"))
            cont += 1
        return self.usuarios, self.num_poblacion