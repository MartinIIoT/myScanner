#!/bin/bash
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

check_status() {
	echo "===  CHECK ONLINE  ==="
	wget -q --spider https://google.com
	if [ $? -eq 0 ];
	then return 0;
	else return 1;
	fi
	# 0 = true
	# 1 = false
}

status_av() {
	if sudo systemctl is-active --quiet clamav-freshclam;
	then echo -e "ClamAV Status: ${GREEN}Active${NC}";
	else echo -e "ClamAV Status: ${RED}Inactive${NC}";
	fi
}

run_update() {
	echo ""
	echo "===  OS Update ==="
	sudo apt full-upgrade -y

	echo ""
	echo "===  Cleaning OS  ==="
	sudo apt autoremove --purge -y
}

update() {
	echo "Status: on-line"
	echo ""
	echo "===  Search OS Updates  ==="
	sudo apt update

	run_update

	echo ""
	echo "===  Stop ClamAV  ==="
	sudo systemctl stop clamav-freshclam
	status_av

	echo ""
	echo "===  Update ClamAV  ==="
	sudo freshclam

	echo ""
	echo "===  Start ClamAV  ==="
	sudo systemctl start clamav-freshclam
	stav_av
}

if check_status;
then update;
fi
