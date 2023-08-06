
图像灰度化  Image Grayscale
====

本文的图像灰度化实现主要基于：

1. Data-driven Color Manifolds [Nguyen et al. 2015].
2. Color-to-gray conversion using ISOMAP [Cui et al. 2010].
3. 一种快速映射Isomap算法 [圣少友 et al. 2009].

使用方法:
===

##### 获取灰度图
    gray, gray_reverse = som.get_gray_scal(os.path.dirname(__file__) + '/datasets/apple/apple_0.png')
    plt.imsave(os.path.dirname(__file__) + '/gray.png', gray, cmap='gray',vmin = 0, vmax = 1)
    plt.imsave(os.path.dirname(__file__) + '/gray_reverse.png', gray, cmap='gray', vmin=0, vmax=1)
##### 获取一维流形：
    som = SOMGraySclae()
    manifest_1d = som.get_1d_manifold(os.path.dirname(__file__) + '/datasets/apple/apple_0.png')
    plt.imsave(os.path.dirname(__file__) + '/manifest_1d.png', manifest_1d, cmap='gray', vmin=0, vmax=1)

##### 获取二维流形：
    som = SOMGraySclae()
    manifest_2d = som.get_2d_manifold(os.path.dirname(__file__) + '/datasets/apple/apple_0.png')
    plt.imsave(os.path.dirname(__file__) + '/manifest_2d.png', manifest_2d, cmap='gray', vmin=0, vmax=1)
  
##### 获取debug plt：
    som = SOMGraySclae()
    som.color_to_gray_debug(os.path.dirname(__file__) + '/datasets/apple/apple_0.png',
                       gray_name='gray', gray_reverse_name='gray_reverse', debug=True)    

灰度化结果
===

#### 输入图像：

![](./som_cm/datasets/apple/apple_0.png)

#### 获取灰度图，输出图像：

![](./som_cm/results/gray.png)
![](./som_cm/results/gray_reverse.png)

#### for debug:
![](./som_cm/results/gray_debug.png)

#### 所有结果：
![](./som_cm/results/result_all.png)


感谢
===

项目中采用Nguyen等人的论文实现，基于以下开源项目：
[https://github.com/tody411/SOM-ColorManifolds](https://github.com/tody411/SOM-ColorManifolds)


## License

The MIT License 2017 (c) tody