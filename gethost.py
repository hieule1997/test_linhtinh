import netifaces as ni
ni.ifaddresses('wlp2s0')
ip = ni.ifaddresses('wlp2s0')[ni.AF_INET][0]['addr']
print (ip)