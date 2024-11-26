from tensorflow.keras.layers import Dense
from tensorflow.keras import Sequential
import tensorflow as tf
from numpy import array, float32

#Variables: 6 sensores
#Salidas: adelante, atras, derecha, izquierda

class Cerebro:

    def __init__(self, ruta = None, sobre_carga = False, clonado = None):
        if ruta != None:
            self.usar_modelo(ruta)
            self.nuevo_interprete()
        elif clonado != None:
            self.clona_modelo(clonado)
        else:
            entrada = Dense(units=6, input_shape=(6,))
            oculta = Dense(units=12, activation="relu")
            oculta1 = Dense(units=6, activation="relu")
            salida = Dense(units=4, activation='sigmoid')
            self.modelo = Sequential([entrada, oculta, oculta1, salida])
            if not sobre_carga:
                self.nuevo_interprete()
    
    def predice(self, entradas):
        entradas = array(entradas).astype(float32)
        self.interprete.set_tensor(self.interprete.get_input_details()[0]["index"], entradas)
        self.interprete.invoke()
        prediccion = self.interprete.get_tensor(self.interprete.get_output_details()[0]["index"])
        prediccion = prediccion[0]
        prediccion_ava = tuple(prediccion[0:2])
        prediccion_vuel = tuple(prediccion[2:4])
        #Saber si avanza o retrocede
        avanza = max(prediccion_ava)
        if avanza >= 0.5:
            if prediccion_ava.index(avanza) == 0:
                prediccion[0] = 1
                prediccion[1] = 0
            else:
                prediccion[1] = 1
                prediccion[0] = 0
        else:
            prediccion[0] = 0
            prediccion[1] = 0
        #Saber si gira a derecha o izquierda
        voltea = max(prediccion_vuel)
        if voltea >= 0.5:
            if prediccion_vuel.index(voltea) == 0:
                prediccion[2] = 1
                prediccion[3] = 0
            else:
                prediccion[3] = 1
                prediccion[2] = 0
        else:
            prediccion[2] = 0
            prediccion[3] = 0

        return prediccion
    
    def clona_modelo(self, new_modelo):
        self.modelo = tf.keras.models.clone_model(new_modelo)
        for i in range(len(self.modelo.layers)):
            self.modelo.layers[i].set_weights(new_modelo.layers[i].get_weights())
        self.nuevo_interprete()

    def nuevo_interprete(self):
        converter = tf.lite.TFLiteConverter.from_keras_model(self.modelo)
        tflite_model = converter.convert()
        self.interprete = tf.lite.Interpreter(model_content=tflite_model)
        self.interprete.allocate_tensors()
    
    def exporta(self):
        self.modelo.save('best_model.h5')

    def usar_modelo(self, ruta):
        self.modelo = tf.keras.models.load_model(ruta)