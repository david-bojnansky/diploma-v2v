# V2V komunikácia použitím minipočítača Raspberry Pi

Diplomová práca (c) 2020 Bojnanský Dávid

## Minimálne požiadavky

- Počítač, nainštalovaný webový prehliadač a nainštalované programy [7-Zip](https://www.7-zip.org/) a [balenaEtcher](https://www.balena.io/etcher/)
- Sieťový LAN kábel napojený do routra s prístupom na internet
- Dva minipočítače Raspberry Pi 3 Model B
- Dve micro SD karty o veľkosti 8 GB (s adaptérom pre počítač)
- Napájací adaptér pre minipočítač
- USB klávesnica a USB myš
- Veľký monitor s HDMI konektorom a HDMI kábel
- Prenosný HDMI displej pre minipočítač s potrebnými káblami
- Dva OBD skenery (nie každý funguje s týmto programom), napr. [OBD Scan](https://www.ebay.com/itm/Vgate-ELM327-Bluetooth-OBD2-V2-1-Scanner-Car-Auto-Diagnostic-Adapter-Scan-Tool/123778992357)
- Dve vozidlá s OBD konektormi
- Dve micro USB auto-nabíjačky

## Postup spustenia programu v praxi
- Stiahnúť .zip archív [Raspbian Buster with desktop and recommended software](https://www.raspberrypi.org/downloads/raspbian/)
- Rozbaliť .zip archív pomocou 7-Zip
- Zapísať .img na micro SD kartu podľa oficiálneho [návodu](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)
- Zapnúť minipočítač (vrátane napojenia LAN kábla)
- Nakonfigurovať OS 
- Spustiť terminál
- Zmeniť názov počítača (napríklad na rpi-1, rpi-2, ...): `sudo nano /etc/hostname`
- Aktualizovať repozitáre: `sudo apt-get update`
- Aktualizovať knižnice: `sudo apt-get upgrade`
- Zmeniť aktuálny pracovný priečinok: `cd /home/pi/Desktop`
- Naklonovať projekt: `git clone https://github.com/david-bojnansky/diploma-v2v.git v2v` (pred tým však môže vyžadovať základnú konfiguráciu git-u)
- Zmeniť aktuálny pracovný priečinok: `cd v2v`
- Spustiť inštalačný skript: `sudo ./install`
- Prepísať informácie o vozidle (MAC adresa OBD skenera, PIN kód OBD skenera pre Bluetooth párovanie, značka vozidla, model vozidla, EČV): `nano vehicleinfo.txt`
- Opraviť IP adresu: `nano etc-network-interfaces.d/bat0`
- Vypnúť
- Vložiť OBD skener do OBD konektora vo vozidle
- Naštartovať vozidlo
- Pripojiť displej a zapnúť minipočítač
- Spustiť terminál
- Zmeniť aktuálny pracovný priečinok: `cd /home/pi/Desktop/v2v`
- Zahájiť Bluetooth párovanie s OBD skenerom: `./obd2rpi/pairwithobd`
- Reštartovať minipočítač: `sudo reboot`
- Po reštartovaní by sa do minúty malo ukázať grafické rozhranie
- Systém beží

## Materiály
https://python-obd.readthedocs.io/en/latest/
sudo pip3 install https://github.com/brendan-w/python-OBD/archive/master.zip --upgrade

https://github.com/brendan-w/python-OBD
https://github.com/brendan-w/python-OBD/issues/160
https://github.com/brendan-w/python-OBD/pull/162
https://github.com/brendan-w/python-OBD/pull/162/files






https://medium.com/@tdoll/how-to-setup-a-raspberry-pi-ad-hoc-network-using-batman-adv-on-raspbian-stretch-lite-dce6eb896687
https://medium.com/@tdoll/how-to-setup-a-raspberry-pi-ad-hoc-network-using-batman-adv-on-raspbian-stretch-lite-dce6eb896687
https://medium.com/@tdoll/how-to-setup-a-raspberry-pi-ad-hoc-network-using-batman-adv-on-raspbian-stretch-lite-dce6eb896687

https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-from-nic-in-python
sudo pip3 install netifaces


Netreba:
https://gist.github.com/ninedraft/7c47282f8b53ac015c1e326fffb664b5



https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/






Netreba:
sudo apt-get install python3-dev libbluetooth-dev bluez?
sudo pip3 install pybluez


Nezabudni na services:
/lib/systemd/system/v2v-client.service
/lib/systemd/system/v2v-server.service




BLUETOOTH:

Pre spúšťací súbor pairwithobd
sudo apt-get install expect
https://askubuntu.com/questions/763939/bluetoothctl-what-is-a-bluetooth-agent

Bluetooth Manager GUI:
sudo apt-get install blueman

Bluetooth Libs:
sudo apt-get install bluez
