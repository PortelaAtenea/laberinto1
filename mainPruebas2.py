import pygame
from pygame.transform import scale

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

GRAVITY = 0.75

pygame.init()

# Definicion de tipo de letra
small_font = pygame.font.SysFont('Corbel', 35)
small2_font = pygame.font.SysFont('Corbel', 20)

pantalla = pygame.display.set_mode([800, 600])

pygame.display.set_caption('Laberinto Principal')

salir = small_font.render('Salir', True, white)
jugar = small_font.render('Jugar', True, white)
adios = small_font.render('Hasta luego', True, white)
clickSalir = small_font.render('Clicke para salir', True, white)


def cargarImages():
    img = []
    img.append(pygame.image.load("img/caldero/caldera.png"))
    return img


class Moneda:
    def __init__(self, x, y):
        img = pygame.image.load('img/monedas/moneda.png')
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
        img = pygame.image.load('img/monedas/moneda.png')
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

    def __init__(self, x, y, largo, alto, color):  # Funcion contructora de una pared de 4 lados

        super().__init__()

        self.image = pygame.Surface([largo, alto])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


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


class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/mago/0.png')
        self.image = pygame.transform.scale(img, (20, 40))
        self.rect = self.image.get_rect()
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()



        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        # reset movement variables
        dx = 0
        dy = 0

        # assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy



    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        pantalla.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


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

        # Esta es la lista de las paredes. Cada una se especifica de la forma [x, y, largo, alto]
        paredes = [[0, 0, 20, 580, AZUL],
                   [0, 350, 20, 250, AZUL],
                   [780, 0, 20, 250, AZUL],
                   [780, 350, 20, 250, AZUL],
                   [20, 0, 760, 20, AZUL],
                   [20, 580, 760, 20, AZUL],
                   [100, 20, 20, 60, AZUL],  # 1
                   [100, 140, 160, 20, AZUL],  # 2
                   [240, 80, 20, 60, AZUL],  # 3
                   [240, 80, 210, 20, AZUL],  # 4
                   [240, 140, 20, 300, AZUL],  # 5
                   [0, 240, 150, 20, AZUL],  # 6
                   [150, 240, 20, 100, AZUL],  # 7
                   [70, 340, 100, 20, AZUL],  # 8
                   [70, 420, 170, 20, AZUL],  # 9
                   [160, 420, 20, 200, AZUL],  # 10
                   [0, 500, 100, 20, AZUL],  # 11
                   [450, 160, 400, 20, AZUL],  # 12
                   [450, 160, 20, 100, AZUL],  # 13
                   [350, 240, 100, 20, AZUL],  # 14
                   [350, 240, 20, 200, AZUL],  # 15
                   [160, 500, 200, 20, AZUL],  # 16
                   [350, 80, 20, 100, AZUL],  # 17
                   [450, 350, 400, 20, AZUL],  # 18
                   [550, 260, 20, 260, AZUL],  # 19
                   [650, 160, 20, 120, AZUL],  # 20
                   [650, 450, 200, 20, AZUL],  # 21
                   [450, 450, 20, 200, AZUL],  # 22
                   [350, 80, 20, 100, AZUL],  # 17

                   ]

        # Iteramos a través de la lista. Creamos la pared y la añadimos a la lista.
        for item in paredes:
            pared = Pared(item[0], item[1], item[2], item[3], item[4])
            self.pared_lista.add(pared)


class Cuarto2(Cuarto):
    """Esto crea todas las paredes del cuarto 2"""

    def __init__(self):
        super().__init__()

        paredes = [[0, 0, 20, 255, ROJO],
                   [0, 350, 20, 250, ROJO],
                   [780, 0, 20, 250, ROJO],
                   [780, 350, 20, 250, ROJO],
                   [20, 0, 760, 20, ROJO],
                   [20, 580, 760, 20, ROJO],  # 15
                   [160, 500, 200, 20, AZUL]
                   ]

        for item in paredes:
            pared = Pared(item[0], item[1], item[2], item[3], item[4])
            self.pared_lista.add(pared)

class Cuarto3(Cuarto):

    def __init__(self):
        super().__init__()
        # El ancho de las rayas es 20
        paredes = [[0, 0, 20, 255, VIOLETA],  # raya de arriba izquierda
                   [0, 350, 20, 250, VIOLETA],  # raya de abajo izquierda
                   [780, 0, 20, 250, VIOLETA],  # raya de arriba derecha
                   [780, 350, 20, 250, VIOLETA],  # raya de abajo derecha
                   [20, 0, 760, 20, VIOLETA],  # Raya de arriba de la pantalla
                   [20, 580, 760, 20, ROJO],  # 15
                   [160, 500, 200, 20, NEGRO],  # 15
                   [250, 85, 20, 200, NEGRO],  # 15
                   [160, 500, 200, 20, NEGRO],  # 15
                   [160, 500, 200, 20, NEGRO]  # Raya de abajo de la pantalla
                   ]
        # x, y, largo, alto
        for item in paredes:
            pared = Pared(item[0], item[1], item[2], item[3], item[4])
            self.pared_lista.add(pared)
        mago = Soldier('player', 200, 200, 3, 5)




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
            rect2 = pygame.draw.rect(pantalla, color_dark, [display_width / 2 - 175, display_height / 2, 140, 40])
        # Cambia a un color mas claro si lo pasas por encima ---> Jugar
        if display_width / 2 - 175 <= mouse[0] <= display_width / 2 + 140 and display_height / 2 <= mouse[
            1] <= display_height / 2 + 40:
            rect2 = pygame.draw.rect(pantalla, color_light, [display_width / 2 - 175, display_height / 2, 140, 40])

        # Vuelve al color original
        else:
            rect1 = pygame.draw.rect(pantalla, color_dark, [display_width / 2, display_height / 2, 140, 40])
            rect2 = pygame.draw.rect(pantalla, color_dark, [display_width / 2 - 175, display_height / 2, 140, 40])

            # superimposing the text onto our button
        pantalla.blit(salir, (display_width / 2 + 50, display_height / 2))
        pantalla.blit(jugar, (display_width / 2 - 150, display_height / 2))
        # updates the frames of the game
        pygame.display.update()


