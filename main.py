from datetime import time

import pygame
from pygame.transform import scale

import var
from var import *


'''
Cambios desde el ultimo Dia:
    -Puedes cojer monedas por el camino del laberinto
    -Te aparece el numero de monedas acumuladas
    -Si teminas el laberinto con menos de 5 monedas, vuelves al inicio
    -Mensaje de Despedida cunado le das a salir con el juego iniciado
'''
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
VIOLETA = (255, 0, 255)
tiempo =round((pygame.time.get_ticks()/1000),0)
pygame.init()

# Definicion de tipo de letra
small_font = pygame.font.SysFont('Corbel', 35)
small2_font = pygame.font.SysFont('Corbel', 20)

pantalla = pygame.display.set_mode([800, 600])

pygame.display.set_caption('Laberinto ')

bienvenida = small_font.render('Bienvenido', True, white)
salir = small_font.render('Salir', True, white)
jugar = small_font.render('Jugar', True, white)
adios = small_font.render('Hasta luego', True, white)
clickSalir = small_font.render('Clicke para salir', True, white)

paredes = []

def cargarImages():
    img = []
    img.append(pygame.image.load("img/caldero/caldera.png"))
    return img


class Moneda:
    def __init__(self, x, y):
        img = pygame.image.load('img/monedas/pocion-magica.png')
        scale = 0.05
        self.x = x
        self.y = y

        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        self.rect.topleft = (self.x, self.y)
        pantalla.blit(self.image, self.rect)


class Caldero:
    def __init__(self, x, y):
        img = pygame.image.load('img/monedas/pocion-magica.png')
        scale = 0.05
        self.x = x
        self.y = y

        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        self.rect.topleft = (self.x, self.y)
        pantalla.blit(self.image, self.rect)


class Pared(pygame.sprite.Sprite):

    def __init__(self, pos):
        paredes.append(self)
        self.image = pygame.Surface([pos[0], pos[1]])
        self.image.fill(ROJO)

        self.rect = self.image.get_rect()
        self.rect.y = pos[0]
        self.rect.x = pos[1]



