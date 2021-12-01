from main import AZUL


def laberinto1():


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
               [450, 450, 20, 200, AZUL]  # 22
                ]

    return paredes


class Caldero(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/caldero/caldera.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.y = 450
        self.rect.x = 450
    def draw(self):
        pantalla.blit(self.image, self.rect)
