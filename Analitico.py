import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns

class Analitico:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.subplots(2,2)
    
    def grafica(self, modelo, iter):
        x, y = 0, 0
        for i in range(len(modelo.layers)):
            pesos = modelo.layers[i].get_weights()[0]
            sns.distplot(pesos, ax=self.ax[x, y])
            if x == 0 and y == 1:
                x = 1
                y = 0
            else:
                y += 1
        self.fig.tight_layout()
        plt.savefig(f'graficas/Iteracion_{iter}.png')
        plt.close()