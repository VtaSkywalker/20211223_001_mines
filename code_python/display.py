from pygame import event
from stage import *
import pygame_menu
import pygame

class Display:
    """
        显示界面
    """

    def __init__(self):
        self.stage = Stage()

    def clickOperation(self, event, mousePos):
        """
            点击鼠标时触发事件
        """
        # 在点击grid的时候触发的事件
        j = mousePos[0] // self.gridSize
        i = mousePos[1] // self.gridSize
        # 游戏结束时不能继续操作
        if(not self.stage.isGameover()):
            # 左右同时：swamp
            if(pygame.mouse.get_pressed()[0] and pygame.mouse.get_pressed()[2]):
                self.stage.action(3, i, j)
            # 左击：翻grid
            elif(event.button == 1):
                self.stage.action(1, i, j)
            # 右击：flag
            elif(event.button == 3):
                self.stage.action(2, i, j)
            # 点完后，判断是否游戏胜利
            if(self.stage.isGamewin()):
                self.stage.gamewin()

    def gameStage(self):
        """
            游戏图形界面
        """
        while True:
            events = pygame.event.get()
            for event in events:
                if(event.type == pygame.QUIT):
                    exit()
                if(event.type == pygame.MOUSEBUTTONDOWN):
                    self.clickOperation(event, pygame.mouse.get_pos())
                if(event.type == pygame.KEYDOWN):
                    # 重开快捷键
                    if(pygame.key.get_pressed()[pygame.K_r]):
                        self.stage = Stage()
            self.gameStageDraw()
            pygame.display.update()

    def gameStageDraw(self):
        """
            对gameStage进行绘制
        """
        # 初始化-黑屏
        self.screen.fill((0,0,0))

        maskedGrid_img = pygame.image.load("./img/maskedGrid.png")
        maskedGrid_rect = maskedGrid_img.get_rect()
        unmaskedGrid_img = pygame.image.load("./img/unmaskedGrid.png")
        unmaskedGrid_rect = unmaskedGrid_img.get_rect()
        flag_img = pygame.image.load("./img/flag.png")
        flag_rect = flag_img.get_rect()
        mine_img = pygame.image.load("./img/mine.png")
        mine_rect = mine_img.get_rect()
        for i in range(StageConfig.height):
            for j in range(StageConfig.width):
                centerx = self.gridSize * (0.5 + j)
                centery = self.gridSize * (0.5 + i)
                # mask / unmask
                if(self.stage.maskField[i][j]):
                    maskedGrid_rect.centerx = centerx
                    maskedGrid_rect.centery = centery
                    self.screen.blit(maskedGrid_img, maskedGrid_rect)
                else:
                    unmaskedGrid_rect.centerx = centerx
                    unmaskedGrid_rect.centery = centery
                    self.screen.blit(unmaskedGrid_img, unmaskedGrid_rect)
                    # 1-9 / mine
                    if('1' <= self.stage.mineField[i][j] <= '9'):
                        number_img = pygame.image.load("./img/%s.png" % self.stage.mineField[i][j])
                        number_rect = number_img.get_rect()
                        number_img = pygame.transform.scale(number_img, (number_rect.size[0] * 0.6, number_rect.size[1] * 0.6))
                        number_rect = number_img.get_rect()
                        number_rect.centerx = centerx
                        number_rect.centery = centery
                        self.screen.blit(number_img, number_rect)
                # game over时显示所有地雷
                if(self.stage.isGameover() and self.stage.mineField[i][j] == '*'):
                    mine_rect.centerx = centerx
                    mine_rect.centery = centery
                    self.screen.blit(mine_img, mine_rect)
        # flag显示
        for eachFlagPoint in self.stage.flagContainer:
            flag_rect.centerx = self.gridSize * (0.5 + eachFlagPoint[1])
            flag_rect.centery = self.gridSize * (0.5 + eachFlagPoint[0])
            self.screen.blit(flag_img, flag_rect)
        # 剩余flag数显示
        flag_rect.centerx = 25
        flag_rect.centery = self.gridSize * self.stage.height + 25
        self.screen.blit(flag_img, flag_rect)
        font = pygame.font.SysFont("arial", 35)
        img = font.render('x %s' % str(self.stage.flagLimit - len(self.stage.flagContainer)), True, (255, 255, 255))
        rect = img.get_rect()
        rect.left = 50
        rect.centery = self.gridSize * self.stage.height + 25
        self.screen.blit(img, rect)
        # 鼠标所在处的那个grid高光
        mousePos = pygame.mouse.get_pos()
        j = mousePos[0] // self.gridSize
        i = mousePos[1] // self.gridSize
        if(0 <= j < self.stage.width and 0 <= i < self.stage.height):
            highLightGrid = pygame.Surface((50, 50))
            highLightGrid.set_alpha(128)
            highLightGrid.fill((255, 255, 255))
            self.screen.blit(highLightGrid, (j * self.gridSize, i * self.gridSize))
        # gameover / gamewin文字显示
        font = pygame.font.SysFont("arial", 35)
        if(self.stage.isGameover()):
            img = font.render('Game Over', True, (255, 0, 0))
            rect = img.get_rect()
            rect.centerx = self.width / 2
            rect.centery = self.gridSize * self.stage.height + 25
            self.screen.blit(img, rect)
        elif(self.stage.isGamewin()):
            img = font.render('Game Win', True, (0, 255, 0))
            rect = img.get_rect()
            rect.centerx = self.width / 2
            rect.centery = self.gridSize * self.stage.height + 25
            self.screen.blit(img, rect)

    def initForm(self):
        """
            初始化图形界面
        """
        pygame.init()
        self.gridSize = 50
        self.width = StageConfig.width * self.gridSize
        self.height = StageConfig.height * self.gridSize + 50
        self.screen = pygame.display.set_mode((self.width, self.height))

    def mainLoop(self):
        """
            主循环
        """
        self.initForm()
        self.gameStage()
