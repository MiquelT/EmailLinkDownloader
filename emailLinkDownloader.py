
import xml.etree.ElementTree as ET
import imaplib
from datetime import datetime
import time
from dateutil import parser
import sys
from email.parser import HeaderParser
import urllib2
import os


user = None
password = None
mail = None
conf_SSL = None

labels = []
lastUpdates = {}



def read_config():

    global password
    global user
    global labels
    global conf_SSL
    global root
    global tree
    global path

    tree = ET.parse('config.xml')

    root = tree.getroot()

    user = root.find('email').find('auth').find('user').text
    password = root.find('email').find('auth').find('password').text

    conf_SSL = root.find('email').find('config').find('ssl').text


    for l in root.find('labels').findall('label'):
        labels.append(l.text)

    for l in root.find('lastDownloads').findall('timestamp'):
        lab = {l.attrib['name']:l.text}
        lastUpdates.update(lab)

    path = root.find('dir').text
    if path[-1:] != '/': path += '/'
    create_directory(path)




def create_directory(path):
    if not os.path.isdir(path):
        splitpath = path.split('/')
        completPath = ''
        for dir in splitpath:
            completPath += dir + '/'
            if not os.path.isdir(dir) and dir != "":
                os.makedirs(completPath)



def read_emails(lab,listaFinal):

    if lab in lastUpdates:
        gdate = lastUpdates[lab]
        gdate = float(gdate)
    else:
        gdate = float(0)


    mail.select(lab)
    print lab
    result, data = mail.search(None, "ALL")


    ids = data[0]
    id_list = ids.split()

    print len(id_list)

    for email_id in id_list:

        result, data = mail.fetch(email_id, "(RFC822)")

        header_data = data[0][1]

        parser = HeaderParser()
        msg = parser.parsestr(header_data)

        date = None
        try:
            fecha = msg['Date']
            date = tryGetfecha1(fecha)

        except:
            continue

        if date == None:
            continue

        fdate = 0.0
        try:
            fdate = float(time.mktime(date.timetuple()))
        except:
            continue


        if gdate < fdate:
            updateDate(lab,fdate)
            get_links(data[0][1],listaFinal)



def tryGetfecha1(fecha):
        date = parser.parse(fecha)
        return date


def get_links(data,listaFinal):
    asfields = str(data).split("<a");
    for a in asfields:

        link = ""
        if "href=" in a:
            linkList = a.split("\"")
            if len(linkList) > 1:
                link = linkList[1]
            else:
                linkList = a.split("\'")
                if len(linkList) > 1:
                    link = linkList[1]

        if 'http' in link and len(link.split(".")) > 1 and link not in listaFinal:
            listaFinal.append(link)








def updateDate(lab,date):
    timestamps = root.find('lastDownloads').findall('timestamp')

    if lab in lastUpdates:
        for t in timestamps:
            if t.get('name') == lab:
                t.text = str(date)
                tree.write('config.xml')
    else:
        a = ET.Element('timestamp')
        a.set('name',lab)
        a.text = str(date)
        root.find('lastDownloads').append(a)

        lab = {lab:str(date)}
        lastUpdates.update(lab)

        tree.write('config.xml')



def start_conexion():

    global mail

    mail = imaplib.IMAP4_SSL(conf_SSL)
    mail.login(user,password)




def download(fileUrl):
    print "Downloading: " + fileUrl
    file_name = fileUrl.split('/')[-1]
    u = urllib2.urlopen(fileUrl)
    f = open(path+file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()



def read_links(listaFinal):
    for l in listaFinal:
        try:
            final_l = ""
            for l2 in l.split():
                if l2[-1:] == '=':
                    l2 = l2[:-1]
                final_l += l2

            l =  final_l
            if l[-1:] == '=':
                l = l[:-1]

            download(l)
        except:
            continue





if __name__ == "__main__":
    read_config()

    start_conexion()

    for lab in labels:
        listaFinal = []
        read_emails(lab,listaFinal)
        read_links(listaFinal)
