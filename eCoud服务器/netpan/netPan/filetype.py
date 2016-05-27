#!/usr/bin/env python
#-*-coding:utf8-*-
import struct  

def typeList():  
    return {
        "FFD8FF": "jpg",
        "89504E47": "png",
        "47494638": "gif",
        "424D": "bmp",
        "D0CF11E0": "xls.or.doc",
        "255044462D312E": "pdf",
        "504B0304140006": "docx.or.pptx",
        "D0CF11E0A1B11A": "ppt"
        }  
  
def bytes2hex(bytes):  
    num = len(bytes)  
    hexstr = u""  
    for i in range(num):  
        t = u"%x" % bytes[i]  
        if len(t) % 2:  
            hexstr += u"0"  
        hexstr += t  
    return hexstr.upper()  
  

def fileType(buf):  
    #print buf 
    tl = typeList()  
    ftype = 'unknown'  
    for hcode in tl.keys():
        numOfBytes = len(hcode) / 2 
        hbytes = struct.unpack_from("B"*numOfBytes,buf[0:numOfBytes])
        f_hcode = bytes2hex(hbytes)
        print f_hcode
        if f_hcode == hcode:
            ftype = tl[hcode]  
            break    
    print ftype
    return ftype  
  
if __name__ == '__main__':  
	binfile = open('4.docx','rb')
	buf = binfile.read()
	binfile.close()
	fileType(buf)
