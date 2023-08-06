
# -*- coding: utf-8 -*-
## @package som_cm.core.hist_3d
#
#  Implementation of 3D color histograms.
#  @author      tody
#  @date        2015/08/28

import numpy as np

from som_cm.core.color_pixels import ColorPixels
from som_cm.core.hist_common import *

class Hist3D:
    ## Constructor
    #  @param image          input image.
    #  @param num_bins       target number of histogram bins.
    #  @param alpha          low density clip.
    #  @param color_space    target color space. 'rgb' or 'Lab' or 'hsv'.
    # alpha这个阈值有待商榷。
    def __init__(self, image,
                 num_bins=16, alpha=0.1, color_space='rgb'):
        self._computeTargetPixels(image, color_space)

        self._num_bins = num_bins
        self._alpha = alpha
        self._color_space = color_space

        self._computeColorRange()
        self._computeHistogram()

        self._plotter = Hist3DPlot(self)

    ## Plot histogram with the given density size range.
    def plot(self, ax, density_size_range=[10, 100]):
        self._plotter.plot(ax, density_size_range)

    def colorSpace(self):
        return self._color_space

    #标示出了在3维数据中，值大于0的x,y,z轴的值
    def colorIDs(self):
        color_ids = np.where(self._histPositive())

        return color_ids

    def colorCoordinates(self):
        color_ids = self.colorIDs()
        num_bins = self._num_bins
        color_range = self._color_range
        return colorCoordinates(color_ids, num_bins, color_range)

    def colorCoordinates2(self):
        color_ids = self.colorIDs()
        num_bins = self._num_bins
        color_range = self._color_range
        return colorCoordinates2(color_ids, num_bins, color_range, self._pixels, self._old_colorId)

    def colorDensities(self):
        return colorDensities(self._hist_bins)

    def rgbColors(self):
        return rgbColors(self._hist_bins, self._color_bins)

    def colorRange(self):
        return self._color_range

    # 原来image是rgb的，经过ColorPixels，先除以255，然后转换成lab，会使得小数变成-127到128的数据，如下
    # 9.73089905e+01   2.20525265e+00  -1.92381144e+00
    def _computeTargetPixels(self, image, color_space):
        color_pixels = ColorPixels(image,num_pixels = 2000)
        # print color_pixels.pixels()
        self._pixels = color_pixels.pixels(color_space)

        # bl=self._pixels==[100,0,0]
        # bl=np.any(bl,axis=1)
        # ind=np.nonzero(bl)[0]
        # self._pixels = np.delete(self._pixels,ind,axis=0)

        self._rgb_pixels = color_pixels.rgb()


    # pixels的数据格式为二维数组，二维数组长为N（N=weight*height），3为（R G B）的形式。由weight * height控制换行。
    # [[ 0.75686282  0.58431375  0.59215689]
    # [ 0.78039223  0.65882355  0.65098041]
    # [ 0.56078434  0.54901963  0.54509807]
    # [ 0.76470596  0.59215689  0.56470591]
    # [ 0.82352948  0.67450982  0.63921571]
    #
    def _computeColorRange(self):
        pixels = self._pixels
        #shape[0] 行 shape[1]列
        cs = pixels.shape[1]

        c_min = np.zeros(cs)
        c_max = np.zeros(cs)
        for ci in range(cs):
            #pixels中的:表示任意行，ci表示ci列
            c_min[ci] = np.min(pixels[:, ci])
            c_max[ci] = np.max(pixels[:, ci])

        self._color_range = [c_min, c_max]

    def _computeHistogram(self):
        pixels = self._pixels
        num_bins = self._num_bins
        c_min, c_max = self._color_range

        hist_bins = np.zeros((num_bins, num_bins, num_bins), dtype=np.float32)
        color_bins = np.zeros((num_bins, num_bins, num_bins, 3), dtype=np.float32)

        color_ids = (num_bins - 1) * (pixels - c_min) / (c_max - c_min)
        color_ids = np.int32(color_ids)
        # 多维数组强制打印全部输出
        # np.set_printoptions(threshold=np.inf)
        # print(color_ids) ，如下
        # [[11 10 10]
        # [12 12 12]
        # [ 8  9  9]
        # [11 10  9]
        # [12 12 11]
        # [ 8 10  9]
        # [10  7  6]
        # print(self._rgb_pixels)

        for pi, color_id in enumerate(color_ids):
            hist_bins[color_id[0], color_id[1], color_id[2]] += 1
            # 用这个色彩还原技度应该更高
            color_bins[color_id[0], color_id[1], color_id[2]] += self._rgb_pixels[pi]

        self._hist_bins = hist_bins
        # print hist_bins 数据如下
        #[[[  3.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.
        #    0.   0.]
        # [  0.   1.   1.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.
        #    0.   0.]
        hist_positive = self._hist_bins > 0.0

        # print(hist_positive) 数据如下
        #[[[ True False False False False False False False False False False False
        # False False False False]
        # [False  True  True False False False False False False False False False
        #  False False False False]


        for ci in range(3):
            color_bins[hist_positive, ci] /= self._hist_bins[hist_positive]
      # print color_bins 记录了更具体的数据
      #   [[[ 0.12810458  0.15294118  0.18954249]
      #  [ 0.          0.          0.        ]
      #  [ 0.          0.          0.        ]
      #  [ 0.          0.          0.        ]
      #  [ 0.          0.          0.        ]
      #  [ 0.          0.          0.        ]
      #  [ 0.          0.          0.        ]
      #  [ 0.          0.          0.        ]
      #  [ 0.          0.          0.        ]
      #  [ 0.          0.          0.        ]
      #  [ 0.          0.          0.        ]
      #  [ 0.          0.          0.        ]
      #  [ 0.          0.          0.        ]
      #  [ 0.          0.          0.        ]
      #  [ 0.          0.          0.        ]
      #  [ 0.          0.          0.        ]]
      #
      # [[ 0.          0.          0.        ]
      #  [ 0.15294118  0.20392159  0.24313727]
      #  [ 0.13725491  0.19607845  0.28235295]
      #  [ 0.          0.          0.        ]

        self._color_bins = color_bins
        self._old_colorId = color_ids


        self._clipLowDensity()


    def _clipLowDensity(self):
        clipLowDensity(self._hist_bins, self._color_bins, self._alpha)

    #除去0的数据
    def _histPositive(self):
        return self._hist_bins > 0.0


