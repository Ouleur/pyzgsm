#!/usr/bin/python
#-*- coding:utf8 -*-
import binascii


def toPDU(command):
    binaire=[format(ord(c),"07b")[::-1]for c in command]
    # print binaire
    binaire ="".join(binaire)
    binaire +='0'*(8-len(binaire)%8)
    # print binaire
    pdu = ""
    # print binaire
    while len(binaire)!=0:
        symbole = binaire[:8]
        # print symbole
        symbole =  symbole[::-1]
        binaire = binaire[8:]
        # print len(binaire)
        pdu += str(binhex(symbole[:4]))+str(binhex(symbole[4:]))
        # print pdu
    return pdu

def toText(pdumsg):
    # print pdumsg
    pdu = binascii.unhexlify(pdumsg)
    # pdu = pdumsg.decode('hex')
    # print pdu
    binaire = [format(ord(c),"08b")[::-1]for c in pdu]
    # print binaire
    binaire ="".join(binaire)
    hexe = ""

    while len(binaire)>=7:
        symbole = binaire[:7]
        binaire = binaire[7:]

        symbole = "0"+symbole[::-1]
        hexe+=str(binhex(symbole[:4]))+str(binhex(symbole[4:]))     

    return binascii.unhexlify(hexe)
    # return hexe.decode('hex')

def bin2dec(string):
    result = 0
    for car in string:
        result *= 2
        if car == '1':
            result += 1
        elif car == '0':
            pass
        else:
            return None
    return result

def dec2hex(n):
    return hex(n).split('x')[1]

def binhex(binaire):
    return dec2hex(bin2dec(binaire)).upper()

print toPDU("#99#")

# prioText("C274D96D2FBBEB65D0BC2E073DE561F7B90C6ABEDDE5BC22A62B9ACDE531BD5E9683EA6E10B90C7FD341E453587E2EBBE90A99AE683697C7F47A590EAABB41F2325D1E4ED341E453587E2EBBE98A998E2A0FBBE7E6B29C0E229FC2F273D94D57D074D070BADC2EBBE9207219640E8FE975795951D33DE561F7B90C1ABED9ECF2985E56D8744F383DFD76CF1B")
#print dec2hex(49)

# print toText("CD69724A74EA1A3259AD76C3C162B09C0D")