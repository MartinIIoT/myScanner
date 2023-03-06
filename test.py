import subprocess
import pathlib

usb_path = "/dev/sda1"
usb_file_path = "/home/pi/myScanner/myUSB/"
desktop = pathlib.Path(usb_file_path)

suborov = 0

try:
        subprocess.check_output("sudo mount " + usb_path + " " + usb_file_path, shell=True)
        for item in desktop.iterdir():
                if not(item.is_dir()):
                        suborov += 1
        try:
                subprocess.check_output("sudo umount " + usb_file_path, shell=True)
        except subprocess.CalledProcessError:
                print("Unmount Err")
except subprocess.CalledProcessError:
        print("Mount Err")

print(suborov)