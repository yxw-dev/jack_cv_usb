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
