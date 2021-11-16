import os
import re

def get_port():
    # 通过命令行获取两usb相机端口信息
    test = os.popen('ls -l /dev|grep _cam')
    text = test.read()

    # 拆分出端口号信息
    res_text = []
    words = []
    index = 0
    start = 0

    while index < len(text):
        start = index
        while text[index] != " " and text[index] not in [",", ",", "\n"]:
            index += 1
            if index == len(text):
                break
        words.append(text[start:index])
        if index == len(text):
            break
        while text[index] == " " or text[index] in [",", ".", "\n"]:
            index += 1
            if index == len(text):
                break
    if(("frame_cam" not in words) | ("back_cam" not in words)):
        res_text.append(0)
        res_text.append(1)
        return res_text
    else:
        video_frame = words[words.index('frame_cam') + 2]
        video_back = words[words.index('back_cam') + 2]

    if len(video_frame) < 7:
        num_frame = video_frame[5]
    else:
        num_frame = video_frame[5:]
    if len(video_back) < 7:
        num_back = video_back[5]
    else:
        num_back = video_back[5:]
    print(num_frame, num_back)

    # 判断端口号，生成opencv调用相机的序号。如果都为偶数使用（/dev/frame_cam和/dev/back_cam）调用，否则判断用0,2调用。
    sum_num = int(num_back) + int(num_frame)
    print(sum_num)
    if sum_num % 2 < 1 and int(num_frame) % 2 < 1:
        res_text.append("/dev/frame_cam")
        res_text.append("/dev/back_cam")
    elif num_frame < num_back:
        res_text.append(0)
        res_text.append(2)
    else:
        res_text.append(2)
        res_text.append(0)
    return res_text