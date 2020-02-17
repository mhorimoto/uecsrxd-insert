#! /usr/bin/env python3
#coding: utf-8
#
# Ver: 0.08
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


################################################################
#
#
#
################################################################

fname ="/var/log/uecs/{0}".format(args[1])
max_lines = sum(1 for line in open(fname))
print("Filename={0}  Max Lines={1}".format(fname,max_lines))

with get_connection() as db:
    with db.cursor() as cur:
        lc = 1
        with open(fname,'r',encoding='utf_8') as f:
            for linebuf in f:
                line = linebuf.strip()
                if (line==''):
                    print("NULL Line exception at {0}".format(lc))
                    lc += 1
                    continue
                v = {}
                try:
                    (tod,xmline) = line.split(' ',1)
                except:
                    print("\nSPLIT exception at {0}".format(lc))
                    lc += 1
                    continue
                tod = tod.replace('-',' ')
                try:
                    root = ET.fromstring(xmline)
                except:
                    print("XML Decode exception at {0}".format(lc))
                    lc += 1
                    continue
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
                if ((lc%1000)==0):
                    print("Status={0:>5.1f}%".format((lc/max_lines)*100),end='\r')
                lc += 1
print("\n{0} lines finish".format(lc-1))
quit()
