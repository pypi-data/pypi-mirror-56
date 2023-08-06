# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
from som_cm.core.color_pixels import ColorPixels
from mpl_toolkits.mplot3d import Axes3D

from som_cm.io_util.image import loadRGB
from som_cm.core.hist_3d import Hist3D
from som_cm.core.som import SOMParam, SOM, SOMPlot

class SOMGraySclae:
    def get_gray_scal(self, image_file):
        image = loadRGB(image_file)
        som1D, som2D = self.setupSOM(image)
        print("  - Train 2D")
        som2D.trainAll()
        som2D_plot = SOMPlot(som2D)
        gray, gray_reverse = som2D_plot.showGrayImage2(image)
        return gray, gray_reverse

    def get_1d_manifold(self, image_file):
        image = loadRGB(image_file)
        som1D, som2D = self.setupSOM(image)

        print("  - Train 1D")
        som1D.trainAll()

        return som1D.nodeImage()

    def get_2d_manifold(self, image_file):
        image = loadRGB(image_file)
        som1D, som2D = self.setupSOM(image)

        print("  - Train 2D")
        som2D.trainAll()

        return som2D.nodeImage()

    # Setup SOM in 1D and 2D for the target image.
    def setupSOM(self, image):
        hist3D = Hist3D(image, num_bins=16)
        samples = hist3D._pixels
        print(len(samples))

        param1D = SOMParam(h=64, dimension=1)
        som1D = SOM(samples, param1D)

        param2D = SOMParam(h=16, dimension=2)
        som2D = SOM(samples, param2D)

        return som1D, som2D


    ## Demo for the single image file.
    def color_to_gray_debug(self, image_file, gray_name, gray_reverse_name, debug):
        image = loadRGB(image_file)

        som1D, som2D = self.setupSOM(image)

        fig = plt.figure(figsize=(12, 10))
        fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.9, wspace=0.1, hspace=0.2)

        font_size = 15
        fig.suptitle("SOM-Color Manifolds for Single Image", fontsize=font_size)

        plt.subplot(331)
        h, w = image.shape[:2]
        plt.title("Original Image: %s x %s" % (w, h), fontsize=font_size)
        plt.imshow(image)
        plt.axis('off')

        print("  - Train 1D")
        som1D.trainAll()

        print("  - Train 2D")
        som2D.trainAll()

        som1D_plot = SOMPlot(som1D)
        som2D_plot = SOMPlot(som2D)
        plt.subplot(332)
        plt.title("SOM 1D", fontsize=font_size)
        # 如果改变updateImage函数的返回值，那么可以用以下语句，代替以下第二行语句。
        # plt.imshow(som1D_plot.updateImage())
        som1D_plot.updateImage()
        plt.axis('off')

        plt.subplot(333)
        plt.title("SOM 2D", fontsize=font_size)
        som2D_plot.updateImage()
        plt.axis('off')


        color_pixels = ColorPixels(image)
        pixels = color_pixels.pixels(color_space="rgb")
        ax = fig.add_subplot(334, projection='3d')
        plt.title("cloudPoint", fontsize=font_size)
        som1D_plot.plotCloud(ax, pixels)

        hist3D = Hist3D(image, num_bins=16)
        color_samples = hist3D.colorCoordinates()
        ax = fig.add_subplot(337, projection='3d')
        plt.title("cloudPoint", fontsize=font_size)
        som1D_plot.plotCloud(ax, color_samples)


        ax1D = fig.add_subplot(335, projection='3d')
        plt.title("1D in 3D", fontsize=font_size)
        som1D_plot.plot3D(ax1D)

        ax2D = fig.add_subplot(336, projection='3d')
        plt.title("2D in 3D", fontsize=font_size)
        som2D_plot.plot3D(ax2D)

        plt.subplot(338)
        plt.title("Gray", fontsize=font_size)

        # 如果改变updateImage函数的返回值，那么可以用以下语句，代替以下第二行语句。
        a,b = som2D_plot.showGrayImage2(image)

        plt.imshow(a, cmap='gray', vmin = 0, vmax = 1)
        plt.axis('off')
        plt.imsave(self.resultFile(gray_name), a, cmap='gray',vmin = 0, vmax = 1)
        plt.imsave(self.resultFile(gray_reverse_name), b, cmap='gray',vmin = 0, vmax = 1)


        plt.subplot(339)
        plt.title("Gray", fontsize=font_size)
        plt.imshow(b, cmap='gray', vmin = 0, vmax = 1)
        plt.axis('off')

        result_file = self.resultFile("%s_debug" % gray_name)
        plt.savefig(result_file)

    def resultFile(self, image_name, image_ext=".png"):
        result_file = os.path.join(os.path.dirname(__file__), image_name + image_ext)
        return result_file

if __name__ == '__main__':
    som = SOMGraySclae()
    som.color_to_gray_debug(os.path.dirname(__file__) + '/datasets/apple/apple_0.png',
                      gray_name='gray', gray_reverse_name='gray_reverse', debug=True)

    som = SOMGraySclae()
    manifest_2d = som.get_2d_manifold(os.path.dirname(__file__) + '/datasets/apple/apple_0.png')
    plt.imsave(os.path.dirname(__file__) + '/manifest_2d.png', manifest_2d, cmap='gray', vmin=0, vmax=1)

    manifest_1d = som.get_1d_manifold(os.path.dirname(__file__) + '/datasets/apple/apple_0.png')
    plt.imsave(os.path.dirname(__file__) + '/manifest_1d.png', manifest_1d, cmap='gray', vmin=0, vmax=1)

    gray, gray_reverse = som.get_gray_scal(os.path.dirname(__file__) + '/datasets/apple/apple_0.png')
    plt.imsave(os.path.dirname(__file__) + '/gray.png', gray, cmap='gray',vmin = 0, vmax = 1)
    plt.imsave(os.path.dirname(__file__) + '/gray_reverse.png', gray, cmap='gray', vmin=0, vmax=1)
