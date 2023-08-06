# -*- coding: utf-8 -*-
## @package som_cm.som_cm
#
#  Implementation of SOM.
#  @author      tody
#  @date        2015/08/14

import os
import numpy as np
import matplotlib.pyplot as plt

from som_cm.np.norm import normVectors
from som_cm.cv.image import to32F, rgb2gray
from scipy import spatial
import cv2


## SOM parameter.
class SOMParam:
    #  @param h           image grid size.
    #  @param L0          initial parameter for learning restraint.  0.16
    #  @param lmbd        iteration limit.
    #  @param dimensoin   target dimension for SOM.
    def __init__(self, h=32, L0=0.16, lmbd=0.6, sigma0=0.3, dimension=2):
        self.h = h
        self.L0 = L0
        self.lmbd = lmbd
        self.sigma0 = sigma0
        self.dimension = dimension


## Implementation of SOM.
#
#  SOM with numpy functions.
#  - Compute nodes as n x 3 vector.
#  - Avoid the loops for x and y.
#  - xy coordinates are cached as n x 2 vector.
class SOM:
    ## Constructor
    #  @param samples  training samples.
    #  @param param    SOM parameter.
    def __init__(self, samples, param=SOMParam()):
        self._h = param.h
        self._dimension = param.dimension
        self._samples = samples
        # print samples
        self._L0 = param.L0

        self._nodes = self._initialNode(param.h, param.dimension)
        # print  self._nodes

        num_samples = self.numSamples()
        self._lmbd = param.lmbd * num_samples

        self._sigma0 = param.sigma0 * param.h

        self._computePositions(param.h, param.dimension)

        self._t = 0

    ## Return the number of training samples.
    def numSamples(self):
        return len(self._samples)

    ## Return the current node image.
    def nodeImage(self):
        if self._dimension == 1:
            return self._nodeImage1D()
        else:
            return self._nodeImage2D()

    # 新增加
    def nodeOriginData(self):
        if self._dimension == 1:
            return self._nodeOriginData()

    ## Return the current time step t.
    def currentStep(self):
        return self._t

    ## Return if the training is finished.
    def finished(self):
        return self._t == self.numSamples()

    ## Process all training process.
    def trainAll(self):
        while self._t < len(self._samples):
            self._train(self._t)
            self._t += 1


        # # # h
        # while self._t < len(self._samples) * 2:
        #     self._train(self._t)
        #     self._t += 1
        #
        # while self._t < len(self._samples)*3:
        #     self._train(self._t)
        #     self._t += 1

        # while self._t < len(self._samples) * 4:
        #     self._train(self._t)
        #     self._t += 1
        #
        # while self._t < len(self._samples)*5:
        #     self._train(self._t)
        #     self._t += 1
        # while self._t < len(self._samples) *6:
        #     self._train(self._t)
        #     self._t += 1
        #
        # while self._t < len(self._samples)*7:
        #     self._train(self._t)
        #     self._t += 1
        #
        # while self._t < len(self._samples)*4:
        #     self._train(self._t)
        #     self._t += 1

    ## Process training step t to t+1.
    def trainStep(self):
        if self._t < len(self._samples):
            self._train(self._t)
            self._t += 1

    # 下面代码写错位置了

    # 原来这个函数没有下面的两端代码，不过根据SOM聚类方法，需要多几次迭代，当变化率够小时，方才停止。所以多了两次循环。
    # 同时，这里多循环两次，其实可以用作者在single_image的68行那样，直接采用随机数组的方式来，加快聚类，效果是相当的
        self._t = 0
        if self._t < len(self._samples):
            self._train(self._t)
            self._t += 1

        self._t = 0
        if self._t < len(self._samples):
            self._train(self._t)
            self._t += 1




    def _nodeImage1D(self):
        h = 10
        w = self._h
        node_image = np.zeros((h, w, 3))
        for y in range(h):
            node_image[y, :, :] = self._nodes[:, :]
        return node_image

    # 返回数据，为了灰度化
    def _nodeOriginData(self):
        return self._nodes

    def _nodeImage2D(self):
        return self._nodes.reshape(self._h, self._h, 3)

    ## Initial node.
    def _initialNode(self, h, dimension):
        if dimension == 1:
            return self._initialNode1D(h)
        else:
            return self._initialNode2D(h)

    def _initialNode1D(self, h):
        #十行三列的二维数组
        return np.random.rand(h, 3)

    def _initialNode2D(self, h):
        return np.random.rand(h, h, 3).reshape(-1, 3)

    ## Compute position.
    def _computePositions(self, h, dimension):
        if dimension == 1:
            self._computePositions1D(h)
        else:
            self._computePositions2D(h)

    def _computePositions1D(self, h):
        x = np.arange(h)
        self._positions = x

    def _computePositions2D(self, h):
        x = np.arange(h)
        y = np.arange(h)
        xs, ys = np.meshgrid(x, y)
        xs = xs.flatten()
        ys = ys.flatten()
        self._positions = np.array([xs, ys]).T

    ## Train process.
    def _train(self, t):
        sample = self._samples[t % len(self._samples)]
        # print sample
        # bmu
        bmu_id = self._bmu(sample)
        bmu_position = self._positions[bmu_id]
        #在一维度情况下 bmu_id 和 bmu_position相等

        # update weight
        D = normVectors(self._positions - bmu_position)
        # L是一个从0.16逐渐减小的数值
        L = self._learningRestraint(t)
        # T是一个根据D计算出来的影响范围
        T = self._neighborhoodFunction(t, D)

        # update nodes
        # print self._nodes
        for ci in range(3):
            self._nodes[:, ci] += L * T * (sample[ci] - self._nodes[:, ci])
        # print self._nodes

    ## BMU: best matching unit.
    #  Return the unit of minimum distance from the sample.
    def _bmu(self, sample):
        norms = normVectors(self._nodes - sample)
        bmu_id = np.argmin(norms)
        return bmu_id

    ## Neighborhood function: exp (-D^2 / 2 sigma^2)
    def _neighborhoodFunction(self, t, D):
        sigma = self._sigma0 * np.exp(-t / self._lmbd)
        Theta = np.exp(-D ** 2 / (2 * sigma ** 2))
        return Theta

    ## Learning restraint: L0 exp (-t / lambda)
    def _learningRestraint(self, t):
        return self._L0 * np.exp(-t / self._lmbd) * 1


