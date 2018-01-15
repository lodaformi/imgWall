import random

class imgList():
    def __init__(self):
        self.img_names = []

        filename=open('allfilename.txt', 'r')

        for line in filename.readlines():
            temp_name = line.strip('\n')
            self.img_names.append(temp_name)


    def selectImg(self):
        select_images = []

        for i in range(400):
            index = random.randint(0, len(self.img_names))
            img_name = self.img_names.pop(index)
            # print len(img_names)
            # print index
            select_images.append(img_name)
        return select_images


if __name__ == '__main__':
    imagelist = imgList()
    templist = imagelist.selectImg()
    templist2 = imagelist.selectImg()
    print(len(templist))
    print(templist)
    print(templist2)
    # for i in range(len(templist)):
    #     print templist[i]