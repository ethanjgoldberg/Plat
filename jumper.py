import pygame, sys
from helpers import *

class Jumper(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('jumper.png',-1)
        self.x, self.y = (23000, 23000)
        self.fixrect()
        self.dx = 0
        self.dy = 0
        self.mm_ = 1000
        self.friction = .7
        self.airfriction = .99
        self.jump = -2600
        self.grounded = False
        self.keys = {K_UP: False,
                     K_LEFT: False,
                     K_RIGHT: False}
        self.score = 0

    def key(self, key, p):
        self.keys[key] = p

    def update(self, s):
        if not self.grounded:
            mm = self.mm_ * (.02)
        else: mm = self.mm_
        if self.keys[K_UP] and self.grounded:
            self.dy += self.jump
        if self.keys[K_LEFT]:
            self.dx -= mm
        if self.keys[K_RIGHT]:
            self.dx += mm
        self.dy += GRAV

        if self.grounded: self.dx = int(self.dx*self.friction)
        else: self.dx = int(self.dx*self.airfriction)
        self.grounded = False

        
        if self.dx != 0: self.move(self.dx,0, s)        
        if self.dy != 0: self.move(0,self.dy, s)
        
    def fixrect(self):
        self.rect.center = (round(self.x/1024), round(self.y/1024))
    def fixx(self):
        self.x = 1024*self.rect.center[0]
    def fixy(self):
        self.y = 1024*self.rect.center[1]
    def fixxy(self):
        self.fixx()
        self.fixy()
    def winner(self):
        print "WINNER with", self.score, "points."
    def loser(self):
        print "LOSER with", self.score, "points."
    
    def move(self, mx, my, m):
        s = m.sprites
        self.x += mx
        self.y += my
        self.fixrect()
        for re in pygame.sprite.spritecollide(self, s.wall_sprites, False):
            r = re.rect
            if my > 0:
                self.rect.bottom = r.top
                self.dy = 0
                self.grounded = True
                self.fixy()
            if my < 0:
                self.rect.top = r.bottom
                self.dy = 0
                self.fixy()
            if mx < 0:
                self.rect.left = r.right
                self.dx = 0
                self.fixx()
            if mx > 0:
                self.rect.right = r.left
                self.dx = 0
                self.fixx()
        if pygame.sprite.spritecollide(self, s.exit_sprites, False):
            self.winner()
            m.Restart()
        self.score += len(pygame.sprite.spritecollide(self, s.coin_sprites, True))
        if self.rect.bottom > TILESIZE * (TILESH + 1):
            self.loser()
            m.Restart()
