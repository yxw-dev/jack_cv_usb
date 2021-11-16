import cv2
import sys
import os
import time
import glob
import Config
from cv_show import *
from usb_pi import get_port
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from configobj import ConfigObj
import cv2_model

class MyMainWindow(QMainWindow , Ui_MainWindow):
    def __init__(self ):
        super(MyMainWindow, self).__init__()
        self.mear_step = 20
        self.focal = 0
        self.config = {}
        self.ratio = [0.43 , 0.64]
        self.setupUi(self)
        self.start_time1 = time.time()
        self.start_time2 = time.time()
        self.frame1=0
        self.frame2=0
        self.cam_time = QtCore.QTimer()
        self.cam_time2 = QtCore.QTimer()
        self.init_time = QtCore.QTimer()
        self.cam_time.timeout.connect(self.show_pic)
        self.cam_time2.timeout.connect(self.show_pic2)
        self.init_time.timeout.connect(self.my_init)
        self.horizontalSlider.valueChanged.connect(self.drawline)
        self.verticalSlider.valueChanged.connect(self.drawline)
        self.setFocus()
        self.init_time.start(100)
        self.cam_number = [0,1]
        self.get_pixmap_flag = 0
        self.ca_step = cv2_model.cv_match()
        self.temp_step = 0
        self.count = 0#计数，多次无结果将step设0



    def my_init(self):
        #填满窗体中空隙
        self.pushButton_l.resize(self.pushButton.width() , 75)
        self.pushButton_l.move(self.pushButton.x(),self.pushButton.y()+self.pushButton.height() - 8)
        self.pushButton_l.lower()

        #设置操作label背景图
        path = os.path.dirname(os.path.abspath(__file__))
        temp_pic = QPixmap(path + '/image/操作说明图.png').scaled(self.label_11.width(), self.label_11.height())
        self.label_11.setPixmap(temp_pic)
        self.init_time.stop()

        #读取配置参数（左右相机放大率，默认线位置）设置指示线位置
        try:
            ini = Config.ini_operate()
            self.config = ini.order_dist
            if not self.config:
                QMessageBox.warning(self , '提示','配置文件加载失败')
        except:
            QMessageBox.show('配置文件加载失败')
        self.width_step_max = 15
        self.height_step_max = 15
        self.width_step = float(self.config['line_left_width'])  # 横向两红线间隔默认值
        self.height_step = float(self.config['line_right_width'])  # 纵向两红线间隔默认值
        self.doubleSpinBox.setValue(self.height_step)
        self.doubleSpinBox_2.setValue(self.width_step)
        self.horizontalSlider.setValue(int(self.config['line_left']))
        self.verticalSlider.setValue(int(self.config['line_right_v']))
        self.pushbutton5_y = int(self.config['line_right_h'])
        #获取相机编号
        self.cam_number = [0,1]

        #启动相机
        self.start_grap()
        self.start_grap2()
        #检查保存图像路径是否存在
        save_path = path + '/图片'
        if os.path.exists(save_path):
            print ('路径不存在')
        else:
            os.makedirs(save_path)
        #lcdnumber显示设置
        self.lcdNumber.setDecMode()
        self.lcdNumber_2.setDecMode()
        self.lcdNumber.setDigitCount(5)
        self.lcdNumber_2.setDigitCount(5)
        self.step_show_label.move(self.lcdNumber.x() + self.lcdNumber.width() + 2, self.lcdNumber.y() + 18)
        self.step_show_label.setFont(QFont("Arial",18))
        self.step_show_label.raise_()
    #键盘监控事件
    def keyPressEvent(self,event):
        if(event.key() == Qt.Key_Q):
            file_path = os.path.dirname(os.path.abspath(sys.argv[0])) + '\conf.ini'
            config = ConfigObj(file_path)
            config['line_left_width'] = self.width_step
            config['line_left'] = self.horizontalSlider.value()
            config['line_right_width'] = self.height_step
            config['line_right_h'] = self.pushbutton5_y
            config['line_right_v'] = self.verticalSlider.value()
            config.write()
            self.close()
        if(event.key() == Qt.Key_I):
            self.focal_set(500)
        if(event.key() == Qt.Key_F):
            self.start_grap()
        if (event.key() == Qt.Key_B):
            self.start_grap2()
        if(event.key() == Qt.Key_C):
            self.get_pixmap_flag = 2
        if(event.key() == Qt.Key_A):
            self.horizontalSlider.setValue(self.horizontalSlider.value() - 1)
            self.update()
        if (event.key() == Qt.Key_D):
            self.horizontalSlider.setValue(self.horizontalSlider.value() + 1)
            self.update()
        if(event.key() == Qt.Key_W):
            if(self.width_step < self.width_step_max):
                self.width_step = self.width_step + 0.01
            else:
                self.width_step = 0
            self.update()
            self.drawline()
            self.doubleSpinBox_2.setValue(self.width_step)
        if (event.key() == Qt.Key_S):
            if (self.width_step > 0):
                self.width_step = self.width_step - 0.01
            else:
                self.width_step = self.width_step_max
            self.update()
            self.drawline()
            self.doubleSpinBox_2.setValue(self.width_step)


        if (event.key() == Qt.Key_Left):
            self.verticalSlider.setValue(self.verticalSlider.value() + 1)
            self.update()
        if (event.key() == Qt.Key_Right):
            self.verticalSlider.setValue(self.verticalSlider.value() - 1)
            self.update()
        if(event.key() == Qt.Key_Comma):
            self.pushbutton5_y = self.pushbutton5_y - 1
            self.drawline()
        if(event.key() == Qt.Key_Period):
            self.pushbutton5_y = self.pushbutton5_y + 1
            self.drawline()
        if (event.key() == Qt.Key_Up):
            if (self.height_step < self.height_step_max):
                self.height_step = self.height_step + 0.01
            else:
                self.height_step = 0
            self.update()
            self.drawline()
            self.doubleSpinBox.setValue(self.height_step)
        if (event.key() == Qt.Key_Down):
            if (self.height_step > 0):
                self.height_step = self.height_step - 0.01
            else:
                self.height_step = self.height_step_max
            self.update()
            self.drawline()
            self.doubleSpinBox.setValue(self.height_step)


    def drawline(self):
        try:
            self.focal_set(self.horizontalSlider.value() * 5)
        except:
            return
        sta1 = self.label.x() + (self.label.width() /  100) * float(self.horizontalSlider.value()+0.5)
        sta2 = self.label_2.y() + (self.label_2.height() /  100) * float(99 - self.verticalSlider.value() + 0.5)
        step1 = (self.doubleSpinBox_2.value()/ 20) * self.label.width()
        step2 = (self.doubleSpinBox.value() / 15) * self.label_2.height()

        #更新lcd显示当前线宽长度
        self.lcdNumber.display('%.3f'%(float(self.config['ratio_l']) * self.width_step))
        self.lcdNumber_2.display('%.3f'%(float(self.config['ratio_r']) * self.height_step))
        # 绘制纵向指示线（相机一）
        if (sta1 - step1/2)>self.label.x():
            self.pushButton1.move(sta1 - step1/2 , self.label.y())
        else:
            self.pushButton1.move(self.label.x() + 1, self.label.y())
        if (sta1 + step1 / 2) < (self.label.x() + self.label.width()):
            self.pushButton2.move(sta1 + step1 / 2, self.label.y())
        else:
            self.pushButton2.move(self.label.x(), self.label.width() - 1)

        #绘制横向指示线（相机二）
        if (sta2 - step2/2)>(self.label_2.y()+ self.menubar.height()):
            self.pushButton3.move(self.label_2.x() ,sta2 - step2/2)
        else:
            self.pushButton3.move(self.label_2.x() , self.label_2.y()-1)
        if (sta2 + step2/2) < (self.label_2.y() + self.label_2.height()):
            self.pushButton4.move(self.label_2.x(), sta2 + step2/2)
        else:
            self.pushButton4.move(self.label_2.x(), self.label_2.y() + self.label_2.height())
        if(self.pushbutton5_y < self.label_2.width()):
            self.pushButton5.move(self.pushbutton5_y + self.label_2.x(), self.label_2.y())
        else:
            self.pushbutton5_y = self.label_2.x() +1
            self.pushButton5.move(self.pushbutton5_y + self.label_2.x() , self.label_2.y())
    #调节焦距，参数a为焦距，c为opencv枚举的相机
    def focal_set(self ,a):
        self.cap1.set(28 , a)

    #移动滑块调节指示线位置
    def moveline(self):
        sta_x = self.horizontalSlider.x()
        sta_y = self.line_2.y()
        length = float(self.horizontalSlider.width()) / 100.0
        sta = sta_x + length/3
        val = self.horizontalSlider.value()
        self.line.move(sta + val*length + val/15 - self.mear_step/2 , sta_y)
        self.line_2.move(sta + val*length + val/15 + self.mear_step/2 , sta_y)
    def start_grap(self):
        self.start_time1 = time.time()
        self.frame1=0
        self.cap1 = cv2.VideoCapture(self.cam_number[0] , cv2.CAP_DSHOW)
        #self.cap1.set(39 , 0)       #关闭自动调焦(af),mf
        self.cap1.set(cv2.CAP_PROP_FRAME_WIDTH , 1920)
        self.cap1.set(cv2.CAP_PROP_FRAME_HEIGHT , 1080)
        print(self.cap1.set(6 , cv2.VideoWriter.fourcc('M','J','P','G')))
        #self.cap1.set(3,1920)
        #self.cap1.set(4,1080)
        #self.cap1 = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
        self.cam_time.start(80)
        self.label_5.setText("正面相机：运行")
        self.pushButton1.resize(1, self.label.height())
        self.pushButton2.resize(1, self.label.height())
        self.pushButton1.show()
        self.pushButton2.show()
        self.drawline()

    def start_grap2(self):
        self.start_time2 = time.time()
        self.frame2=0
        self.cap2 = cv2.VideoCapture(self.cam_number[1], cv2.CAP_DSHOW)
        #self.cap2 = cv2.VideoCapture(2+ cv2.CAP_DSHOW)
        self.cam_time2.start(60)
        self.label_7.setText("侧面相机：运行")
        self.pushButton3.resize(self.label_2.width(), 1)
        self.pushButton4.resize(self.label_2.width(), 1)
        self.pushButton5.resize(1, self.label_2.height())
        self.pushButton3.show()
        self.pushButton4.show()
        self.pushButton5.show()
        self.drawline()
    def stop_cam(self):
        self.cap1.release()
        self.cam_time.stop()
        self.cap2.release()
        self.cam_time2.stop()
    def show_pic(self):
        ret, img = self.cap1.read()
        if not ret:
            print('read error!\n')
            self.label_5.setText("正面相机：打开失败")
            self.pushButton1.hide()
            self.pushButton2.hide()
            self.cam_time.stop()
            return
        cut = img[int(self.config['start_y']):int(self.config['end_y']) , int(self.config['start_x']):int(self.config['end_x'])] # 裁剪坐标为[y0:y1, x0:x1]
        temp = cv2.rotate(cut ,1)
        #img_rote = temp[0:640, 80:480]
        #temp = img[130:550, 0:480]  # 裁剪坐标为[y0:y1, x0:x1]de
        cur_frame = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)
        heigt, width = cur_frame.shape[:2]
        pixmap = QImage(cur_frame, width, heigt, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(pixmap)
        self.label.setPixmap(pixmap)
        #匹配计算间距
        loc , step = self.ca_step.get_step(cur_frame)
        if step < 0.3:
            # 调节正面相机间距指示线位置loc
            start_point  = self.label.x() + loc * 2#一个系数，图像像素和label宽度的比
            self.temp_step = step
            self.step_show_label.setText('%.3f' % (float(self.temp_step)))
            if self.count > 4:
                self.count = self.count - 1
            else:
                self.count = 0
        else:
            self.count = self.count + 1
            if self.count > 8:
                self.step_show_label.setText('0')
                self.count = 0
        if step > float(self.lcdNumber.value()):
            self.pushButton1.setStyleSheet("border:2px solid rgb(255,0,0)")
            self.pushButton2.setStyleSheet("border:2px solid rgb(255,0,0)")
        else:
            self.pushButton1.setStyleSheet("border:2px solid rgb(0,255,0)")
            self.pushButton2.setStyleSheet("border:2px solid rgb(0,255,0)")

        end_time1 = time.time()
        diff_time1 = (end_time1 - self.start_time1)
        self.frame1 = self.frame1 + 1
        if diff_time1>1:
            self.start_time1 = end_time1
            self.label_6.setText('帧率(1):' + str(self.frame1))
            self.frame1 = 0
        # 保存一帧图像
        if(self.get_pixmap_flag == 2):
            file_number = glob.glob(os.path.dirname(os.path.abspath(__file__))+'/图片/'+'*.jpg')
            if(len(file_number) == 0):
                file_name = os.path.dirname(os.path.abspath(__file__)) + '/图片/' + "1" + "_f.jpg"
                pixmap.save(file_name)
                return
            file_name = os.path.dirname(os.path.abspath(__file__))+'/图片/' + str(len(file_number)+1) + "_f.jpg"
            pixmap.save(file_name)
            self.get_pixmap_flag = 1
    def show_pic2(self):
        ret_2, img_2 = self.cap2.read()
        if not ret_2:
            print('read error!\n')
            self.label_7.setText("侧面相机：打开失败")
            self.pushButton3.hide()
            self.pushButton4.hide()
            self.pushButton5.hide()
            self.cam_time2.stop()
            return
        #cv2.flip(img_2, 1, img_2)
        temp = cv2.rotate(img_2, 2)
        cur_frame = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)
        heigt, width = cur_frame.shape[:2]
        pixmap = QImage(cur_frame, width, heigt, QImage.Format_RGB888)
        trs = QTransform()
        trs.rotate(270)
        pixmap = pixmap.transformed(trs)
        pixmap = QPixmap.fromImage(pixmap)
        self.label_2.setPixmap(pixmap)
        end_time2 = time.time()
        diff_time2 = (end_time2 - self.start_time2)
        self.frame2 = self.frame2 + 1
        if diff_time2 > 1:
            self.start_time2 = end_time2
            self.label_8.setText('帧率(2):' + str(self.frame2))
            self.frame2 = 0
        #保存一帧图像
        if (self.get_pixmap_flag == 1):
            file_number = glob.glob(os.path.dirname(os.path.abspath(__file__)) + '/图片/' + '*.jpg')
            if (len(file_number) == 0):
                file_name = os.path.dirname(os.path.abspath(__file__)) + '/图片/' + "1" + "_b.jpg"
                pixmap.save(file_name)
                return
            file_name = os.path.dirname(os.path.abspath(__file__)) + '/图片/' + str(len(file_number) + 1) + "_b.jpg"
            pixmap.save(file_name)
            self.get_pixmap_flag = 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyMainWindow()
    win.showFullScreen()
    sys.exit(app.exec_())


