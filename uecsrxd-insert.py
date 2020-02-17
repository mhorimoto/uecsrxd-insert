#! /usr/bin/env python3
#coding: utf-8
#
# Ver: 0.03
# Date: 2020/02/17
# Author: horimoto@holly-linux.com
#
import sys
import datetime
import time
import configparser
import xml.etree.ElementTree as ET
import psycopg2

def get_connection():
    return psycopg2.connect("user=uecs0 dbname=uecs0 password=UECS0")

args = sys.argv
if ( args[1] == '' ):
    quit()

with get_connection() as db:
    with db.cursor() as cur:
        fname ="/var/log/uecs/{0}".format(args[1])
        print("Filename={0}".format(fname))
        f = open(fname,'r')
        line = f.readline().strip()
        v = {}
        lc = 1
        while line:
            (tod,xmline) = line.split(' ',1)
            tod = tod.replace('-',' ')
            print("{0} ".format(lc),end='\r')
            try:
                root = ET.fromstring(xmline)
            except:
                print("Error lc={0}".format(lc))

            v['ver'] = root.attrib['ver']
            for c1 in root:
                sp = c1.tag
                v[sp] = c1.text
                for c2 in c1.attrib:
                    v[c2] = c1.attrib[c2]
            ptext = "{0},{1},{2},{3},{4},{5},{6},{7},{8}"\
                .format(tod,v['ver'],v['type'],v['room'],v['region'],v['order'],\
                        v['priority'],v['DATA'],v['IP'])
            cur.execute('INSERT INTO t_data (TOD,VER,CCMTYPE,ROOM,REGION,ORD,PRIORITY,VALUE,IP) VALUES \
            (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(tod,v['ver'],v['type'],v['room'],v['region'],v['order'],\
                                           v['priority'],v['DATA'],v['IP'],))
            line = f.readline().strip()
            lc = lc+1
        f.close()
        db.commit()
        cur.close()
        print("\n{0} lines finish".format(lc))
        quit()
