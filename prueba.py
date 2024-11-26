import tensorflow as tf
import pygame
import sys
import math
from Mapa import Mapa
from Usuario import Usuario
from Sensores import Sensores
from Cerebro import Cerebro

ruta = 'models\\best_model1.h5'
modelo = tf.keras.models.load_model(ruta)

for i in range(len(modelo.layers)):
    print(modelo.layers[i].get_weights()[0])

pygame.init()
clock = pygame.time.Clock()

screenwidth, screenheight = (640, 480)

screen = pygame.display.set_mode((screenwidth, screenheight))

pygame.mouse.set_visible(1)

pygame.display.set_caption('Plataforma')


velocidad = 0
angulo = 0
temp_ang = 0

mapa = Mapa()
usuario = Usuario(mapa)
sensor = Sensores(usuario)
piloto = Cerebro(ruta=ruta)
usuarios = []
usuarios.append([usuario, sensor, usuario.x, usuario.y, velocidad, angulo, 0, 400, 0, 0])


def obten_parametros(user):
    parametros = []
    for distancia in user[1].toques:
        if distancia == None:
            parametros.append(1)
        else:
            parametros.append(distancia[0][2])
    return [parametros]

max_time = 3000

font = pygame.font.SysFont('arial', 18)
text2 = font.render('HOLA', True, (255, 0, 0), (255, 255, 255))
textRect2 = text2.get_rect()
textRect2.center = (300, 46)

while True:
    
    time = clock.tick(60)/10

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit() 
    
    mapa.Show(screen)
    
    if max_time == 0 or usuarios[0][7] == 0:
        sys.exit()
    else:
        text2 = f"Tiempo: {str(max_time)}"
        screen.blit(font.render(text2, True, (255, 0, 0), (255, 255, 255)), textRect2)

    for user in usuarios:
        next_move = piloto.predice(obten_parametros(user))
        print(next_move)
        #Adelante o atras
        if next_move[0] == 1:
            user[4] = 2
        elif next_move[1] == 1:
            user[4] = -2
        else:
            user[4] = 0
        #Izquierda o derecha
        if next_move[2] == 1:
            temp_ang = 0.05
        elif next_move[3] == 1:
            temp_ang = -0.05
        else:
            temp_ang = 0
        
        #Nueva posicion
        user[5] += temp_ang
        user[2] += user[4]*math.cos(user[5])
        user[3] += user[4]*math.sin(user[5])
        if not user[0].simula(user[2], user[3], user[5]):
            user[0].updateCoord(user[2], user[3])
            if next_move[0] == 1 or next_move[1] == 1:
                user[8] += 1
        else:
            user[7] -= 1
            user[2] += -1*user[4]*math.cos(user[5])
            user[3] += -1*user[4]*math.sin(user[5])
            user[5] += -1*temp_ang
        if user[5] == 0:
            user[0].Show(screen, user[5])
        else:
            user[0].Rotate(screen, user[5])
        user[6] = len(user[1].intersecciones)
        user[1].Show(screen, user[5])

    max_time -= 1
    # usuarios = sorted(usuarios, key=lambda x: [x[6], x[8], x[7]], reverse=True)
    print("NUEVO")
    for i in usuarios:
        print(f"user: {i[9]}, puntos: {i[6]}, choques: {i[7]}, desplazo: {i[8]}")
    usuarios[0][1].Show_data(screen)

    pygame.display.update()