#!/bin/bash
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

online_stav() {
	echo "===  Overujem online stav  ==="
	wget -q --spider https://google.com
	if [ $? -eq 0 ];
	then return 0;
	else return 1;
	fi
	# 0 = true
	# 1 = false
}

stav_av() {
	if sudo systemctl is-active --quiet clamav-freshclam;
	then echo -e "ClamAV Status: ${GREEN}Active${NC}";
	else echo -e "ClamAV Status: ${RED}Inactive${NC}";
	fi
}

spusti_aktualizaciu() {
	echo ""
	echo "===  Preberám aktualizácie OS ==="
	sudo apt full-upgrade -y

	echo ""
	echo "===  Čistím OS  ==="
	sudo apt autoremove --purge -y
}

aktualizuj() {
	echo "Stav: on-line"
	echo ""
	echo "===  Hľadám aktualizácie OS  ==="
	sudo apt update

	spusti_aktualizaciu

	echo ""
	echo "===  Zastavujem ClamAV  ==="
	sudo systemctl stop clamav-freshclam
	stav_av

	echo ""
	echo "===  Aktualizujem ClamAV  ==="
	sudo freshclam

	echo ""
	echo "===  Spúšťam ClamAV  ==="
	sudo systemctl start clamav-freshclam
	stav_av
}

if online_stav;
then aktualizuj;
fi
