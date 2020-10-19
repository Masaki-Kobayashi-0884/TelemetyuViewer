class Communication():
    def __init__(self, port="COM3"):
        with open("test/data.csv", 'r') as f:
            self.data = f.readlines()
        self.i = 0
        self.data_latest = list()
        self.status_list = list()

    def update(self):
        line = self.data[self.i].strip().split(',')
        if len(line) == 1:
            if line == ['failure']:
                self.i += 1
                return False

            self.status_list.append(line[0])
            self.i += 1
            self.update()
        else:
            self.data_latest = [float(s) for s in line]
            self.i += 1
        return True


if __name__ == "__main__":
    com = Communication()
    for i in range(30):
        com.update()
        print(com.data_latest)
        print(com.status_list)
