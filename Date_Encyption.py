import sys
import os
import binascii
from configobj import ConfigObj

def info_ok(number):
    # windows：win32； 树莓派，linux：linux.根据系统获取cpu序列号
    type_system = sys.platform.lower()
    if type_system == 'win32':
        cpu = os.popen('wmic cpu get processorid').read()
        cpu = cpu.strip().replace('\n', '').replace('\r', '').split(" ")
        cpu = cpu[len(cpu) - 1]
    elif type_system == 'linux':
        cpu = os.popen('echo "123" | sudo -S dmidecode -t 4 | grep ID').read()
        cpu = cpu.replace(' ', '')
        cpu = cpu[2:]
    cpu_rev = list(cpu)
    cpu_rev.reverse()
    res = ''.join(cpu_rev)
    h = res.encode().hex()
    if number == h:
        return True
    else:
        return False

def log_in():
    # windows：win32； 树莓派，linux：linux.根据系统获取cpu序列号
    type_system = sys.platform.lower()
    if type_system == 'win32':
        cpu = os.popen('wmic cpu get processorid').read()
        cpu = cpu.strip().replace('\n', '').replace('\r', '').split(" ")
        cpu = cpu[len(cpu) - 1]
    elif type_system == 'linux':
        file_path = os.path.dirname(os.path.abspath(sys.argv[0])) + '\conf.ini'
        cpu = os.popen('echo "123" | sudo -S dmidecode -t 4 | grep ID').read()
        cpu = cpu.replace(' ', '')
        cpu = cpu[2:]
        cpu_rev = list(cpu)
        cpu_rev.reverse()
        res = ''.join(cpu_rev)
        h = res.encode().hex()
        config = ConfigObj(file_path)
        config['version'] = h
        config.write()

# #以cpu序列号生成密钥(序号翻转，转化十六进制，写入ini)
# file_path = os.path.dirname(os.path.abspath(sys.argv[0])) + '\conf.ini'
# cpu_rev = list(cpu)
# cpu_rev.reverse()
# res = ''.join(cpu_rev)
# h = res.encode().hex()
# config = ConfigObj(file_path)
# config['version'] = h
# config.write()
#
#
# #从ini读取十六进制，转化为字符串，再翻转
# s = binascii.a2b_hex(h).decode()
# te = list(s)
# te.reverse()
# cpu_id = ''.join(te)
# print(cpu_id)