## 3D color histogram plotter.
class Hist3DPlot:
    ## Constructor.
    #  @param hist3D histogram for plotting.
    def __init__(self, hist3D):
        self._hist3D = hist3D

    ## Plot histogram with the given density size range.
    def plot(self, ax, density_size_range=[10, 100]):
        color_samples = self._hist3D.colorCoordinates()
        density_sizes = self._densitySizes(density_size_range)
        colors = self._hist3D.rgbColors()

        ax.scatter(color_samples[:, 0], color_samples[:, 1], color_samples[:, 2], color=colors, s=density_sizes)
        self._axisSetting(ax)

    def _densitySizes(self, density_size_range):
        color_densities = self._hist3D.colorDensities()
        return densitySizes(color_densities, density_size_range)

    def _axisSetting(self, ax):
        color_space = self._hist3D.colorSpace()

        ax.set_xlabel(color_space[0])
        ax.set_ylabel(color_space[1])
        ax.set_zlabel(color_space[2])

        color_range = self._hist3D.colorRange()
        tick_range = np.array(color_range).T

        xticks, yticks, zticks = range2ticks(tick_range)

        ax.set_xticks(xticks)
        ax.set_yticks(yticks)
        ax.set_zticks(zticks)

        xlim, ylim, zlim = range2lims(tick_range)

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_zlim(zlim)
