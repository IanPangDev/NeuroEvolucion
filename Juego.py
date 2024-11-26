import pygame
import sys
import math
from Mapa import Mapa
from Usuario import Usuario
from Sensores import Sensores
from Genetico import Genetico

modo = 2
ruta = 'models\\best_model.h5'

pygame.init()
clock = pygame.time.Clock()

screenwidth, screenheight = (640, 480)

screen = pygame.display.set_mode((screenwidth, screenheight))

pygame.mouse.set_visible(1)

pygame.display.set_caption('Mapeado')

num_poblacion = 20
num_generaciones = 20
usuarios = []
velocidad = 0
angulo = 0
temp_ang = 0


mapa = Mapa()
for i in range(num_poblacion):
    usuario = Usuario(mapa)
    sensor = Sensores(usuario)
    usuarios.append([usuario, sensor, usuario.x, usuario.y, velocidad, angulo, 0, 400, 0, i])

poblacion = Genetico(num_poblacion, num_generaciones, usuarios)

#Pesos cargados
if modo == 1:
    poblacion.crea_poblacion()
elif modo == 2:
    poblacion.crea_poblacion_cargada(ruta)
elif modo == 3:
    usuarios, num_poblacion = poblacion.crea_poblacion_historica(ruta)


def obten_parametros(user):
    parametros = []
    for distancia in user[1].toques:
        if distancia == None:
            parametros.append(1)
        else:
            parametros.append(distancia[0][2])
    return [parametros]

betados = []
tiempo = 2000
max_time = tiempo

font = pygame.font.SysFont('arial', 18)
text1 = font.render('HOLA', True, (255, 0, 0), (255, 255, 255))
text2 = font.render('HOLA', True, (255, 0, 0), (255, 255, 255))
text3 = font.render('HOLA', True, (255, 0, 0), (255, 255, 255))
textRect1 = text1.get_rect()
textRect2 = text2.get_rect()
textRect3 = text3.get_rect()
textRect1.center = (300, 10)
textRect3.center = (300, 28)
textRect2.center = (300, 46)

cont = 1
while True:
    
    time = clock.tick(60)/10

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit() 
    
    mapa.Show(screen)
    
    if len(betados) == len(usuarios) or max_time == 0:
        if num_generaciones-1 != 0:
            num_generaciones -= 1
            poblacion.selecciona_mejores(usuarios)
            usuarios = []
            betados = []
            for i in range(num_poblacion):
                usuario = Usuario(mapa)
                sensor = Sensores(usuario)
                usuarios.append([usuario, sensor, usuario.x, usuario.y, velocidad, angulo, 0, 400, 0, i])
            max_time = tiempo
            cont += 1
        else:
            poblacion.exportaMejor()
            sys.exit()
    else:
        text1 = f"Quedan: {str(len(usuarios)-len(betados))}"
        text2 = f"Tiempo: {str(max_time)}"
        text3 = f"Generacion: {str(cont)}"
        screen.blit(font.render(text1, True, (255, 0, 0), (255, 255, 255)), textRect1)
        screen.blit(font.render(text3, True, (255, 0, 0), (255, 255, 255)), textRect3)
        screen.blit(font.render(text2, True, (255, 0, 0), (255, 255, 255)), textRect2)

    for user in usuarios:
        if user[9] not in betados:
            next_move = poblacion.poblacion[user[9]].predice(obten_parametros(user))
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
            if user[7] == 0:
                betados.append(user[9])

    max_time -= 1
    usuarios = sorted(usuarios, key=lambda x: [x[6], x[7], x[8]], reverse=True)
    print("NUEVO")
    for i in usuarios:
        print(f"user: {i[9]}, puntos: {i[6]}, choques: {i[7]}, desplazo: {i[8]}")
    for i in range(len(usuarios)):
        if usuarios[i][9] not in betados:
            usuarios[i][1].Show_data(screen)
            break

    pygame.display.update()