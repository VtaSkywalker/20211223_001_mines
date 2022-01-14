from stage import *
import pygame_menu
import pygame

class Display:
    """
        显示界面
    """
    def gameStage(self):
        """
            游戏图形界面
        """
        while True:
            events = pygame.event.get()
            for event in events:
                if(event.type == pygame.QUIT):
                    exit()
            pygame.display.update()

    def initForm(self):
        """
            初始化图形界面
        """
        pygame.init()
        gridSize = 30
        width = StageConfig.width * gridSize
        height = StageConfig.height * gridSize
        self.screen = pygame.display.set_mode((width, height))
        self.menu = pygame_menu.Menu("title", width, height)

    def mainLoop(self):
        """
            主循环
        """
        self.initForm()
        self.gameStage()