def lab1():
    protagonista = Protagonista(50, 50)  # Creamos un protagonista
    monedas = [
        Moneda(25, 150), Moneda(260, 250), Moneda(350, 23), Moneda(500, 40), Moneda(500, 250), Moneda(400, 400),
        Moneda(700, 300), Moneda(275, 450),
        Moneda(100, 100), Moneda(600, 100)

    ]  # hay 10 monedas

    desplazarsprites = pygame.sprite.Group()
    desplazarsprites.add(protagonista)
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

    reloj = pygame.time.Clock()

    hecho = False
    while not hecho:

        # --- Procesamiento de Eventos ---

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salida()
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
                for i in range(len(monedas) - 1, -1, -1):
                    del monedas[i]
                del protagonista



        else:
                cuarto_actual_no = 0
                cuarto_actual = cuartos[cuarto_actual_no]
                protagonista.rect.x = 25
                protagonista.rect.x = 25

        for i in range(len(monedas) - 1, -1, -1):
            if protagonista.rect.colliderect(monedas[i].rect):
                del monedas[i]
                puntuacion += 1
                # --- Dibujamos ---
        pantalla.fill(BLANCO)
        text = small_font.render('User = ' + str('usuario_actual'), True, ROJO) #APareceria el nombre del usuario
        textRect = text.get_rect()
        textRect.center = (500, 40)

        desplazarsprites.draw(pantalla)
        cuarto_actual.pared_lista.draw(pantalla)
        text = small2_font.render('Puntuacion = ' + str(puntuacion), True, VERDE)
        textRect = text.get_rect()
        textRect.center = (100, 10)
        pantalla.blit(text, textRect)
        text = small2_font.render('User = ' + str('usuario_actual'), True, ROJO)
        textRect = text.get_rect()
        textRect.center = (500, 10)
        pantalla.blit(text, textRect)
        for moneda in monedas:
            moneda.draw()
        pygame.display.flip()

        reloj.tick(60)






def lab2():
    caldero = Caldero(450,450)
    desplazarsprites = pygame.sprite.Group()
    cuartos = []
    cuarto = Cuarto3()
    cuartos.append(cuarto)
    cuarto_actual_no = 2
    cuarto_actual = cuartos[cuarto_actual_no]
    puntuacion = 0

    reloj = pygame.time.Clock()

    hecho = False
    while not hecho:

        # --- Procesamiento de Eventos ---

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salida()
                hecho = True


        # --- Lógica del Juego ---

        fin = False
        if fin:  # Acaba la prueba
            # Comprobar si la puntuacion es mayor a "La que sea"
            if puntuacion > 0:
                #pasa ala siguiente prueba
                print('se paso la fase')

            else:
                #El juego vuelve a empezar
                print('No se paso al fase')

                # --- Dibujamos ---
        pantalla.fill(BLANCO)

        desplazarsprites.draw(pantalla)
        cuarto_actual.pared_lista.draw(pantalla)
        text = small2_font.render('Puntuacion = ' + str(puntuacion), True, VERDE)
        textRect = text.get_rect()
        textRect.center = (100, 10)
        pantalla.blit(text, textRect)
        text = small2_font.render('User = ' + str('usuario_actual'), True, ROJO)
        textRect = text.get_rect()
        textRect.center = (500, 10)
        pantalla.blit(text, textRect)
        text = small2_font.render('Fase en desarrollo', True, ROJO)
        textRect = text.get_rect()
        textRect.center = (500, 500)
        pantalla.blit(text, textRect)
        pygame.display.flip()

        reloj.tick(60)






def salida():
    pantalla.fill(VERDE)

    while True:

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on the
                # button the game is terminated
                if display_width / 2 +25 <= mouse[0] <= display_width / 2 + 200 and display_height / 2 <= mouse[
                    1] <= display_width / 2 + 40:
                    pygame.quit()

        # (x,y)
        # La variable es una tupla
        mouse = pygame.mouse.get_pos()

        # Cambia a un color mas claro si lo pasas por encima ---> Salir
        if display_width / 2-100 <= mouse[0] <= display_width / 2 + 300 and display_height / 2 <= mouse[
            1] <= display_height / 2 + 40:
            rect1 = pygame.draw.rect(pantalla, color_light, [display_width / 2-100, display_height / 2, 300, 40])
        # Vuelve al color original
        else:
            rect1 = pygame.draw.rect(pantalla, color_dark, [display_width / 2-100, display_height / 2, 300, 40])


            # superimposing the text onto our button
        pantalla.blit(adios, (display_width / 2 -20, display_height / 2 - 150))
        pantalla.blit(clickSalir, (display_width / 2 - 75, display_height / 2 +5))
        # updates the frames of the game
        pygame.display.update()
def inicializar_datos():
    puntuacion = 0
    text = small2_font.render('Puntuacion = ' + str(puntuacion), True, VERDE)
    textRect = text.get_rect()
    textRect.center = (100, 10)
    pantalla.blit(text, textRect)


if __name__ == "__main__":
    main()