class Protagonista(pygame.sprite.Sprite):  # Funcion constructora del cuadrado con movimiento

    # Velocidades iniciales
    cambio_x = 0
    cambio_y = 0

    def __init__(self, x, y):

        super().__init__()
        img = pygame.image.load('img/mago/0.png')
        self.image = pygame.transform.scale(img, (20, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False

    def cambiovelocidad(self, x, y):  # Cambia de velocidad con pulsar el teclado
        self.cambio_x += x
        self.cambio_y += y

    def mover(self, paredes):
        # desplazamiento Horizontal
        self.rect.x += self.cambio_x

        # Choco contra una pared??
        lista_impactos_bloques = pygame.sprite.spritecollide(self, paredes, False)
        for bloque in lista_impactos_bloques:
            # Si nos estamos desplazando hacia la derecha, hacemos que nuestro lado derecho sea el lado izquierdo del objeto que hemos tocado.
            if self.cambio_x > 0:
                self.rect.right = bloque.rect.left
            else:
                # Si no, nos desplazamos hacia la izquierda, lo hacemos que sea el derecho.
                self.rect.left = bloque.rect.right

        # Desplazamiento vertical
        self.rect.y += self.cambio_y

        # se ha chocado con algo???
        lista_impactos_bloques = pygame.sprite.spritecollide(self, paredes, False)
        for bloque in lista_impactos_bloques:

            # Cambiamos nuestra posicion
            if self.cambio_y > 0:
                self.rect.bottom = bloque.rect.top
            else:
                self.rect.top = bloque.rect.bottom


class Enemigo(pygame.sprite.Sprite):  # Funcion constructora del cuadrado con movimiento

    # Velocidades iniciales
    cambio_x = 0
    cambio_y = 0

    def __init__(self, x, y):

        super().__init__()
        img = pygame.image.load('img/enemigo/monster.png')
        self.image = pygame.transform.scale(img, (20, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad_x = 5
        self.velocidad_y = 5
        self.contador = 0  #Contador para dsitancia

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        # Limita el margen derecho
        if self.rect.right > var.display_width:
            self.rect.right = var.display_width

        # Limita el margen izquierdo
        if self.rect.left < 0:
            self.rect.left = 0

        # Limita el margen inferior
        if self.rect.bottom > var.display_height:
            self.rect.bottom = var.display_height

        # Limita el margen superior
        if self.rect.top < 0:
            self.rect.top = 0

    def cambiovelocidad(self, x, y):  # Cambia de velocidad con pulsar el teclado
        self.cambio_x += x
        self.cambio_y += y

    def dibujar(self):
        self.rect.topleft = (self.x, self.y)

        pantalla.blit(self.image, self.rect)
    def mover(self):
        # desplazamiento Horizontal
        distancia = 20
        velocidad = 8

        if self.contador >= 0 and self.contador <= distancia:
            self.rect.x += velocidad
        elif self.contador >= distancia and self.contador <= distancia * 2:
            self.rect.x -= velocidad
        else:
            self.contador = 0

        self.contador += 1
        self.rect.x += self.cambio_x






class Cuarto():
    # Cada cuarto tiene una lista de paredes, y de los sprites enemigos.
    pared_lista = None
    sprites_enemigos = None

    def __init__(self):
        """ Constructor, creamos nuestras listas. """
        self.pared_lista = pygame.sprite.Group()
        self.sprites_enemigos = pygame.sprite.Group()


class Cuarto1(Cuarto):
    """Esto crea todas las paredes del cuarto 1"""

    def __init__(self):
        super().__init__()
        # Crear las paredes. (x_pos, y_pos, ancho, alto)
        #well, well, look who´s inside again
        #scream at my refleaction, ¿what the hell is wrong with me?

        # Esta es la lista de las paredes. Cada una se especifica de la forma [x, y, largo, alto]
        level = [
            "WWWWWWWWWWWWWWWWWWWW",
            "W                  W",
            "W         WWWWWW   W",
            "W   WWWWWWWWWWWW   W",
            "W   W        WWWW  W",
            "W WWW  WWWW        W",
            "W   W     W W      W",
            "W   W     W   WWW WW",
            "W   WWW WWW   W W  W",
            "W     W   W   W W  W",
            "WWW   W   WWWWW W  W",
            "W W      WW        W",
            "W W   WWWW   WWW   W",
            "W     W    E   W   W",
            "WWWWWWWWWWWWWWWWWWWW",
        ]
        x = y = 0
        al = 10
        an = 10

        for row in level:
            for col in row:
                if col == "W":
                    Pared((x, y))
                    self.pared_lista.add(row)
                if col == "E":
                    end_rect = pygame.Rect(x, y, 16, 16)
                    self.pared_lista.add(row)
                x += 16
            y += 16
            x = 0


class Cuarto2(Cuarto):

    def __init__(self):
        super().__init__()
        # Crear las paredes. (x_pos, y_pos, ancho, alto)

        # Esta es la lista de las paredes. Cada una se especifica de la forma [x, y, largo, alto]
        level = [
            "WWWWWWWWWWWWWWWWWWWW",
            "W                  W",
            "W         WWWWWW   W",
            "W   WWWWWWWWWWWW   W",
            "W   W        WWWW  W",
            "W WWW  WWWW        W",
            "W   W     W W      W",
            "W   W     W   WWW WW",
            "W   WWW WWW   W W  W",
            "W     W   W   W W  W",
            "WWW   W   WWWWW W  W",
            "W W      WW        W",
            "W W   WWWW   WWW   W",
            "W     W    E   W   W",
            "WWWWWWWWWWWWWWWWWWWW",
        ]
        x = y = 0
        al = 10
        an = 10

        for row in level:
            for col in row:
                if col == "W":
                    Pared((x, y))
                if col == "E":
                    end_rect = pygame.Rect(x, y, 16, 16)
                x += 16
            y += 16
            x = 0


class Cuarto3(Cuarto):

    def __init__(self):
        super().__init__()
        # Crear las paredes. (x_pos, y_pos, ancho, alto)

        # Esta es la lista de las paredes. Cada una se especifica de la forma [x, y, largo, alto]
        level = [
            "WWWWWWWWWWWWWWWWWWWW",
            "W                  W",
            "W         WWWWWW   W",
            "W   WWWWWWWWWWWW   W",
            "W   W        WWWW  W",
            "W WWW  WWWW        W",
            "W   W     W W      W",
            "W   W     W   WWW WW",
            "W   WWW WWW   W W  W",
            "W     W   W   W W  W",
            "WWW   W   WWWWW W  W",
            "W W      WW        W",
            "W W   WWWW   WWW   W",
            "W     W    E   W   W",
            "WWWWWWWWWWWWWWWWWWWW",
        ]
        x = y = 0
        al = 10
        an = 10

        for row in level:
            for col in row:
                if col == "W":
                    Pared((x, y))
                if col == "E":
                    end_rect = pygame.Rect(x, y, 16, 16)
                x += 16
            y += 16
            x = 0


def main():
    while True:

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()

                # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on the
                # button the game is terminated
                if display_width / 2 <= mouse[0] <= display_width / 2 + 140 and display_height / 2 <= mouse[
                    1] <= display_width / 2 + 40:
                    pygame.quit()
                if display_width / 2 - 175 <= mouse[0] <= display_width / 2 + 140 and display_height / 2 <= mouse[
                    1] <= display_width / 2 + 40:
                    print('ha seleccionado jugar')
                    lab1()

        # (x,y)
        # La variable es una tupla
        mouse = pygame.mouse.get_pos()

        # Cambia a un color mas claro si lo pasas por encima ---> Salir
        if display_width / 2 <= mouse[0] <= display_width / 2 + 140 and display_height / 2 <= mouse[
            1] <= display_height / 2 + 40:
            rect1 = pygame.draw.rect(pantalla, color_light, [display_width / 2, display_height / 2, 140, 40])
        # Vuelve al color original
        else:
            rect1 = pygame.draw.rect(pantalla, color_dark, [display_width / 2, display_height / 2, 140, 40])
        # Cambia a un color mas claro si lo pasas por encima ---> Jugar
        if display_width / 2 - 175 <= mouse[0] <= display_width / 2 + 140 and display_height / 2 <= mouse[
            1] <= display_height / 2 + 40:
            rect2 = pygame.draw.rect(pantalla, color_light, [display_width / 2 - 175, display_height / 2, 140, 40])

        # Vuelve al color original
        else:
            rect2 = pygame.draw.rect(pantalla, color_dark, [display_width / 2 - 175, display_height / 2, 140, 40])

            # superimposing the text onto our button
        pantalla.blit(bienvenida, (display_width / 2 -100, display_height / 2-200))
        pantalla.blit(salir, (display_width / 2 + 50, display_height / 2))
        pantalla.blit(jugar, (display_width / 2 - 150, display_height / 2))
        # updates the frames of the game
        pygame.display.update()


def lab1():
    protagonista = Protagonista(50, 50)  # Creamos un protagonista
    enemingo1 = Enemigo(50,150)
    enemigos_lista = pygame.sprite.Group()
    enemigos_lista.add(enemingo1)
    monedas = [

        Moneda(250, 150),
         Moneda(550, 40),
        Moneda(500, 250), Moneda(400, 400),
        Moneda(700, 300), Moneda(200, 450),
         Moneda(700, 75),

        Moneda(200, 180),Moneda(170, 100),
        Moneda(100, 290),

    ]  # hay 10 monedas

    desplazarsprites = pygame.sprite.Group()
    desplazarsprites.add(protagonista)
    desplazarsprites.add(enemingo1)
    cuartos = []
    cuarto = Cuarto1()
    cuartos.append(cuarto)
    cuarto = Cuarto2()
    cuartos.append(cuarto)
    cuarto = Cuarto3()
    cuartos.append(cuarto)
    cuarto_actual_no = 0
    cuarto_actual = cuartos[cuarto_actual_no]
    puntuacion = 0
    vida = 10

    reloj = pygame.time.Clock()

    #Movimiento enemigo 2
    enemingo1.update()



    hecho = False
    while not hecho:

        # --- Procesamiento de Eventos ---

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salida()
                hecho = True
            if tiempo == 10000:
                hecho = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    protagonista.cambiovelocidad(-5, 0)
                if evento.key == pygame.K_RIGHT:
                    protagonista.cambiovelocidad(5, 0)
                if evento.key == pygame.K_UP:
                    protagonista.cambiovelocidad(0, -5)
                if evento.key == pygame.K_DOWN:
                    protagonista.cambiovelocidad(0, 5)

            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT:
                    protagonista.cambiovelocidad(5, 0)
                if evento.key == pygame.K_RIGHT:
                    protagonista.cambiovelocidad(-5, 0)
                if evento.key == pygame.K_UP:
                    protagonista.cambiovelocidad(0, 5)
                if evento.key == pygame.K_DOWN:
                    protagonista.cambiovelocidad(0, -5)

        # --- Lógica del Juego ---

        protagonista.mover(cuarto_actual.pared_lista)

        if protagonista.rect.x > 801:  # se mueve hacia la derecha
            # Comprobar si la puntuacion es mayor a 5
            if puntuacion > 4:
                cuarto_actual_no = 2
                cuarto_actual = cuartos[cuarto_actual_no]
                protagonista.rect.x = 0
                protagonista.rect.y = 700
                for i in range(len(monedas) - 1, -1, -1):
                    del monedas[i]


            else:
                cuarto_actual_no = 0
                cuarto_actual = cuartos[cuarto_actual_no]
                protagonista.rect.x = 25
                protagonista.rect.x = 25

        for i in range(len(monedas) - 1, -1, -1):
            if protagonista.rect.colliderect(monedas[i].rect):
                del monedas[i]
                puntuacion += 1
        if protagonista.rect.colliderect(enemingo1.rect):
            while protagonista.rect.colliderect((enemingo1.rect)):
                vida -= 1
                # --- Dibujamos ---
        pantalla.fill(BLANCO)
        text = small_font.render('User = ' + str('usuario_actual'), True, ROJO) #APareceria el nombre del usuario
        textRect = text.get_rect()
        textRect.center = (500, 40)


        desplazarsprites.draw(pantalla)
        tiempo = round((pygame.time.get_ticks() / 1000), 0)
        if (tiempo == 100.0):
            pygame.quit()
        cuarto_actual.pared_lista.draw(pantalla)
        text = small2_font.render('Puntuacion = ' + str(puntuacion), True, VERDE)
        textRect = text.get_rect()
        textRect.center = (100, 10)
        pantalla.blit(text, textRect)
        text = small2_font.render('Vida = ' + str(vida), True, VERDE)
        textRect = text.get_rect()
        textRect.center = (300, 10)
        pantalla.blit(text, textRect)
        text = small2_font.render('User = ' + str('usuario_actual'), True, ROJO)
        textRect = text.get_rect()
        textRect.center = (500, 10)
        pantalla.blit(text, textRect)
        text2 = small2_font.render('tiempo = ' + str(tiempo), True, ROJO)
        textRect2 = text2.get_rect()
        textRect2.center = (700, 10)
        pantalla.blit(text2, textRect2)
        for moneda in monedas:
            moneda.draw()

        pygame.display.flip()

        reloj.tick(60)








def salida():
    pantalla.fill(VERDE)

    while True:
        tiempo = round((pygame.time.get_ticks() / 1000), 0)
        if (tiempo == 10.0):
            pygame.quit()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()



def inicializar_datos():
    puntuacion = 0
    text = small2_font.render('Puntuacion = ' + str(puntuacion), True, VERDE)
    textRect = text.get_rect()
    textRect.center = (100, 10)
    pantalla.blit(text, textRect)


if __name__ == "__main__":
    main()
