import subprocess
import i2clcd
import urllib.request
import time
import os

lcd = i2clcd.i2clcd(i2c_bus=1, i2c_addr=0x27, lcd_width=20)
lcd.init()

usb_key = 0
usb_path = "/dev/sda1"
usb_file_path = "/home/pi/myScanner/myUSB/"
usb_scanned = False
update_time = 30 # in seconds
update_time_temp = update_time



def update_main():
    lcd.clear()
    lcd.print_line('CHECK UPDATE', line=0, align='CENTER')
    
    try:
        
        urllib.request.urlopen('https://google.com', timeout=5) #Python 3.x
        lcd.print_line(':::  ONLINE  :::', line=2, align='CENTER')
        lcd.print_line('UPDATING', line=3, align='CENTER')
        subprocess.run(['./update.sh'])
        lcd.clear()
        return True
    except:
        lcd.print_line('...  OFFLINE  ...', line=2, align='CENTER')
        time.sleep(1)
        lcd.clear()
        return False


def find_usb():
    global usb_key
    global usb_scanned

    if os.path.exists(usb_path) and usb_key == 0:
        try:
            subprocess.check_output("sudo mount " + usb_path + " " + usb_file_path, shell=True)
            usb_key = 1
            print("Mount OK")
            time.sleep(1)
        except subprocess.CalledProcessError:
            print("Mount Err")
            usb_key = 0

        lcd.move_cursor(1, 0)
        lcd.print("USB [X]")
        time.sleep(1)
        return True
    elif not(os.path.exists(usb_path)) and usb_key == 1:
        lcd.print_line('', line=2, align='CENTER')
        lcd.move_cursor(1, 0)
        lcd.print("USB [ ]")
        usb_key = 0
        usb_scanned = False
        return False

def draw():
    lcd.print_line('===  MartinIIoT  ===', line=0, align='CENTER')
    lcd.move_cursor(1, 0)
    lcd.print("USB [ ]")
    lcd.move_cursor(1, 12)
    lcd.print('SCAN [ ]')

    version_raw = subprocess.run(['clamscan', '--version'], stdout=subprocess.PIPE)
    version_help = version_raw.stdout.decode('utf-8')

    version_core = version_help[7:version_help.find('/')]
    version_db = version_help[version_help.find('/')+1:version_help.rfind('/')]

    lcd.move_cursor(3, 0)
    lcd.print(version_core)

    lcd.move_cursor(3, 15)
    lcd.print(version_db)

update_main()
draw()

while True:
    if update_time_temp > 0:
        if find_usb() and not(usb_scanned):
            usb_scanned = True
            lcd.move_cursor(1, 12)
            lcd.print('SCAN [X]')
            lcd.print_line('SCANNING', line=2, align='CENTER')
            subprocess.run(['clamscan', '-r', '-i', usb_file_path])
            lcd.move_cursor(1, 12)
            lcd.print('SCAN [ ]')
            
            if usb_key == 1:
                try:
                    subprocess.check_output("sudo umount " + usb_file_path, shell=True)
                    print("Unmount OK")
                except subprocess.CalledProcessError:
                    print("Unmount Err")

            lcd.print_line('SCAN DONE!', line=2, align='CENTER')
            time.sleep(5)
            lcd.print_line('REMOVE USB', line=2, align='CENTER')
        update_time_temp -= 1
        time.sleep(1)
    else:
        update_main()
        draw()
        update_time_temp = update_time
