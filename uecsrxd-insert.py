#! /usr/bin/env python3
#coding: utf-8
#
# Ver: 0.01
# Date: 2020/02/16
# Author: horimoto@holly-linux.com
#
import datetime
import time
import configparser
import xml.etree.ElementTree as ET
import psycopg2

def get_connection():
    return psycopg2.connect("user=uecs0 dbname=uecs0 password=UECS0")

with get_connection() as db:
    with db.cursor() as cur:

        f = open('recvdata-sample.log','r')
        line = f.readline().strip()
        v = {}

        while line:
            (tod,xmline) = line.split(' ',1)
            tod = tod.replace('-',' ')
            root = ET.fromstring(xmline)
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
            print(ptext)
            line = f.readline().strip()
        f.close()
        db.commit()
        cur.close()
