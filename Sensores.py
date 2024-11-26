import pygame
import math

class Sensores:
    def __init__(self, usuario):
        self.num_sensores = 10
        self.usuario = usuario
        self.longitud = 50
        self.separacion = 2*math.pi
        self.num_sensores = 6
        self.sensores = []
        self.toques = []
        self.intersecciones = []
        self.lineas = self.ObtenLineas()
        self.Update(0)

    def ObtenLineas(self):
        lineas = []
        for i in self.usuario.obstaculos:
            lineas.append(((i.topright), (i.bottomright)))
            lineas.append(((i.topleft), (i.bottomleft)))
            lineas.append(((i.topright), (i.topleft)))
            lineas.append(((i.bottomright), (i.bottomleft)))
        return lineas
    
    def Update(self, angulo):
        self.sensores = []
        for i in range(self.num_sensores):
            angulo_Interpolado = (i+1)*(self.separacion/self.num_sensores)
            centro = self.usuario.shape.get_rect(topleft = (self.usuario.x, self.usuario.y)).center
            angulo_Interpolado += angulo
            final = (centro[0]+math.cos(angulo_Interpolado)*self.longitud, 
                    centro[1]+math.sin(angulo_Interpolado)*self.longitud)
            self.sensores.append((centro, final))
        self.toques = []
        for i in range(len(self.sensores)):
            self.toques.append(self.Reading(self.sensores[i], self.lineas))

    def Reading(self, sensores, borders):
        toques = []
        for i in range(len(borders)):
            toque = self.Interseccion(sensores[0], sensores[1],
            borders[i][0], borders[i][1])
            if toque:
                toques.append(toque)

        if len(toques) == 0:
            return None
        else:
            salidas = list(map(lambda x: x[2], toques))
            minSalida = min(salidas)
            return [x for x in toques if x[2] == minSalida]

    def Interseccion(self, A, B, C, D):
        tTop = (D[0]-C[0])*(A[1]-C[1])-(D[1]-C[1])*(A[0]-C[0])
        uTop = (C[1]-A[1])*(A[0]-B[0])-(C[0]-A[0])*(A[1]-B[1])
        bottom = (D[1]-C[1])*(B[0]-A[0])-(D[0]-C[0])*(B[1]-A[1])

        if bottom != 0:
            t = tTop/bottom
            u = uTop/bottom
            if t >= 0 and t <= 1 and u >= 0 and u <= 1:
                return [self.Lerp(A[0], B[0], t),
                    self.Lerp(A[1], B[1], t),
                    t]
        return None

    def Show(self, surface, angulo):
        self.Update(angulo)
        for i in range(self.num_sensores):
            if self.toques[i]:
                pygame.draw.line(surface, (255, 0, 0), 
                self.sensores[i][0], (self.toques[i][0][0], self.toques[i][0][1]), 2)
                if (round(self.toques[i][0][0]), round(self.toques[i][0][1])) not in self.intersecciones:
                    self.intersecciones.append((round(self.toques[i][0][0]), round(self.toques[i][0][1])))
                pygame.draw.line(surface, (0, 0, 0), 
                self.sensores[i][1], (self.toques[i][0][0], self.toques[i][0][1]), 2)
            else:
                pygame.draw.line(surface, (255, 0, 0), 
                self.sensores[i][0], self.sensores[i][1], 2)

    def Show_data(self, surface):
        for i in range(self.num_sensores):
            if len(self.intersecciones) > 1:
                for i in self.intersecciones:
                    pygame.draw.circle(surface, (255, 0, 0), i, 2)

    
    def Lerp(self, start, end, t):
        return ((1-t)*start)+(t*end)