# pylint: disable=missing-module-docstring, missing-function-docstring
import subprocess
import urllib.request
import time
import os
import i2clcd

# LCD 20x4 Setup:
#   Address: 27 on I2C
#   LCD_WIDTH: 20 for 20x4
lcd = i2clcd.i2clcd(i2c_bus=1, i2c_addr=0x27, lcd_width=20)
lcd.init()

USB_KEY = 0
USB_PATH = "/dev/sda1"  # Where is USB
USB_FILE_PATH = "/home/pi/myScanner/myUSB/"  # Mount point for USB
USB_SCANNED = False
UPDATE_REFRESH_TIME = 30  # in seconds
UPDATE_TIME_TEMP = UPDATE_REFRESH_TIME
START_UPDATE = 1800  # in seconds (1800s = 30min)


# Save last update timestamp to ./last_update.conf
def save_last_update():
    lcd.clear()
    with open('./last_update.conf', 'w', encoding='utf-8') as my_file:
        lcd.print_line('SAVE LAST UPDATE', line=2, align='CENTER')
        date_time_now = str(time.time())
        my_file.write(date_time_now)
        lcd.clear()


# Read last timestamp update.
# If is more as START_UPDATE variable then start update.
def read_last_update():
    global START_UPDATE

    with open('./last_update.conf', 'r', encoding='utf-8') as my_file:
        update_now = False
        date_time_old = float(my_file.read())
        date_time_now = time.time()
        if date_time_now - date_time_old >= START_UPDATE:
            update_now = True

    if update_now:
        update_os()
        clamav_update()
        save_last_update()


# Update ClamAV definitions database
def clamav_update():
    lcd.clear()
    lcd.print_line('CHECK UPDATE', line=0, align='CENTER')
    lcd.print_line('STOP ClamAV', line=2, align='CENTER')
    subprocess.run(['sudo', 'systemctl', 'stop', 'clamav-freshclam'], check=False)
    lcd.print_line('UPDATE ClamAV', line=2, align='CENTER')
    subprocess.run(['sudo', 'freshclam'], check=False)
    lcd.print_line('START ClamAV', line=2, align='CENTER')
    subprocess.run(['sudo', 'systemctl', 'start', 'clamav-freshclam'], check=False)
    lcd.clear()


# Update Ubuntu and clean Ubuntu after update
def update_os():
    lcd.clear()
    lcd.print_line('CHECK UPDATE', line=0, align='CENTER')
    lcd.print_line('GET OS UPDATE', line=2, align='CENTER')
    subprocess.run(['sudo', 'apt', 'update'], check=False)
    lcd.print_line('OS UPDATING', line=2, align='CENTER')
    subprocess.run(['sudo', 'apt', 'full-upgrade', '-y'], check=False)
    lcd.print_line('CLEAN OS', line=2, align='CENTER')
    subprocess.run(['sudo', 'apt', 'autoremove', '--purge', '-y'], check=False)
    lcd.clear()


# Main update function.
# Check if have internet connection and if yes, start read_last_update()
def update_main():
    try:
        with urllib.request.urlopen('https://google.com', timeout=5):
            lcd.clear()
            read_last_update()
            return True
    except urllib.error.URLError:
        time.sleep(1)
        lcd.clear()
        return False


# Check if is USB present and if yes, mount it to ./myUSB/
def find_usb():
    global USB_KEY
    global USB_SCANNED

    if os.path.exists(USB_PATH) and USB_KEY == 0:
        try:
            subprocess.check_output("sudo mount " + USB_PATH + " " + USB_FILE_PATH, shell=True)
            USB_KEY = 1
            print("Mount OK")
            lcd.move_cursor(1, 0)
            lcd.print("USB [X]")
            time.sleep(1)
            return True
        except subprocess.CalledProcessError:
            print("Mount Err")
            USB_KEY = 0
            return False

    if not os.path.exists(USB_PATH) and USB_KEY == 1:
        lcd.print_line('', line=2, align='CENTER')
        lcd.move_cursor(1, 0)
        lcd.print("USB [ ]")
        USB_KEY = 0
        USB_SCANNED = False
        return False

    return None


# Draw main screen with ClamAV Core and definitions database versions
def draw():
    lcd.clear()
    lcd.print_line('===  MartinIIoT  ===', line=0, align='CENTER')
    lcd.move_cursor(1, 0)
    lcd.print("USB [ ]")
    lcd.move_cursor(1, 12)
    lcd.print('SCAN [ ]')

    version_raw = subprocess.run(['clamscan', '--version'], check=False, stdout=subprocess.PIPE)
    version_help = version_raw.stdout.decode('utf-8')

    version_core = version_help[7:version_help.find('/')]
    version_db = version_help[version_help.find('/') + 1:version_help.rfind('/')]

    lcd.move_cursor(3, 0)
    lcd.print(version_core)

    lcd.move_cursor(3, 15)
    lcd.print(version_db)


# Initial run
update_main()
draw()

# Main loop for running program
while True:
    if UPDATE_TIME_TEMP > 0:
        if find_usb() and not USB_SCANNED:
            USB_SCANNED = True
            lcd.move_cursor(1, 12)
            lcd.print('SCAN [X]')
            lcd.print_line('SCANNING', line=2, align='CENTER')
            subprocess.run(['clamscan', '-r', '-i', USB_FILE_PATH], check=False)
            lcd.move_cursor(1, 12)
            lcd.print('SCAN [ ]')

            if USB_KEY == 1:
                try:
                    subprocess.check_output("sudo umount " + USB_FILE_PATH, shell=True)
                    print("Unmount OK")
                except subprocess.CalledProcessError:
                    print("Unmount Err")

            lcd.print_line('SCAN DONE!', line=2, align='CENTER')
            time.sleep(5)
            lcd.print_line('REMOVE USB', line=2, align='CENTER')

        UPDATE_TIME_TEMP -= 1
        time.sleep(1)
    else:
        update_main()
        draw()
        UPDATE_TIME_TEMP = UPDATE_REFRESH_TIME
