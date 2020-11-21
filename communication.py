import datetime
import sys

import im920
from serial.tools import list_ports


class Communication:
    def __init__(self, port=None):
        if port is None:
            ports = list_ports.comports()
            if ports == []:
                print("no comport")
                sys.exit()
            port = ports[0].device
        self.com = im920.Im920(port)

        self.receive_buf = list()
        self.data_latest = list()
        self.status_list = list()

        # ログファイル作成
        dt_now = datetime.datetime.now()
        now_str = dt_now.strftime('%m%d%H%M%S')
        self.result_path = "output/log_" + now_str + ".csv"
        with open(self.result_path, 'w') as f:
            f.write("Node,ID,RSSI,data\r\n")

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
            if len(data[3].split(',')) > 1:
                self.data_latest = [float(s) for s in data[3].split(',')]
                update_flag = True
            else:
                self.status_list.append(data[3])
                update_flag = True

        self.receive_buf = []
        return update_flag

    def store(self, data):
        with open(self.result_path, 'a') as f:
            for line in data:
                f.write(','.join(line))


if __name__ == "__main__":
    com = Communication('COM3')
