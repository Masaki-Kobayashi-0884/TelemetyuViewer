import time

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


class Map:
    def __init__(self):
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)

        pixel2meter = 7.246376811
        img_map = Image.open('source/noshiro_sea.png')
        img_list = np.asarray(img_map)
        img_height = img_map.size[1]
        img_width = img_map.size[0]
        img_origin = np.array([1244, -917])
        # Define image range
        img_left = -1.0 * img_origin[0] * pixel2meter
        img_right = (img_width - img_origin[0]) * pixel2meter
        img_top = -img_origin[1] * pixel2meter
        img_bottom = -1.0 * (img_height + img_origin[1]) * pixel2meter
        self.ax.imshow(img_list, extent=(img_left, img_right, img_bottom, img_top))

        self.x_list = list()
        self.y_list = list()
        self.lines, = self.ax.plot(self.x_list, self.y_list, color='red', marker='.')

        self.ax.set_xlim(-1500, 500)
        self.ax.set_ylim(-500, 1000)

    def update(self, x, y):
        self.x_list.append(x)
        self.y_list.append(y)
        self.lines.set_data(self.x_list, self.y_list)


class Height:
    def __init__(self):
        plt.style.use('ggplot')
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)

        self.height_list = list()
        self.time_list = list()
        self.time_diff = list()

        self.lines, = self.ax.plot(self.time_diff, self.height_list, color="blue", marker='.')
        self.ax.set_xlim(-1, 30)
        self.ax.set_ylim(0, 800)

    def update(self, h):
        self.height_list.insert(0, h)
        self.time_list.insert(0, time.time())

        if len(self.height_list) > 30:
            del (self.height_list[-1],
                 self.time_list[-1])

        self.time_diff = [time.time() - t_li for t_li in self.time_list]
        self.lines.set_data(self.time_diff, self.height_list)


if __name__ == "__main__":
    map_ = Map()
