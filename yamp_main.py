import pygame
from random import randint, choice

# CONSTANTES

ANCHO = 460
ALTO = 600

NORTE = 0
SUR = 1
ESTE = 2
OESTE = 3


# CLASES


class Jugador:
    def __init__(self):
        self.RADIO = 20

        self.x = ANCHO // 2 - self.RADIO
        self.y = ALTO - self.RADIO

        self.vel = 0  # Eje Y únicamente

        self.hit = [0, 0, 0, 0]

        self.altura = 0

        self.fall = False

    def dibujar(self):
        pygame.draw.circle(ventana, (255, 0, 0), (self.x, self.y), self.RADIO)

    def gravedad(self):
        if self.hit[SUR]:
            self.vel = -25

        elif self.vel < 17:
            self.vel += 1

    def colision(self):
        # Reiniciando
        self.hit = [0, 0, 0, 0]

        # Suelo
        if self.y + self.RADIO <= ALTO <= self.y + self.RADIO + self.vel:
            if int(base.y) == 600:
                self.hit[SUR] = 1
                self.y = ALTO - self.RADIO
                self.vel = 0

            else:
                self.fall = True

        # Obstáculos
        for o in obstaculos:
            if self.x - self.RADIO - o.ANCHO <= o.x <= self.x + self.RADIO:
                if self.y + self.RADIO <= o.y <= self.y + self.RADIO + self.vel:
                    if o.activo:
                        self.hit[SUR] = 1
                        self.y = int(o.y // 1) - self.RADIO
                        self.vel = 0
                        if o.tipo == 2:
                            o.activo = False
                        if o.tipo == 3:
                            self.vel = -120
                    return

    def mejor(self):
        h = base.y - self.y
        if h > self.altura * 170:
            self.altura = round(h / 170)

    def reset(self):
        self.fall = False
        self.altura = 0
        self.hit = [0, 0, 0, 0]
        self.y = ALTO - self.RADIO - 10
        self.vel = 0


class Obstaculo:
    def __init__(self, x_relativa, y_relativa, tipo):
        self.ANCHO = 112
        self.ALTO = 30

        self.activo = True

        self.x = x_relativa * 112 + 2
        self.y = int((ALTO - 100) - y_relativa * 85)

        self.tipo = tipo
        self.is_base()

    def is_base(self):
        if self.tipo == 0:
            self.y = ALTO

    def dibujar(self):
        if self.tipo == 1:
            pygame.draw.rect(ventana, (0, 200, 11), (self.x, self.y, self.ANCHO, self.ALTO))
        elif self.tipo == 2:
            pygame.draw.rect(ventana, (255, 255, 255), (self.x, self.y, self.ANCHO, self.ALTO))
        elif self.tipo == 3:
            pygame.draw.rect(ventana, (255, 255, 0), (self.x, self.y, self.ANCHO, self.ALTO))


# FUNCIONES


def render():

    if j.altura < 500:
        rg = round(-0.34 * j.altura) + 170
        b = round(-0.51 * j.altura) + 255
    else:
        rg = b = 0
    ventana.fill((rg, rg, b))

    j.dibujar()

    for o in obstaculos:
        if o.activo:
            o.dibujar()

    # HUD
    puntuacion = fuente.render(f'Mejor Altura: {j.altura}m', 1, (255, 255, 255))
    ventana.blit(puntuacion, (ANCHO // 2 - 150, 10))


def mover():
    j.x = pygame.mouse.get_pos()[0]

    # Debajo de la mitad
    if j.y + j.vel > ALTO // 2 - 100:
        j.y += j.vel

    else:
        base.y -= j.vel

        for o in obstaculos:
            if o.y < ALTO:
                o.y -= j.vel


def init_nivel():
    nivel = []
    for i in obstaculos_raw:
        nivel.append(Obstaculo(i[0], i[1], i[2]))
    return nivel


def pausa_menu():
    pygame.draw.rect(ventana, (30, 80, 200), (ANCHO // 2 - 205, ALTO // 2 - 150, 400, 300))
    p = fuente.render('Juego en Pausa', 1, (255, 255, 255))
    ventana.blit(p, (ANCHO // 2 - 120, ALTO // 2 - 145))


    #p.draw.rect(ventana, )
    pygame.display.update()

# MAIN


def main():
    global ventana, j, obstaculos, obstaculos_raw, base, fuente

    # INICIALIZAR VENTANA
    pygame.init()
    pygame.display.set_caption('Yamp inde espeis')
    ventana = pygame.display.set_mode((450, 600))
    clock = pygame.time.Clock()

    # INICIALIZAR VARIABLES
    j = Jugador()

    # Nivel
    base = Obstaculo(0, 0, 0)
    obstaculos_raw = [(0, 0, 1)]

    registro = []
    for i in range(1, 800):
        h = randint(0, 10)
        obstaculos_raw.append((h, i, choice((1, 1, 1, 1, 2, 2, 3))))

        registro.append(h)
        if len(registro) == 2:
            if registro[0] > 3 and registro[1] > 3:
                obstaculos_raw.append((randint(1, 3), i, choice((1, 1, 2))))
            registro = []

    obstaculos = init_nivel()

    # Texto
    fuente = pygame.font.SysFont('comicsansms', 30)

    # MAINLOOP

    run = True
    pausa = False

    while run:
        
        # EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Poner/Sacar pausa
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    if pausa:
                        pausa = False
                    else:
                        pausa = True

        # PAUSA
        if pausa:
            pausa_menu()
            continue

        # Reset Level
        if j.fall:
            obstaculos = init_nivel()
            base = Obstaculo(0, 0, 0)
            pygame.time.delay(1500)
            j.reset()
            continue

        # UPDATE
        clock.tick(60)
        j.colision()
        mover()
        render()
        j.gravedad()
        j.mejor()
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
