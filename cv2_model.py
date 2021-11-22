import cv2
import os
import sys
import time

class cv_match:
    def __init__(self):
        self.file_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.mod1 = cv2.imread(self.file_path + '\image\mod_needle.jpg')
        self.mod2 = cv2.imread(self.file_path + '\image\mod_shuttle .jpg')
        self.height_n = 66
        self.width_n = 32
        self.height_s = 16
        self.width_s = 18
        self.left_line = 0
        self.right_line = 100
        self.needle = cv2.cvtColor(self.mod1, cv2.COLOR_BGR2RGB)
        self.shuttle = cv2.cvtColor(self.mod2, cv2.COLOR_BGR2RGB)

    def get_step(self , img):
        res_needle = cv2.matchTemplate(img, self.needle, cv2.TM_CCOEFF)
        res_shuttle = cv2.matchTemplate(img, self.shuttle, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res_needle)
        # cv2.rectangle(img, (max_loc[0], max_loc[1]), (max_loc[0] + self.width_n, max_loc[1] + self.height_n), (0, 0, 255), 1)
        mv, mxv, minl, maxl = cv2.minMaxLoc(res_shuttle)
        # cv2.rectangle(img, (maxl[0], maxl[1]), (maxl[0] + self.width_s, maxl[1] + self.height_s), (0, 255, 0), 1)
        left_line = max_loc[0] + 28
        right_line = minl[0] - 2
        res = (left_line + right_line) / 2
        step = (right_line - left_line) * 0.022
        # cv2.imshow('3' , img)
        # cv2.waitKey()
        return int(res) , step.__abs__()

# tem = cv_match()
# p =  os.path.dirname(os.path.abspath(sys.argv[0]))
# img = cv2.imread(p + '\image\id.jpg')
# t1 = time.time()
# res = tem.get_step(img)
# t2 = time.time()
# diff = t2 - t1
# print(diff)
