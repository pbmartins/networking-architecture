import socket
import argparse
import re
import sys
from pysnmp.hlapi import *

def main(addr=None):
        # List of snmp agent's ips
        ips = {
                'ISP1_PT_R1'          : '200.1.0.125',
                'ISP2_PT_R1'          : '200.1.0.126',
                'Aveiro_Core_A'       : '10.17.3.33',
                'Aveiro_Core_B'       : '10.17.3.41',
                'Datacenter_Aveiro_1' : '200.1.0.62',
                'Datacenter_Aveiro_2' : '200.1.0.61',
                'Aveiro_E1_Dist_B'    : '10.17.3.25',
                'Aveiro_E1_Dist_B'    : '10.17.3.26',
                'Aveiro_E0_Dist_A'    : '10.17.3.21',
                'Aveiro_E0_Dist_B'    : '10.17.3.22'
              }
        
        # Query all ips
        for name, ip in ips.items():
            idx = -1
            interfaces = {}
            for (errorIndication,
                 errorStatus,
                 errorIndex,
                 varBinds) in nextCmd(SnmpEngine(),
                                      CommunityData('public', mpModel=0),
                                      UdpTransportTarget((ip, 161)),
                                      ContextData(),
                                      # Get interface name
                                      ObjectType(ObjectIdentity('IF-MIB', 'ifDescr')),
                                      # Get interface's IPv4
                                      ObjectType(ObjectIdentity('1.3.6.1.2.1.4.20.1.1')),
                                      # Get interface's index
                                      ObjectType(ObjectIdentity('1.3.6.1.2.1.4.20.1.2')),
                                      lexicographicMode=False):
    
                if errorIndication:
                    print(errorIndication)
                    break
                elif errorStatus:
                    print('%s at %s' % (errorStatus.prettyPrint(), errorIndex 
                            and varBinds[int(errorIndex)-1][0] or '?'))
                    break
                else:
                    # Extract values from route and arp table
                    interface_name = varBinds[0][1].prettyPrint()
                    interface_ip_addr = varBinds[1][1].prettyPrint()
                    objects = str(varBinds[0][0]).split('.')
                    if (objects[-2] != 2):
                        interfaces[objects[-1]] = interface_name
                    # Compare with searched ip or mac
                    if(interface_ip_addr == addr): 
                        # Save interface index
                        idx = varBinds[2][1].prettyPrint()
            if (idx != -1):
                print(name + " ON " + interfaces[idx])
                return

"""
Validate an IPv4 address
"""
def is_valid_ipv4_address(address):
        try:
                socket.inet_pton(socket.AF_INET, address)
        except AttributeError:    # no inet_pton here, sorry
                try:
                        socket.inet_aton(address)
                except socket.error:
                        return False
                return address.count('.') == 3
        except socket.error:    # not a valid address
                return False

        return True

if __name__ == "__main__":        
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', help='An IPv4 address to search')
    args = parser.parse_args()
    
    # Search for an (valid) interface's IPv4 with SNMP
    if(is_valid_ipv4_address(args.ip)):
        main(args.ip)
    else:
        sys.stderr.write('Invalid IPv4!\n')