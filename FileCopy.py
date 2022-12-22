import time
import psutil
import shutil
import threading
import os

previous_disk_list = psutil.disk_partitions()


def check_new_disk():
    global previous_disk_list
    current_disk_list = psutil.disk_partitions()
    is_disk_add = len(current_disk_list) > len(previous_disk_list)
    if len(current_disk_list) != len(previous_disk_list):
        previous_disk_list = current_disk_list
    return is_disk_add


def copy_disk():
    global previous_disk_list
    target_dir = './' + str(time.strftime('%Y-%m-%d %H.%M.%S', time.localtime(time.time())))
    src_dir = previous_disk_list[-1].mountpoint.replace('\\', '/')
    os.mkdir(target_dir)
    print("start copy the disk:" + previous_disk_list[-1].device + " from:" + src_dir + " to:" + target_dir)
    threading.Thread(target=copy_dir(src_dir, target_dir)).start()


def copy_dir(src, target):
    try:
        file_list = os.listdir(src)
    except Exception as e:
        print(e)
        return
    for name in file_list:
        if os.path.isdir(src + '/' + name):
            print('start copy dir:' + src + '/' + name)
            os.mkdir(target + '/' + name)
            copy_dir(src + '/' + name, target + '/' + name)
        elif os.path.isfile(src + '/' + name):
            print('start copy file:' + src + '/' + name)
            threading.Thread(target=lambda: shutil.copy(src + '/' + name, target + '/' + name)).start()


def main():
    while True:
        if check_new_disk():
            print("The disk list changed!")
            copy_disk()
        else:
            print("monitor the disk list change ...")
        time.sleep(1)


if __name__ == '__main__':
    main()
