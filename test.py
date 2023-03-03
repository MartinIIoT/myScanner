import subprocess
import time

usb_cesta = "/dev/sda1"
usb_file_cesta = "/home/pi/myScanner/myUSB/"

usb = 0

try:
    subprocess.check_output("sudo mount " + usb_cesta + " " + usb_file_cesta, shell=True)
    #subprocess.run(['sudo', 'mount', usb_cesta, usb_file_cesta])
    usb = 1
    print("Mount OK")
    time.sleep(10)
except subprocess.CalledProcessError:
    print("Mount Err")


if usb == 1:
    try:
        subprocess.check_output("sudo umount " + usb_file_cesta, shell=True)
        #subprocess.run(['sudo', 'umount', usb_file_cesta])
        usb = 0
        print("Unmount OK")
    except subprocess.CalledProcessError:
        print("Unmount Err")