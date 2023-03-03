import subprocess
import i2clcd
import urllib.request
import time
import os

lcd = i2clcd.i2clcd(i2c_bus=1, i2c_addr=0x27, lcd_width=20)
lcd.init()

usb_kluc = 0
usb_cesta = "/dev/sda1"
usb_file_cesta = "/home/pi/myScanner/myUSB/"
usb_scanned = False
cas_aktualizacie = 30 # v sekundach
cas_aktualizacie_temp = cas_aktualizacie

def aktualizuj():
    lcd.clear()
    lcd.print_line('CHECK UPDATE', line=0, align='CENTER')
    
    try:
        
        urllib.request.urlopen('https://google.com', timeout=5) #Python 3.x
        lcd.print_line(':::  ONLINE  :::', line=2, align='CENTER')
        lcd.print_line('UPDATING', line=3, align='CENTER')
        subprocess.run(['./aktualizuj.sh'])
        lcd.clear()
        return True
    except:
        lcd.print_line('...  OFFLINE  ...', line=2, align='CENTER')
        time.sleep(1)
        lcd.clear()
        return False


def hladaj_kluc():
    global usb_kluc
    global usb_scanned

    if os.path.exists(usb_cesta) and usb_kluc == 0:
        try:
            subprocess.check_output("sudo mount " + usb_cesta + " " + usb_file_cesta, shell=True)
            #subprocess.run(['sudo', 'mount', usb_cesta, usb_file_cesta])
            usb_kluc = 1
            print("Mount OK")
            time.sleep(1)
        except subprocess.CalledProcessError:
            print("Mount Err")
            usb_kluc = 0

        lcd.move_cursor(1, 0)
        lcd.print("USB [X]")
        time.sleep(1)
        return True
    elif not(os.path.exists(usb_cesta)) and usb_kluc == 1:
        lcd.print_line('', line=2, align='CENTER')
        lcd.move_cursor(1, 0)
        lcd.print("USB [ ]")
        usb_kluc = 0
        usb_scanned = False
        return False

def vykreslit():
    lcd.print_line('===  MartinIIoT  ===', line=0, align='CENTER')
    lcd.move_cursor(1, 0)
    lcd.print("USB [ ]")
    lcd.move_cursor(1, 12)
    lcd.print('SCAN [ ]')

    verzia_raw = subprocess.run(['clamscan', '--version'], stdout=subprocess.PIPE)
    verzia_help = verzia_raw.stdout.decode('utf-8')

    verzia_core = verzia_help[7:verzia_help.find('/')]
    verzia_db = verzia_help[verzia_help.find('/')+1:verzia_help.rfind('/')]

    lcd.move_cursor(3, 0)
    lcd.print(verzia_core)

    lcd.move_cursor(3, 15)
    lcd.print(verzia_db)

aktualizuj()
vykreslit()

while True:
    if cas_aktualizacie_temp > 0:
        if hladaj_kluc() and not(usb_scanned):
            usb_scanned = True
            lcd.move_cursor(1, 12)
            lcd.print('SCAN [X]')
            lcd.print_line('SCANNING', line=2, align='CENTER')
            #subprocess.run(['clamscan', '-r', '-i', usb_cesta], stdout=subprocess.PIPE)
            subprocess.run(['clamscan', '-r', '-i', usb_file_cesta])
            lcd.move_cursor(1, 12)
            lcd.print('SCAN [ ]')
            
            if usb_kluc == 1:
                try:
                    subprocess.check_output("sudo umount " + usb_file_cesta, shell=True)
                    #subprocess.run(['sudo', 'umount', usb_file_cesta])
                    print("Unmount OK")
                except subprocess.CalledProcessError:
                    print("Unmount Err")

            lcd.print_line('SCAN DONE!', line=2, align='CENTER')
            time.sleep(5)
            lcd.print_line('REMOVE USB', line=2, align='CENTER')
        cas_aktualizacie_temp -= 1
        time.sleep(1)
    else:
        aktualizuj()
        vykreslit()
        cas_aktualizacie_temp = cas_aktualizacie
