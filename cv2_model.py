import cv2
import os
import sys

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
        src = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res_needle = cv2.matchTemplate(src, self.needle, cv2.TM_SQDIFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res_needle)
        cv2.rectangle(img, (min_loc[0], min_loc[1]), (min_loc[0] + self.width_n, min_loc[1] + self.height_n), (0, 0, 255), 1)
        res_shuttle = cv2.matchTemplate(src, self.shuttle, cv2.TM_SQDIFF)
        mv, mxv, minl, maxl = cv2.minMaxLoc(res_shuttle)
        cv2.rectangle(img, (minl[0], minl[1]), (minl[0] + self.width_s, minl[1] + self.height_s), (0, 255, 0), 1)
        left_line = min_loc[0] + 28
        right_line = minl[0] - 2
        res = (left_line + right_line) / 2
        step = (right_line - left_line) * 0.022
        return int(res) , step.__abs__()

te = cv_match()



