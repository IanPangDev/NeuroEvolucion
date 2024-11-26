import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import yeojohnson
import numpy as np

fig = plt.figure()
ax = fig.subplots(2,2)
fig1 = plt.figure()
ax1 = fig1.subplots(2,2)
# fig1 = plt.figure()
# ax1 = fig1.subplots(2,2)

ruta1 = 'models\\best_model.h5'
ruta2 = 'models\\best_model1.h5'
model1 = tf.keras.models.load_model(ruta1)
model2 = tf.keras.models.load_model(ruta2)

cont = 1
x, y = 0, 0
data_normalizada = []
for i in range(len(model1.layers)):
    pesos1 = model1.layers[i].get_weights()[0]
    pesos2 = model2.layers[i].get_weights()[0]
    # salida = np.shape(i.get_weights()[1])[0]
    sns.distplot(pesos1, ax=ax[x, y])
    sns.distplot(pesos2, ax=ax1[x, y])
    # transformed_data, _ = yeojohnson(pesos.flatten())
    # sns.distplot(transformed_data, ax=ax1[x, y])
    # data_normalizada.append([transformed_data.reshape(
    #     np.shape(pesos)[0], np.shape(pesos)[1]),
    #     np.zeros(salida,)])
    # cont += 1
    if x == 0 and y == 1:
        x = 1
        y = 0
    else:
        y += 1

fig.suptitle("Modelo 1")
fig.tight_layout()
fig1.suptitle("Modelo 2")
fig1.tight_layout()
# fig1.tight_layout()
plt.show()

# for i in range(len(model.layers)):
#     model.layers[i].set_weights(data_normalizada[i])

# model.save(str(f"{ruta[0:len(ruta)-3]}_normal.h5"))