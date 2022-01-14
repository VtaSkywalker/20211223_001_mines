from stage import *
import pygame_menu
import pygame

class Display:
    """
        显示界面
    """

    def __init__(self):
        self.stage = Stage()

    def gameStage(self):
        """
            游戏图形界面
        """
        while True:
            events = pygame.event.get()
            for event in events:
                if(event.type == pygame.QUIT):
                    exit()
            self.gameStageDraw()
            pygame.display.update()

    def gameStageDraw(self):
        """
            对gameStage进行绘制
        """
        maskedGrid_img = pygame.image.load("./img/maskedGrid.png")
        maskedGrid_rect = maskedGrid_img.get_rect()
        unmaskedGrid_img = pygame.image.load("./img/unmaskedGrid.png")
        unmaskedGrid_rect = unmaskedGrid_img.get_rect()
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