## Plotting class with matplot.
class SOMPlot:
    ## Constructor
    #  @param samples training samples.
    #  @param param    SOM parameter.
    def __init__(self, som):
        self._som = som
        self._node_image = None
        self._plot3d = None
        self._step_text = None

    ## Return the updated image.
    def updateImage(self):
        node_image = self._som.nodeImage()
        if self._node_image is None:
            self._node_image = plt.imshow(node_image)

        else:
            self._node_image.set_array(node_image)

        return self._node_image

    ## Return the current step status.
    def updateStepText(self):
        if self._step_text is None:
            self._step_text = plt.text(1, 1, '', fontsize=15)

        else:
            if self._som.finished():
                self._step_text.set_text('')
            else:
                self._step_text.set_text('step: %s' % self._som.currentStep())

        return self._step_text

    ## Plot color manifold in 3D.
    def plot3D(self, ax):
        node_image = self._som.nodeImage()
        colors = node_image.reshape(-1, 3)
        plot3d = ax.scatter(colors[:, 0], colors[:, 1], colors[:, 2],
                    color=colors, s = 3)

        # ax.set_xlabel('R', x=10, y=10)
        # ax.set_ylabel('G')
        # ax.set_zlabel('B')

        #坐标轴范围
        ax.set_zlim3d([0, 1])
        ax.set_ylim3d([-0, 1])
        ax.set_xlim3d([-0, 1])

        #所要显示的标度
        ax.set_xticks(np.linspace(0.0, 1.0, 3))
        ax.set_yticks(np.linspace(0.0, 1.0, 3))
        ax.set_zticks(np.linspace(0.0, 1.0, 3))
        return plot3d

    ## Animation function for FuncAnimation.
    def trainAnimation(self, *args):
        image = self.updateImage()
        text = self.updateStepText()

        self._som.trainStep()

        return [image, text]


    ## 显示点云图像 manifold in 3D.
    def plotCloud(self, ax, color_pixels):
        colors = color_pixels.reshape(-1, 3)
        plot3d = ax.scatter(colors[:, 0], colors[:, 1], colors[:, 2],
                    color=np.float32(colors), s = 10)

        # ax.set_xlabel('R', x=10, y=10)
        # ax.set_ylabel('G')
        # ax.set_zlabel('B')

        #坐标轴范围
        # ax.set_zlim3d([-0.05, 1.05])
        # ax.set_ylim3d([-0.05, 1.05])
        # ax.set_xlim3d([-0.05, 1.05])
        ax.set_zlim3d([0, 1])
        ax.set_ylim3d([-0, 1])
        ax.set_xlim3d([-0, 1])

        # 所要显示的标度
        ax.set_xticks(np.linspace(0.0, 1.0, 3))
        ax.set_yticks(np.linspace(0.0, 1.0, 3))
        ax.set_zticks(np.linspace(0.0, 1.0, 3))
        return plot3d

    def showGrayImage(self, image):
        # nodeOriginData = self._som.nodeOriginData()
        node_image = self._som.nodeImage()


        #只需要一行，因为有很多行一样的
        nodeOriginData = cv2.cvtColor(np.float32(node_image), cv2.COLOR_LAB2RGB)[0, :, :]
        print(nodeOriginData)
        # from sklearn import manifold
        # mds = manifold.MDS(n_components=1)
        # Xtrans = mds.fit_transform(nodeOriginData.astype(np.float64))
        # print Xtrans

        image = to32F(image)
        gray = rgb2gray(image)
        lmin = np.min(gray)
        lmax = np.max(gray)

        print(image.shape)
        print(image.dtype)

        h = image.shape[0]
        w = image.shape[1]
        node_image = np.zeros((h, w), dtype=image.dtype)


        for i in range(h):
            for j in range(w):
                smallestValue = 1 << 31
                smallestIndex = 0
                for k in range(len(nodeOriginData)):
                    # node_image[i, j] = 0.3 * image[i, j][0] + 0.59 * image[i, j][1] + 0.11 * image[i, j][2]
                    temp = self.distance(image[i, j], nodeOriginData[k])
                    # if i == 100 and j == 100:
                    #     print str(image[i, j]) + ':' + str(nodeOriginData[k]) + ":" + str(temp)
                    if smallestValue > temp:
                        smallestValue = temp
                        smallestIndex = k

                # print smallestIndex
                node_image[i, j] =  1 - (float(smallestIndex) / len(nodeOriginData) * (lmax - lmin) + lmin)


        # temp = rgb2gray(image)
        # import cv2
        # cv2.imshow('gray_image',temp)
        #
        # cv2.waitKey(0)

        return node_image


    def distance(self, tuple1, tuple2):
        # return (tuple1[0] - tuple2[0]) * (tuple1[0] - tuple2[0]) + (tuple1[1] - tuple2[1]) * (tuple1[1] - tuple2[1]) + (tuple1[2] - tuple2[2]) * (tuple1[2] - tuple2[2])
        return abs(tuple1[0] - tuple2[0])+ abs(tuple1[1] - tuple2[1]) + abs(tuple1[2] - tuple2[2])

    def showGrayImage2(self, image, fold = None):
        # fold = self._som.nodeImage()[0, :, :]
        from som_cm.cv.image import to32F, rgb2Lab, rgb2hsv, gray2rgb
        image = to32F(image)
        image = rgb2Lab(image)
        if fold == None:
            fold = self._som.nodeImage()
            fold = to32F(fold * 255)
            fold = rgb2Lab(fold)
        X = fold.reshape((-1, 3))
        X = np.float32(X)


        h = image.shape[0]
        w = image.shape[1]
        node_image = np.zeros((h, w), dtype=np.float)
        node_image2 = np.zeros((h, w), dtype=np.float)

        from sklearn import manifold
        n_com = 30
        mds = manifold.Isomap(n_components=n_com)
        Xtrans = mds.fit_transform(X)

        import time
        before = time.time()

        # 重新设置距离矩阵 ----
        mds.dist_matrix_ = mds.dist_matrix_ ** 1.4
        G = mds.dist_matrix_ ** 2
        G *= -0.5
        Xtrans = mds.kernel_pca_.fit_transform(G)
        #----
        # 距离矩阵的列向量的均值
        MeanLc = []
        for row in range(len(mds.dist_matrix_[0])):
            MeanLc.append(np.mean(mds.dist_matrix_[row,:]))
        MeanLc = np.array(MeanLc)


        #预计算特征向量除以特征值的根号
        #  n_com等于1就不循环了
        # for i in range(n_com):
        import math
        coleighVector = [mds.kernel_pca_.alphas_[:, 0] / math.sqrt(mds.kernel_pca_.lambdas_[0]) * -0.5]
        # print '--------------'
        # print X
        # print '--------------'
        # print Xtrans
        min_my = 1 << 31
        max_my = -1 << 31
        Cdistance = np.empty(len(mds.dist_matrix_))
        kdTree = spatial.cKDTree(X)

        dict = {}
        for i in range(h):
            for j in range(w):
                Cx = image[i][j][0]
                Cy = image[i][j][1]
                Cz = image[i][j][2]

                # 查找缓存
                val = dict.get(tuple(image[i,j]), None)
                if val != None:
                    node_image[i,j] = val
                    continue

                # 点到其他landmark 的距离
                k = 3
                distance,index = kdTree.query([Cx,Cy,Cz], k=k)

                # for col in range(len(mds.dist_matrix_)):
                #     smallestV = mds.dist_matrix_[index[0], col] + distance[0]
                #     for kindex in range(k-1):
                #         if smallestV > mds.dist_matrix_[index[kindex+1], col] + distance[kindex+1]:
                #             smallestV = mds.dist_matrix_[index[kindex+1], col] + distance[kindex+1]
                #     Cdistance.append(smallestV ** 2)
                #     print col


                # 最初版本，根据最近的点计算, 不加+ distance
                # Cdistance = (mds.dist_matrix_[index,:] + distance) ** 2

                CdistanceAll = np.array((mds.dist_matrix_[index[0],:] + distance[0]))
                for kIndex in range(1, k):
                    CdistanceAll = np.vstack((CdistanceAll, mds.dist_matrix_[index[kIndex],:] + distance[kIndex]))

                Cdistance = CdistanceAll.min(axis=0)
                Cdistance = Cdistance ** 2

                theta = Cdistance - MeanLc
                theta = np.asmatrix(theta)
                # print theta
                node_image[i,j] = (np.asmatrix(coleighVector) * theta.T)[0,0]
                dict[tuple(image[i,j])] = node_image[i,j]

                if node_image[i,j] < min_my:
                    min_my = node_image[i,j]
                if node_image[i,j] > max_my:
                    max_my = node_image[i,j]


        print('cost time :' + str(time.time() - before))

        for i in range(h):
            for j in range(w):
                node_image[i, j] =  (node_image[i, j] - min_my) / float((max_my - min_my))
                node_image2[i,j] = 1 - node_image[i, j]


        return node_image, node_image2


    def findmin(self, a, b, c):
        return min(a,b,c)
