import sys
from pysnmp.hlapi import *
from pysnmp import debug

# Code largely taken from pySNMP documentation
# Find at https://pysnmp.readthedocs.io/en/latest/index.html 
# Copyright (c) 2005-2019, Ilya Etingof <etingof@gmail.com> All rights reserved.
# Modifications made by JD Black (c) 2022, 
# For use by American Electric Power, its subsidiaries and others authorized


#These get pasted directly in, they aren't strings
#The documentation lies to you, only use these ones
#List of acceptable auth protocol objects:
#   usmNoAuthProtocol (default is authKey not given)
#   usmHMACMD5AuthProtocol - MD5
#   usmHMACSHAAuthProtocol - SHAv1
#   usmHMAC128SHA224AuthProtocol - SHAv2 224bit
#   usmHMAC192SHA256AuthProtocol - SHAv2 256bit
#   usmHMAC256SHA384AuthProtocol - SHAv2 384bit
#   usmHMAC384SHA512AuthProtocol - SHAv2 512bit

#List of acceptable message encyption objects:
#   usmNoPrivProtocol (default is privhKey not given)
#   usmDESPrivProtocol (default if privKey is given)
#   usm3DESEDEPrivProtocol - 3DES
#   usmAesCfb128Protocol - AES 128
#   usmAesCfb192Protocol - AES 192
#   usmAesCfb256Protocol - AES 256

# A note on varBinds:
#  >varBinds is how we get data out 
#  >varBinds is a list containing a tuple containing an "ObjectIdentity"
#   and an optional value string. 
#   An ObjectIdentity is modeled as a pair of strings, 
#   one being the address of the value in the MIB Tree,
#   and the other being it's human readable name
#   ex: List( ObjectType( Object Identity('1.3.6.1.2.1.1.5.0', 'sysName'),
#  'oh850labise-2960x-sw1.aepsc.com'))

# Takes a generator object, grabs the first value, checks for errors,
# and either prints it or returns it based on the value of toPrint.
#   > For future reference, this doesn't have to be a different function
def nextVal(iterator, toPrint):
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
            return 'otherError'

    elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    elif not toPrint:
        try:    
            return str(varBinds[0][1])
        except IndexError:
            return 'authError'
    else:
        print(varBinds[0])

def newUserDatav3(oid, ip, authProtocolIn, privProtocolIn, 
    userIn, authPassIn, privPassIn, toPrint):
     return UsmUserData(
            userName= userIn,           #username
            authKey= authPassIn,         #authentication password
            privKey= privPassIn,         #encryption password
            authProtocol= authProtocolIn,
            privProtocol= privProtocolIn,
        )

#   Gets the value of a single MIB based on provided parameters
#   getMIB(String oid, String ip, Object authProtocolIn, Object privProtocolIn
#           String userIn, String authPassIn, String privPassIn, int toPrint)
#       > See above for possible values of authProtocolIn and privProtocolIn
#       > If toPrint !=, function will print output for you
#       > Returns varBinds object
def getOnev3(oid, ip, authProtocolIn, privProtocolIn, userIn, authPassIn, privPassIn, toPrint):
    iterator = getCmd(
        SnmpEngine(),
        UsmUserData(
            userName= userIn,           #username
            authKey= authPassIn,         #authentication password
            privKey= privPassIn,         #encryption password
            authProtocol= authProtocolIn,
            privProtocol= privProtocolIn,
        ),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    return nextVal(iterator, 0)

# Sets the value located at oid to newVal
def setOnev3(newVal, oid, ip, authProtocolIn, privProtocolIn, 
    userIn, authPassIn, privPassIn, toPrint):
    iterator = setCmd(
        SnmpEngine(),
        UsmUserData(
            userName= userIn,           #username
            authKey= authPassIn,         #authentication password
            privKey= privPassIn,         #encryption password
            authProtocol= authProtocolIn,
            privProtocol= privProtocolIn,
        ),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid), OctetString(newVal)),
    )
    nextVal(iterator, toPrint)

#   Below this nothing works. Perhaps nothing will ever work. 
#   Perhaps all hope is lost and we lay adrift in an infinite sea of
#   poor documentation and suffering.
def getWalkv3(ip, authProtocolIn, privProtocolIn, userIn, authPassIn, privPassIn):
    iterator = getCmd(
        SnmpEngine(),
        UsmUserData(
            userName= userIn,           #username
            authKey= authPassIn,         #authentication password
            privKey= privPassIn,         #encryption password
            authProtocol= authProtocolIn,
            privProtocol= privProtocolIn,
        ),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysContact'))
    )
    

    for errorIndication, errorStatus, errorIndex, varBinds in iterator:

        if errorIndication:
            print(errorIndication)
            break

        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            break

        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))


            

        
 


