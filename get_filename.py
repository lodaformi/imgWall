class getFileName():
    def __init__(self):
        pass

    def find_last_index(self, string, str):
        last_position = -1
        while True:
            position = string.find(str, last_position + 1)
            if position == -1:
                return last_position
            last_position = position

    def getName(self, string, str):
        index = self.find_last_index(string, str) + 1
        length = len(string)
        return string[index:(length - 4)]

if __name__ == '__main__':
    filename = 'H:\code\medicalUI\imgs\dicom\9000099.dcm'
    # filename = 'H:/code/medicalUI/imgs/npy/9000099_s0.jpg'
    get = getFileName()
    print(get.getName(filename, '\\'))