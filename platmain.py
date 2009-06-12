import pygame, sys
from helpers import *
import jumper
import tiles

class PlatMain:
    def __init__(self, width=TILESIZE*TILESW,height=TILESIZE*TILESH):
        pygame.init()
        self.width = width
        self.height = height
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        self.sprites = AllSprites()
        self.LoadJumpman()

        
        self.background = pygame.Surface((TILESIZE*TILESW, TILESIZE*TILESH)).convert()
        self.background.fill((200,200,200))
        self.coin_surface = pygame.Surface((TILESIZE*TILESW, TILESIZE*TILESH)).convert()
        self.coin_surface.set_colorkey((255,0,255))
        self.coin_surface.fill((255,0,255))
        
        self.sprites.wall_sprites.draw(self.background)
        self.sprites.exit_sprites.draw(self.background)
        self.sprites.coin_sprites.draw(self.coin_surface)

    def MainLoop(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN or event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        sys.exit()
                    p = event.type == KEYDOWN
                    if ((event.key == K_RIGHT)
                    or (event.key == K_LEFT)
                    or (event.key == K_UP)
                    or (event.key == K_DOWN)):
                        self.jumpman.key(event.key, p)
            self.jumpman.update(self)
            self.screen.blit(self.background, (0,0))
            self.coin_surface.fill((255,0,255))
            self.sprites.coin_sprites.draw(self.coin_surface)
            self.screen.blit(self.coin_surface, (0,0))
            self.jumpman_sprites.draw(self.screen)
            
            pygame.display.flip()
            clock.tick(60)

    def LoadJumpman(self):
        self.jumpman = jumper.Jumper()
        self.jumpman_sprites = pygame.sprite.RenderUpdates((self.jumpman))
        self.jumpman.rect.center = self.sprites.jumpman_start
        self.jumpman.fixxy()
    
    def Restart(self):
        self.sprites.Reload()
        self.LoadJumpman()
        self.MainLoop()

class AllSprites:
    def __init__(self):
        self.LoadSprites()
        self.LoadTiles()
        
    def LoadSprites(self):
        self.wall_sprites = pygame.sprite.Group()
        self.exit_sprites = pygame.sprite.Group()
        self.coin_sprites = pygame.sprite.RenderUpdates()

    def LoadTiles(self):        
        items = {'#': (tiles.Wall, self.wall_sprites.add),
                 'O': (tiles.Coin, self.coin_sprites.add),
                 'E': (tiles.Exit, self.exit_sprites.add)}
        walldata = ["##############.%.#######################",
                    "#............................OO.......O#",
                    "#.....O........#......#...#......#.....#",
                    "#..................#................#..#",
                    "#.......................#.......#......#",
                    "#.....#............#..#.....#..........#",
                    "#..............#...#...................#",
                    "#.#.......#........#.........#..#..#...#",
                    "#...............OO.#............E#.....#",
                    "#######################.......##########"]
        for x in range(TILESW):
            for y in range(TILESH):
                k = walldata[y][x]
                if k == '%':
                    self.jumpman_start = (x*TILESIZE + HALFTILE, y*TILESIZE + HALFTILE)
                if k in items:
                    n = items[k][0](x*TILESIZE + HALFTILE, y*TILESIZE + HALFTILE)
                    items[k][1](n)

    def Reload(self):
        self.LoadSprites()
        self.LoadTiles()