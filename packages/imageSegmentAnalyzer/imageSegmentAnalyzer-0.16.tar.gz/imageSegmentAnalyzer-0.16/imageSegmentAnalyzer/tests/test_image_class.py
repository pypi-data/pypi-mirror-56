from unittest import TestCase
import numpy as np
import matplotlib.pyplot as plt
from imageSegmentAnalyzer.image import Image
import rawpy
from skimage.color import rgb2hsv,rgb2grey


class TestImage(TestCase):
    def setUp(self):
        self.img = rawpy.imread("TestImg3.NEF")
        self.I = Image(image=self.img, name="Test")
        self.I.select_points(name="column1A", shape="rectangle", rows=33, columns=8,
                             points=[[1265.4519217793313, 235.97145579854194],
                                     [1228.3420703378579, 2345.7487165855196],
                                     [1730.970515697517, 251.79981742008587]])
        self.I.select_points(name="column2A", shape="rectangle", rows=17, columns=2,
                             points=[[2012.4414514832285, 265.57813164320805],
                                     [2032.0545832184525, 1290.2104755026899],
                                     [2078.476218574243, 269.5308789522611]])
        self.I.select_points(name="column2A-2", shape="rectangle", rows=16, columns=2, row_start=17,
                             points=[[2039.657558968272, 1356.3186423398915],
                                     [2075.22399675894, 2351.0048873519872],
                                     [2102.556143498964, 1356.5185741323305]])
        self.I.select_points(name="column2A-3", shape="rectangle", rows=16, columns=3, column_start=6,
                             points=[[2302.8045925848346, 226.38600492249816],
                                     [2298.2437565036416, 1181.9267624869933],
                                     [2438.896012253875, 222.18587138667925]])
        self.I.select_points(name="column2A-4", shape="rectangle", rows=17, columns=3, column_start=6, row_start=16,
                             points=[[2345.8230453756773, 1298.5127766969872]
                                 , [2394.469136127031, 2356.5652505389344],
                                     [2479.5997949419, 1286.3512540091488]])
        self.I.select_points(name="column3A-1", shape="rectangle", rows=16, columns=8,
                             points=[[2704.4808583495346, 217.02330914372243],
                                     [2661.269156383273, 1183.2633254448685],
                                     [3160.768157795752, 240.3484007324065]])
        self.I.select_points(name="column3A-2", shape="rectangle", rows=17, columns=8, row_start=17,
                             points=[[2693.7062825416538, 1350.3552183645627],
                                     [2769.1363062055766, 2414.4163033246928],
                                     [3156.958156953698, 1316.043469802245]])

    def test_plot_intensities(self):
        self.I.plot_intensities()

    def test_init_image(self):
        self.assertIsInstance(I, Image)

    def test_process_image(self):
        self.I.process_image()
        self.assertIsInstance(self.I.processed_image, np.ndarray)

    def test_select_points(self):
        self.I.select_points(name="test1")
        print(self.I.sections["test1"])

    def test_select_points(self):

        self.I.show()
        plt.show()
        self.I.get_values(pixels=30, type="smooth_max")

    def test_segment_images(self):
        self.I.select_points(name="column1A", shape="rectangle", rows=8, columns=33)
        self.I.select_points(name="column2A", shape="rectangle", rows=8, columns=33)
        self.I.show()
        plt.show()
        seg = self.I.get_segmented()
        k = seg.values()
        print(seg)
        plt.imshow(seg['column1Aa0'])
        plt.show()

    def test_getValues_images(self):
        self.I.select_points(name="column1A", shape="rectangle", rows=33, columns=8)
        self.I.show()
        plt.show()
        self.I.get_values()