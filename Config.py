from configobj import ConfigObj
import os
import datetime
import sys

class ini_operate:
    file_path = os.path.dirname(os.path.abspath(sys.argv[0])) + '\conf.ini'
    print(file_path)
    #命令集合（字典）
    order_dist = dict()
    def __init__(self):
        config = ConfigObj()
        #检查配置文件是否存在
        if(os.path.exists(self.file_path)):
            config = ConfigObj(self.file_path)
            self.order_dist = config.dict()
            return
        else:
            config.filename = self.file_path
            config['create_time'] = datetime.datetime.now()
            config['ratio_l'] = 0.43
            config['ratio_r'] = 0.64
            config['start_x'] = 120
            config['end_x'] = 500
            config['start_y'] = 60
            config['end_y'] = 320
            config['line_left_width'] = 1
            config['line_left'] = 50
            config['line_right_width'] = 5
            config['line_right_h'] = 50
            config['line_right_v'] = 50
            config.write()
