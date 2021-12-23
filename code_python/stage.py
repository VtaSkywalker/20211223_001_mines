import numpy as np

class StageConfig:
    height = 10
    width = 10
    mineNumber = 10

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

    def gameover(self):
        """
            游戏结束时执行
        """

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

    def isFlagReachMax(self):
        """
            检查Flag数是否达到上限
        """

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
