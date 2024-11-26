import pygame
import math

class Mapa:
    def __init__(self):
        self.barra1 = pygame.Rect(200, 180, 20, 150)
        self.barra2 = pygame.Rect(300, 100, 20, 50)
        self.barra3 = pygame.Rect(300, 350, 20, 50)
        self.pol = [(60, 100), (60, 400), (600, 400), (600, 100)]
        self.ancho_pol = 20
        # Crear rectas del polígono
        self.lados_pol = []
        for i in range(len(self.pol)):
            start = self.pol[i]
            end = self.pol[(i + 1) % len(self.pol)]
            recta = self.crear_recta(start, end)
            self.lados_pol.append(recta)

    def crear_recta(self, punto1, punto2):
        if punto1[0] == punto2[0]:  # Recta vertical
            recta = pygame.Rect(punto1[0] - self.ancho_pol / 2, punto1[1], self.ancho_pol, punto2[1] - punto1[1])
        elif punto1[1] == punto2[1]:  # Recta horizontal
            recta = pygame.Rect(punto1[0], punto1[1] - self.ancho_pol / 2, punto2[0] - punto1[0], self.ancho_pol)
        else:  # Recta inclinada
            diferencia_x = punto2[0] - punto1[0]
            diferencia_y = punto2[1] - punto1[1]
            pendiente = diferencia_y / diferencia_x
            angulo = abs(math.atan(pendiente))

            delta_x = self.ancho_pol / 2 * math.sin(angulo)
            delta_y = self.ancho_pol / 2 * math.cos(angulo)

            recta = pygame.Rect(punto1[0] - delta_x, punto1[1] - delta_y, punto2[0] - punto1[0] + 2 * delta_x, punto2[1] - punto1[1] + 2 * delta_y)

        return recta

    def Show(self, surface):
        surface.fill((0, 0, 0))
        # pygame.draw.polygon(surface, (255, 255, 255), self.pol, self.ancho_pol)
        # pygame.draw.rect(surface, (255, 255, 255), self.barra1)
        # pygame.draw.rect(surface, (255, 255, 255), self.barra2)
        # pygame.draw.rect(surface, (255, 255, 255), self.barra3)