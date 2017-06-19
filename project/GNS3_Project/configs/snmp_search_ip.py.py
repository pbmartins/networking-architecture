import argparse
import socket
import sys
from pysnmp.hlapi import *

def snmp(addr=None):
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
                                      # Get interface ip
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
                    # Extract interface's values
                    interface_name = varBinds[0][1].prettyPrint()
                    interface_idx = varBinds[0][0].prettyPrint().split('.')[-1]
                    
                    # Build interfaces map with indexes
                    interfaces[interface_idx] = interface_name
                    
                    # Search for valid ips 
                    objects = varBinds[1][0].prettyPrint().split('mib-')[1].split('.')
                    if(objects[4] != '2'):
                        continue
                    
                    # Parse ip and interface index
                    interface_ip_addr = varBinds[1][0].prettyPrint().split('20.1.2.')[1]
                    if(interface_ip_addr == addr):
                        idx = varBinds[1][1].prettyPrint()
            
            # Print interface name
            if (idx != -1):
                print(name + " ON " + interfaces[idx])
                return
        
        print('IPv4 not found!')

"""
Validate an IPv4 address
"""
def is_valid_ipv4_address(address):
        try:
            socket.inet_pton(socket.AF_INET, address)
        except AttributeError:
            try:
                socket.inet_aton(address)
            except socket.error:
                return False
            return address.count('.') == 3
        except socket.error:
            return False

        return True

if __name__ == "__main__":        
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', help='An IPv4 address to search')
    args = parser.parse_args()
    
    # Search for a (valid) interface's IPv4 with SNMP
    if(is_valid_ipv4_address(args.ip)):
        snmp(args.ip)
    else:
        sys.stderr.write('Invalid IPv4!\n')