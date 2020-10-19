import datetime
import sys

import im920_
from serial.tools import list_ports


class Communication:
    def __init__(self, port=None):
        if port is None:
            ports = list_ports.comports()
            if ports == []:
                print("no comport")
                sys.exit()
            port = ports[0].device
        self.com = im920_.Im920(port)  # 後で戻す -> im920

        self.receive_buf = list()
        self.data_latest = list()
        self.status_list = list()

        # # ログファイル作成
        # dt_now = datetime.datetime.now()
        # now_str = dt_now.strftime('%m%d%H%M%S')
        # self.result_path = "output/result" + now_str + ".csv"
        # with open(self.result_path, 'w') as f:
        #     f.write("Node,ID,RSSI,data")

    def pairing(self, send_id, hex_=True):
        self.com.add_id(str(send_id), Hex=hex_)

    def update(self):
        while len(self.com.buf) > 0:
            raw = self.com.receive()
            self.receive_buf.append(raw)
        self.store(self.receive_buf)

        # 最新データを更新
        update_flag = False
        for data in self.receive_buf:
            if len(data.split(',')) > 1:  # 後で戻す -> data[3]
                self.data_latest = [float(s) for s in data.split(',')]  # 後で戻す -> data[3]
                update_flag = True
            else:
                self.status_list.append(data)  # 後で戻す -> data[3]
                update_flag = True

        self.receive_buf = []
        return update_flag

    def store(self, data):
        pass
        # with open(self.result_path, 'a'):
        #     pass


if __name__ == "__main__":
    com = Communication('COM3')
