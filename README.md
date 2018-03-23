# Raspberry setup

1. Install raspbian strech (March 2018)
2. Set up new pwd
3. sudo raspi-config:
	- change locale
	- change time-zone
	- enable SSH
	- expand file-system
4. sudo apt-get update
5. sudo apt-get upgrade

# Service

1. sudo nano /etc/init.d/goTarino
2. sudo chmod 755 /etc/init.d/goTarino
3. sudo /etc/init.d/goTarino {start|stop}

# Python

1. sudo apt-get install python3-pip
2. sudo pip3 install requests
3. sudo pip3 install asyncio
4. sudo pip3 install pyserial
5. sudo pip3 install json

