# V2V komunikácia použitím minipočítača Raspberry Pi

Diplomová práca (c) 2020 Bojnanský Dávid

## Textové dokumenty

-  [Diplomová práca vo formáte PDF](https://github.com/david-bojnansky/diploma-v2v/blob/master/thesis/V2V%20komunik%C3%A1cia%20pou%C5%BEit%C3%ADm%20minipo%C4%8D%C3%ADta%C4%8Da%20Raspberry%20Pi.pdf)

## Praktické ukážky

- [Playlist videí](https://www.youtube.com/playlist?list=PLTxJhgGv-fMB8rF7z0QGvksdUlAue43B_)
- [Vozidlá idúce za sebou I.](https://youtu.be/kq7yeCqjYpg)
- [Vozidlá idúce za sebou II.](https://youtu.be/ZFmHJJL8_uo)
- [Dosah signálu](https://youtu.be/NyofHGUne5c)
- [Vozidlá, ktoré sa míňajú](https://youtu.be/ac9dYk9JT6I)
- [Automatický reštart systému](https://youtu.be/rrhvNowX0fs)

## Minimálne požiadavky

- Počítač, nainštalovaný webový prehliadač a nainštalované programy typu [7-Zip](https://www.7-zip.org/) a [balenaEtcher](https://www.balena.io/etcher/)
- Sieťový LAN kábel napojený do routra s prístupom na internet
- Dva minipočítače Raspberry Pi 3 Model B
- Dve pamäťové microSD karty o veľkosti 8 GB (s adaptérom pre počítač)
- Napájací adaptér pre minipočítač do elektrickej zásuvky
- USB klávesnica a USB myš
- Veľký monitor s HDMI vstupom a HDMI kábel
- Prenosný HDMI displej pre minipočítač s potrebnými káblami
- Dva OBD-II skenery ako napríklad [OBD Scan](https://www.ebay.com/itm/Vgate-ELM327-Bluetooth-OBD2-V2-1-Scanner-Car-Auto-Diagnostic-Adapter-Scan-Tool/123778992357)
- Dve vozidlá s OBD-II konektormi
- Dva microUSB napájacie adaptéry kompatibilné so zapaľovaním vo vozidle

## Postup spustenia V2V systému

- Stiahnúť .zip archív [Raspbian Buster with desktop and recommended software](https://www.raspberrypi.org/downloads/raspbian/)
- Rozbaliť .zip archív pomocou 7-Zip
- Zapísať .img na pamäťovú microSD kartu podľa oficiálneho [návodu](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)
- Zapnúť minipočítač (vrátane pripojeného LAN kábla a pripojených periférnych zariadení)
- Preklikať sa inštalačnými nastaveniami pri úplne prvom spustení
- Spustiť príkazový riadok
- Zmeniť názov počítača (napríklad na rpi-1, rpi-2, ...): `sudo nano /etc/hostname`
- Zmeniť aktuálny pracovný adresár: `cd /home/pi/Desktop`
- Naklonovať Git projekt: `git clone https://github.com/david-bojnansky/diploma-v2v.git v2v`
- Zmeniť aktuálny pracovný adresár: `cd v2v`
- Spustiť inštalačný skript: `sudo ./install`
- Prepísať informácie o vozidle: `nano vehicleinfo.txt`
    - MAC adresa OBD-II skenera
    - Párovací Bluetooth kód
    - Značka vozidla
    - Model vozidla
    - Evidenčné číslo vozidla
- Prideliť IP adresu: `nano etc-network-interfaces.d/bat0`
- Vypnúť minipočítač: `sudo shutdown now`
- Vložiť OBD-II skener do OBD-II konektora vo vozidle
- Naštartovať vozidlo
- Pripojiť displej k minipočítaču ako aj ostatné periférne zariadenia
- Zapnúť minipočítač
- Spustiť príkazový riadok
- Zmeniť aktuálny pracovný adresár: `cd /home/pi/Desktop/v2v`
- Zahájiť Bluetooth párovanie s OBD-II skenerom: `./obd2rpi/pairwithobd`
- Reštartovať minipočítač: `sudo reboot`
- Po reštartovaní sa do minúty ukáže grafické rozhranie
- Systém beží...
- *Postup zopakovať pre ďalšie vozidlo*
