
import pygame

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
VIOLETA = (255, 0, 255)


class Pared(pygame.sprite.Sprite):

    def __init__(self, x, y, largo, alto, color):#Funcion contructora de una pared de 4 lados

        super().__init__()

        self.image = pygame.Surface([largo, alto])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Protagonista(pygame.sprite.Sprite):#Funcion constructora del cuadrado con movimiento

    # Velocidades iniciales
    cambio_x = 0
    cambio_y = 0

    def __init__(self, x, y):

        super().__init__()

        self.image = pygame.Surface([15, 15])#Creamos un cuadrado que sera el prota
        self.image.fill(BLANCO)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def cambiovelocidad(self, x, y): #Cambia de velocidad con pulsar el teclado
        self.cambio_x += x
        self.cambio_y += y

    def mover(self, paredes):
        #desplazamiento Horizontal
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
        paredes = [[0, 0, 20, 250, BLANCO],
                   [0, 350, 20, 250, BLANCO],
                   [780, 0, 20, 250, BLANCO],
                   [780, 350, 20, 250, BLANCO],
                   [20, 0, 760, 20, BLANCO],
                   [20, 580, 760, 20, BLANCO],
                   [100, 80, 20, 500, AZUL],
                   [150, 20, 20, 500, AZUL],
                   [200, 80, 20, 500, AZUL],
                   [250, 20, 20, 500, AZUL],
                   [300, 80, 20, 500, AZUL],
                   [100, 80, 500, 20, AZUL]]


        # Iteramos a través de la lista. Creamos la pared y la añadimos a la lista.
        for item in paredes:
            pared = Pared(item[0], item[1], item[2], item[3], item[4])
            self.pared_lista.add(pared)


class Cuarto2(Cuarto):
    """Esto crea todas las paredes del cuarto 2"""

    def __init__(self):
        super().__init__()

        paredes = [[0, 0, 20, 250, ROJO],
                   [0, 350, 20, 250, ROJO],
                   [780, 0, 20, 250, ROJO],
                   [780, 350, 20, 250, ROJO],
                   [20, 0, 760, 20, ROJO],
                   [20, 580, 760, 20, ROJO],
                   [190, 50, 20, 500, VERDE],
                   [590, 50, 20, 500, VERDE]
                   ]

        for item in paredes:
            pared = Pared(item[0], item[1], item[2], item[3], item[4])
            self.pared_lista.add(pared)



class Cuarto3(Cuarto):

    def __init__(self):
        super().__init__()
        #El ancho de las rayas es 20
        paredes = [[0, 0, 20, 255, VIOLETA],#raya de arriba izquierda
                   [0, 350, 20, 250, VIOLETA],#raya de abajo izquierda
                   [780, 0, 20, 250, VIOLETA],#raya de arriba derecha
                   [780, 350, 20, 250, VIOLETA],#raya de abajo derecha
                   [20, 0, 760, 20, VIOLETA],#Raya de arriba de la pantalla
                   [20, 580, 760, 20, VIOLETA]#Raya de abajo de la pantalla
                   ]
        #x, y, largo, alto
        for item in paredes:
            pared = Pared(item[0], item[1], item[2], item[3], item[4])
            self.pared_lista.add(pared)

        for x in range(100, 800, 100):
            for y in range(35, 451, 300):
                pared = Pared(x, y, 20, 230, ROJO)
                self.pared_lista.add(pared)

        for x in range(150, 700, 100):
            pared = Pared(x, 200, 20, 230, BLANCO)
            self.pared_lista.add(pared)


def main():
    pygame.init()

    pantalla = pygame.display.set_mode([800, 600])


    pygame.display.set_caption('Laberinto Principal')

    protagonista = Protagonista(50, 50) #Creamos un protagonista

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

    reloj = pygame.time.Clock()

    puntuacion = 0

    hecho = False

    while not hecho:

        # --- Procesamiento de Eventos ---

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
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

        if protagonista.rect.x < -15:
            if cuarto_actual_no == 0:
                cuarto_actual_no = 2
                cuarto_actual = cuartos[cuarto_actual_no]
                protagonista.rect.x = 790
            elif cuarto_actual_no == 2:
                cuarto_actual_no = 1
                cuarto_actual = cuartos[cuarto_actual_no]
                protagonista.rect.x = 790
            else:
                cuarto_actual_no = 0
                cuarto_actual = cuartos[cuarto_actual_no]
                protagonista.rect.x = 790

        if protagonista.rect.x > 801:
            if cuarto_actual_no == 0:
                cuarto_actual_no = 1
                cuarto_actual = cuartos[cuarto_actual_no]
                protagonista.rect.x = 0
            elif cuarto_actual_no == 1:
                cuarto_actual_no = 2
                cuarto_actual = cuartos[cuarto_actual_no]
                protagonista.rect.x = 0
            else:
                cuarto_actual_no = 0
                cuarto_actual = cuartos[cuarto_actual_no]
                protagonista.rect.x = 0

        # --- Dibujamos ---
        pantalla.fill(NEGRO)

        desplazarsprites.draw(pantalla)
        cuarto_actual.pared_lista.draw(pantalla)

        pygame.display.flip()

        reloj.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
