import numpy as np
import sys

class StageConfig:
    height = 10
    width = 10
    mineNumber = 10
    doFirstFlip = False

class Stage:
    """
        场景类

        Attributes
        ----------
        height : int
            雷区的高度
        width : int
            雷区的宽度
        mineNumber : int
            雷的数量
        mineField : char[][]
            雷区
        maskField : bool[][]
            雷区的Mask，True为挡住
        flagContainer : int[2][]
            雷区的flag，存储了哪些地方插旗的信息
        flagLimit : int
            插旗的上限
        currentFlagNumber : int
            当前插旗的数量
    """
    def __init__(self):
        self.height = StageConfig.height
        self.width = StageConfig.width
        self.mineNumber = StageConfig.mineNumber
        self.initStage()

    def initStage(self):
        """
            初始化游戏
        """
        if(not self.isMineNumberLegal()):
            raise Exception("雷的数量不合理！")
        self.generateField()
        self.generateMine()
        self.generateMarkNumber()
        self.generateMaskField()
        self.initFlagInfo()
        if(StageConfig.doFirstFlip):
            safeIdx = np.where(self.mineField != '*')
            randomSelectIdx = int(np.random.rand() * len(safeIdx[0]))
            self.flipGrid(safeIdx[0][randomSelectIdx], safeIdx[1][randomSelectIdx])
        self.gameoverState = False

    def isMineNumberLegal(self):
        """
            雷的数量是否合理

            Returns
            -------
            合理 / 不合理 : True / False
        """
        if(self.width * self.height <= self.mineNumber):
            return False
        if(self.mineNumber <= 0):
            return False
        return True

    def generateField(self):
        """
            初始化二维数组
        """
        self.mineField = np.zeros(shape=(self.height, self.width), dtype=str)

    def generateMine(self):
        """
            生成地雷
        """
        indexList = list(np.arange(self.width * self.height, dtype=int))
        mineList = []
        for mineID in range(self.mineNumber):
            thisMineIdx = indexList[int(np.random.rand() * len(indexList))]
            mineList.append(thisMineIdx)
            indexList.remove(thisMineIdx)
        for eachMinePosIdx in mineList:
            i = eachMinePosIdx // self.width
            j = eachMinePosIdx % self.width
            self.mineField[i][j] = '*'

    def generateMarkNumber(self):
        """
            生成数字标记
        """
        for i in range(self.height):
            for j in range(self.width):
                if(self.mineField[i][j] == '*'):
                    continue
                number = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if((di == 0 and dj == 0) or (not (0 <= i + di < self.height)) or (not (0 <= j + dj < self.width))):
                            continue
                        if(self.mineField[i+di][j+dj] == '*'):
                            number += 1
                self.mineField[i][j] = str(number)

    def generateMaskField(self):
        """
            生成Mask数组
        """
        self.maskField = np.ones(shape=(self.height, self.width), dtype=bool)
    
    def initFlagInfo(self):
        """
            初始化Flag信息，包括容器和flag数
        """
        self.flagContainer = []
        self.flagLimit = self.mineNumber
        self.currentFlagNumber = 0

    def flipGrid(self, i, j):
        """
            翻开位于i行j列处的方块，如果踩雷则游戏结束，否则更新相应的状态后继续游戏

            Parameters
            ----------
            i : int
                i行
            j : int
                j列
        """
        if(not self.isMasked(i, j)): # 已经被点过的话，当然就不点了
            return
        if([i, j] in self.flagContainer): # 插了flag的不能点
            return
        if(self.mineField[i][j] == '*'): # 踩雷，di了！
            self.gameover()
        self.updateMask(i, j)

    def isGameover(self):
        if(self.gameoverState):
            return True
        return False

    def gameover(self):
        """
            游戏结束时执行
        """
        self.gameoverState = True
        print("gameover")

    def updateMask(self, i, j):
        """
            根据点击的位置，更新Mask的情况

            Parameters
            ----------
            i : int
                i行
            j : int
                j列
        """
        # 使用队列的方法，判断该解除哪一块的mask
        queue = [[i, j]]
        while(queue):
            p = queue[0]
            queue.remove(queue[0])
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    i = p[0]
                    j = p[1]
                    if((di == 0 and dj == 0) or (not (0 <= i + di < self.height)) or (not (0 <= j + dj < self.width))):
                        continue
                    if(di and dj):
                        continue
                    if(self.maskField[i+di, j+dj]):
                        if(self.mineField[i, j] not in ['0', '*'] and self.mineField[i+di, j+dj] == '0'):
                            queue.append([i+di, j+dj])
                        if(self.mineField[i, j] == '0' and self.mineField[i+di, j+dj] not in ['*']):
                            queue.append([i+di, j+dj])
            # 如果上面本来有flag，则拔掉
            if([i, j] in self.flagContainer):
                self.flagGrid(i, j)
            self.maskField[i, j] = False

    def isMasked(self, i, j):
        """
            检查i行j列是否被Mask

            Parameters
            ----------
            i : int
                i行
            j : int
                j列            
        """
        if(self.maskField[i][j]):
            return True
        return False

    def flagGrid(self, i, j):
        """
            右键点击i行j列的grid时执行，综合判断flag操作

            Parameters
            ----------
            i : int
                i行
            j : int
                j列 
        """
        if(not self.maskField[i][j]): # 如果已经被点开了，自然不能插旗
            return
        self.updateFlag(i, j)

    def isFlagReachMax(self):
        """
            检查Flag数是否达到上限
        """
        if(self.currentFlagNumber >= self.flagLimit):
            return True
        return False

    def updateFlag(self, i, j):
        """
            对i行j列进行Flag操作

            Parameters
            ----------
            i : int
                i行
            j : int
                j列 
        """
        if([i, j] in self.flagContainer):
            self.flagContainer.remove([i, j])
            self.currentFlagNumber -= 1
        else:
            if(not self.isFlagReachMax()):
                self.flagContainer.append([i, j])
                self.currentFlagNumber += 1

    def cmdShow(self):
        """
            在cmd中打印当前状态
        """
        print("X\t", end="")
        for j in range(self.width):
            print("\033[33m%s\033[0m\t" % j, end="")
        print("")
        for i in range(self.height):
            print("\033[33m%s\033[0m\t" % i, end="")
            for j in range(self.width):
                if(self.maskField[i][j]):
                    if([i, j] in self.flagContainer):
                        print("F\t", end="")
                    else:
                        print(".\t", end="")
                else:
                    print("%s\t" % self.mineField[i][j], end="")
            print("")

    def swampGrid(self, i, j):
        """
            对着i, j的四周一圈扫雷

            Parameters
            ----------
            i : int
                i行
            j : int
                j列 
        """
        # 如果扫的是mask区，则直接跳过
        if(self.maskField[i][j]):
            return
        # 如果检查到flag下面没有雷（或有雷却没被flag），则不翻开
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if((di == 0 and dj == 0) or (not (0 <= i + di < self.height)) or (not (0 <= j + dj < self.width))):
                    continue
                if([i+di, j+dj] in self.flagContainer and self.mineField[i+di][j+dj] != "*"):
                    return
                if([i+di, j+dj] not in self.flagContainer and self.mineField[i+di][j+dj] == "*"):
                    # 如果有雷没有flag，并且已经flag用完了，则直接点击爆炸
                    if(self.isFlagReachMax()):
                        self.flipGrid(i+di, j+dj)
                    return
        # 扫雷成功后，翻开周围一圈的地盘
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if((di == 0 and dj == 0) or (not (0 <= i + di < self.height)) or (not (0 <= j + dj < self.width))):
                    continue
                if(self.maskField[i+di][j+dj] and [i+di, j+dj] not in self.flagContainer):
                    self.flipGrid(i+di, j+dj)

    def isGamewin(self):
        """
            判断是否游戏胜利
        """
        if(sum(sum(self.maskField)) == self.mineNumber):
            return True
        return False

    def gamewin(self):
        """
            游戏胜利
        """
        for i in range(self.height):
            for j in range(self.width):
                if(self.maskField[i][j] and [i, j] not in self.flagContainer):
                    self.flagContainer.append([i, j])
        print("game win!")

    def action(self, signal, i, j):
        """
            采取动作，与图像界面直接连接
            信号1:翻雷
            信号2:flag
            信号3:扫雷

            Parameters
            ----------
            signal : int
                信号
            i : int
                第i行
            j : int
                第j列
        """
        if(signal == 1):
            self.flipGrid(i, j)
        elif(signal == 2):
            self.flagGrid(i, j)
        elif(signal == 3):
            self.swampGrid(i, j)
