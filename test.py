import sys
import clr
import System
from System import Environment
from System import String, Char, Int32, Environment, IntPtr

halconroot = Environment.GetEnvironmentVariable("HALCONROOT")
h = clr.AddReference("source/halcondotnet")
d = clr.AddReference("source/hdevenginedotnet")

print(h)
from HalconDotNet import *

ho_Image1 = HImage()
ho_Image2 = HImage()
hv_Window = HWindow()

#读取模型图像
ho_Image1.ReadImage("image/model_needle.png")
ho_Image2.ReadImage("image/model_shuttle.png")

#创建模型
hv_model1 = HTuple()
rad = HTuple(360)
print(hv_model1)
HOperatorSet.CreateShapeModel(ho_Image1 , 0 , 0 ,rad.TupleRad() , 0 , "no_pregeneration" , "use_polarity" , 60 ,20 ,out hv_model1)
print(hv_model1)