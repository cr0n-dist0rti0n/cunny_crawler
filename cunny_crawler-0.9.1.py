import nmap
from ipwhois import IPWhois
from generate_ip import ipPick
from pprint import pprint
import warnings
import time
import threading
import os
import signal

warnings.filterwarnings("ignore")

nm = nmap.PortScanner()

os.system('clear')
print('Welcome to Cunny_Crawler. \n\n')
print('You might want to be carful with this program. Possibly don\'t use it. Possibly get behind a VPN. Possibly go to prison. This program is for educational purposes only. In fact its simplistic and stupid so you might want to build something else. On the otherhand its simple and effective. \n\n')
starting_port = int(input('Please enter starting port: '))
finishing_port = int(input('Please enter finishing port: '))
finishing_port += 1
print('\n\n<<<<<<<<<<<<<>>>>>>>>>>>>>\n\n')
print("Please wait...")

class Cunny_Scanner(object):
    
    def __init__(self, s_port, f_port):
        self.s_port = s_port
        self.f_port = f_port
        self.r_port = str(s_port)+'-'+str(f_port)    
    
    def interface(self):
        while True:
            os.system('clear')
            print('User Interface:\n\n')
            user_input = input('1. View number of IPs that have been scanned\n2. Current IP\n3. Exit program\n\nUser Choice: ')
            if user_input == '1':
                try:
                    print('\nThere have been ' + str(self.ips_got) + ' scanned.')
                    input('\nPress enter to continue')
                except AttributeError:
                    print('\nNo IPs have been discovered yet.\n')
                    input('\nPress enter to continue')
                    print('\n\nThinking...')
            elif user_input == '2':
                try:
                    print('\n\n'+self.ip)
                    input('\nPress enter to continue')
                except AttributeError:
                    print('\nNo IPs have been discovered yet.\n')
                    input('\nPress enter to continue')
                    print('\n\nThinking...')                    
            elif user_input == '3':
                print('Program now exiting')
                os.kill(os.getppid(), signal.SIGHUP)
            else:
                print('Please choose a vaild choice')
                
                
    def scanner(self):
        self.ips_got = 0
        while True:
            self.ip = (ipPick())
            self.ips_got += 1
            self.scanned = nm.scan(self.ip, self.r_port, '-T4 -sV --version-all')
            x = 1
            self.ssh_result = open("cunny_scan_results.txt", "a+")
            self.whois = IPWhois(self.ip)
            self.ssh_result.write('\n\n\n*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-\n\n\n')
            self.ssh_result.write('Results for ' + self.ip + '\n\n')
            self.whois_result = self.whois.lookup_rdap(depth=0)
            pprint(self.whois_result, self.ssh_result) 
            self.ssh_result.write('<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>\n\n')
            while (x == 1):
                for i in range (self.s_port, self.f_port):
                    try:
                        ssh_check = self.scanned['scan'][self.ip]['tcp'][i]['name']
                        port_check = self.scanned['scan'][self.ip]['tcp'][i]['state']
                        self.ssh_result.write(self.ip + ': Port ' + str(i) + ' is ' + ssh_check)
                        if port_check == str('open') or str('filtered'):
                            self.ssh_result.write(str(i) + ' is ' + port_check)
                        else:
                            pass
                    except KeyError:
                        pass                        
                    if i == self.f_port-1:
                        x = 0
            self.ssh_result.close()
            
            
cunny_scanner = Cunny_Scanner(starting_port, finishing_port)
interface = threading.Thread(name='interface', target=cunny_scanner.interface)
scanner = threading.Thread(name='scanner', target=cunny_scanner.scanner)
scanner.start()
interface.start()