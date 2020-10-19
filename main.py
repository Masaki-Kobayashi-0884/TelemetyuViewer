import tkinter as tk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pyproj import geod

# import communication as com
import communication_ as com
import figure


class Application(tk.Frame):
    def __init__(self, master=None):
        self.data = ""
        self.latitude = 0.0
        self.longitude = 0.0
        self.height = 0.0
        self.lat0 = 40.242865
        self.lon0 = 140.010450

        # pyproj
        self.geo = geod.Geod(ellps='WGS84')

        # communication
        self.com = com.Communication('COM3')
        # [緯度, 経度, 高度]

        # figure
        self.fig_map = figure.Map()
        self.fig_height = figure.Height()

        # Tkinter
        super().__init__(master)
        self.master = master
        self.master.title("TelemetryViewer")
        self.master.geometry("1024x768")
        self.master.resizable(False, False)
        self.pack()
        self.create_widgets()
        self.master.after(1000, self.update_widgets)

    def create_widgets(self):
        # グラフ
        self.frame_canvas = tk.Frame(self.master)
        self.frame_canvas.pack(side=tk.LEFT)

        self.canvas_map = FigureCanvasTkAgg(self.fig_map.fig, master=self.frame_canvas)
        self.canvas_map.draw()
        self.canvas_map.get_tk_widget().pack()

        self.canvas_height = FigureCanvasTkAgg(self.fig_height.fig, master=self.frame_canvas)
        self.canvas_height.draw()
        self.canvas_height.get_tk_widget().pack()

        # 情報
        self.frame_info = tk.Frame(self.master)
        self.frame_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.text_status = tk.Label(self.frame_info, text='Status', font=("メイリオ", 18))
        self.info_signal = tk.Label(self.frame_info, text='receive signal', font=("メイリオ", 18))
        self.info_status = tk.Label(self.frame_info, text='', font=("メイリオ", 18),)
        labels_top = [self.text_status,
                      self.info_signal,
                      self.info_status]
        [label.pack(side=tk.TOP) for label in labels_top]

        self.text_lat = tk.Label(self.frame_info, text='Latitude', font=("メイリオ", 18))
        self.info_lat = tk.Label(self.frame_info, text="0.0°E", font=("メイリオ", 18))
        self.text_lon = tk.Label(self.frame_info, text='Longitude', font=("メイリオ", 18))
        self.info_lon = tk.Label(self.frame_info, text="0.0°E", font=("メイリオ", 18))
        self.text_hight = tk.Label(self.frame_info, text='Height', font=("メイリオ", 18))
        self.info_hight = tk.Label(self.frame_info, text="0.0 m", font=("メイリオ", 18))
        labels_bottom = [self.text_lat,
                         self.info_lat,
                         self.text_lon,
                         self.info_lon,
                         self.text_hight,
                         self.info_hight]
        [label.pack(side=tk.BOTTOM) for label in labels_bottom[::-1]]

    def update_widgets(self):
        # 情報取得
        if self.com.update():  # 成功
            self.data = self.com.data_latest
            self.latitude = self.data[0]
            self.longitude = self.data[1]
            self.height = self.data[2]

            # 受信できたときだけ更新するやつ
            self.info_signal["text"] = "receive signal"
            self.info_signal["fg"] = "green"
            self.info_lat["text"] = str(self.latitude) + "°E"
            self.info_lon["text"] = str(self.longitude) + "°N"
            self.info_hight["text"] = str(self.height) + " m"
        else:  # 失敗
            self.latitude = None
            self.longitude = None
            self.height = None
            self.info_signal["text"] = "lost signal"
            self.info_signal["fg"] = "red"

        # info更新
        self.info_status["text"] = "\n".join(self.com.status_list)

        # figure更新
        try:
            x, y = self.lat2meter(self.latitude, self.longitude)
        except TypeError:
            x = None
            y = None
        self.fig_map.update(x, y)
        self.canvas_map.draw()

        self.fig_height.update(self.height)
        self.canvas_height.draw()

        self.master.after(1000, self.update_widgets)

    def lat2meter(self, lat, lon):
        azi, _, dis = self.geo.inv(self.lon0, self.lat0, lon, lat)
        theta = np.deg2rad(450 - azi % 360)
        x = dis * np.cos(theta)
        y = dis * np.sin(theta)
        return x, y


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    app.mainloop()
