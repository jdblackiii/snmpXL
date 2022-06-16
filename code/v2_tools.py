
import sys
from pysnmp.hlapi import *
from pysnmp import debug
from v3_tools import *

# Code largely taken from pySNMP documentation
# Find at https://pysnmp.readthedocs.io/en/latest/index.html 
# Copyright (c) 2005-2019, Ilya Etingof <etingof@gmail.com> All rights reserved.
# Modifications made by JD Black (c) 2022, 
# For use by American Electric Power, its subsidiaries and others authorized


def getOnev2(communityString, ip, oid, toPrint):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(communityString),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
    )   
    return nextVal(iterator, toPrint)

def setOnev2(newVal, communityString, ip, oid, toPrint):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(communityString),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid), OctetString(newVal)),
    )   
    nextVal(iterator, toPrint)

#here be dragons
def getWalkv2(communityString, ip, oid):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(communityString),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.6.0'))
    )   
    for errorIndication, errorStatus, errorIndex, varBinds in iterator:
        if errorIndication:
            print(errorIndication)

        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))