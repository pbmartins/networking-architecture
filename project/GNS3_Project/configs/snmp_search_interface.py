import argparse
import sys
from pysnmp.hlapi import *

def snmp(interface=None, ip=None):
    idx = -1
    ips = {}
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
            # Extract values from interface description
            interface_name = varBinds[0][1].prettyPrint()
            interface_idx = str(varBinds[0][0]).split('.')[-1]
            
            # Find searched interface's idx
            if (interface_name == interface):
                idx = interface_idx
            
            # Search for valid ip's
            objects = varBinds[1][0].prettyPrint().split('mib-')[1].split('.')
            if(objects[4] != '2'):
                continue

            # Build ip's map with index
            interface_ip_addr = varBinds[1][0].prettyPrint().split('20.1.2.')[1]
            int_idx = varBinds[1][1].prettyPrint()
            ips[int_idx] = interface_ip_addr

    # Print result
    if (idx != -1 and idx in ips.keys()):
        print(interface + " has " + ips[idx])
    else:
        print(interface + " has no IPv4")

if __name__ == "__main__":        
    # SNMP agent's ips
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
    
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('equipment_name', help='Equipment name . Ex : ISP1_PT_R1')
    parser.add_argument('interface_name', help="Equipment's interface name. Ex: FastEthernet0/0")
    args = parser.parse_args()
  
    # Search for interface's ip  
    if (args.equipment_name in ips.keys()):
        snmp(args.interface_name, ips[args.equipment_name])
    else:
        sys.stderr.write('Invalid equipment name!\n')