import pygame
import math

class Usuario:
    def __init__(self, mapa):
        self.shape = pygame.image.load('cuadrado.png')
        self.shape = pygame.transform.scale(self.shape, (20, 20))
        self.x = 90
        self.y = 240
        self.angulo = 0
        self.obstaculos = self.rectasMapa(mapa)
        self.puntos = []

    def Show(self, surface, angulo):
        self.angulo = angulo
        pygame.draw.polygon(surface, (0, 0, 0), self.Poligono())
        surface.blit(self.shape, (self.x, self.y))

    def Rotate(self, surface, angulo):
        self.angulo = angulo
        cuadro_rotado = pygame.transform.rotate(self.shape, math.degrees(-self.angulo))
        new_rect = cuadro_rotado.get_rect(
            center = self.shape.get_rect(topleft = (self.x, self.y)).center)
        pygame.draw.polygon(surface, (0, 0, 0), self.Poligono())
        surface.blit(cuadro_rotado, new_rect)

    def Poligono(self):
        self.puntos = []
        x, y = self.shape.get_rect(topleft = (self.x, self.y)).center
        rad = math.hypot(self.shape.get_width(), self.shape.get_height())/2
        alpha = math.atan2(self.shape.get_width(), self.shape.get_height())
        self.puntos.append([x-math.cos(self.angulo-alpha)*rad, y-math.sin(self.angulo-alpha)*rad])
        self.puntos.append([x-math.cos(self.angulo+alpha)*rad, y-math.sin(self.angulo+alpha)*rad])
        self.puntos.append([x-math.cos(math.pi+self.angulo-alpha)*rad, y-math.sin(math.pi+self.angulo-alpha)*rad])
        self.puntos.append([x-math.cos(math.pi+self.angulo+alpha)*rad, y-math.sin(math.pi+self.angulo+alpha)*rad])
        return self.puntos

    def updateCoord(self, x, y):
        self.x = x-self.shape.get_width()/2
        self.y = y-self.shape.get_height()/2

    def simula(self, x, y, angulo):
        antes_ang = self.angulo
        antes_x = self.x
        antes_y = self.y
        self.angulo = angulo
        self.x = x-self.shape.get_width()/2
        self.y = y-self.shape.get_height()/2
        self.Poligono()
        if self.Choque():
            self.x = antes_x
            self.y = antes_y
            self.angulo = antes_ang
            return True
        return False

    def rectasMapa(self, mapa):
        barras = [mapa.barra1, mapa.barra2, mapa.barra3]
        for i in mapa.lados_pol:
            barras.append(i)
        return barras

    def Choque(self):
        for recta1 in self.obstaculos:
            for i in range(len(self.puntos)):
            # Obtiene dos vértices adyacentes para formar un segmento de recta
                punto1 = self.puntos[i]

                # Crea una recta temporal utilizando los dos vértices
                recta_temporal = pygame.Rect(punto1[0], punto1[1], 1, 1)

                # Verifica si el segmento de recta colisiona con la recta definida
                if recta1.colliderect(recta_temporal):
                    return True
        return False
