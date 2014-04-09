
import xml.etree.ElementTree as ET
import imaplib
from datetime import datetime
import time
from dateutil import parser
import sys
from email.parser import HeaderParser
import urllib2
import os
import argparse
import dateutil.tz
from time import gmtime, strftime


user = None
password = None
mail = None
conf_SSL = None

root = None
tree = None
path = None

download = None
start_Date = None
end_Date = None

labels = []

def read_options():

    today = datetime.now().strftime("%Y-%m-%d");

    parser = argparse.ArgumentParser(description='email Link Downloader',
                                 prefix_chars='-',version='1.0')

    parser.add_argument('-d', '--download', action='store_true', default=False,
                    dest='download',
                    help='Download finded files')

    parser.add_argument('-i', '--init', action='store', dest='init', default=today,
                    help='First day for search - Format: YYYY-MM-DD')

    parser.add_argument('-e', '--end', action='store', dest='end', default=today,
                    help='Last day for search - Format: YYYY-MM-DD')


    results = parser.parse_args()

    global download
    global start_Date
    global end_Date

    download = results.download
    start_Date = results.init
    end_Date = results.end


    validate(start_Date,parser)
    validate(end_Date,parser)

def validate(date_text, parser):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        print "\nFormato de fecha incorrecto, debe ser en el siguiente formato YYYY-MM-DD\n"

        parser.print_help()

        sys.exit(0)

def read_config():

    global password
    global user
    global labels
    global conf_SSL
    global root
    global tree
    global path



    read_options()


    tree = ET.parse('config.xml')

    root = tree.getroot()

    user = root.find('email').find('auth').find('user').text
    password = root.find('email').find('auth').find('password').text

    conf_SSL = root.find('email').find('config').find('ssl').text


    for l in root.find('labels').findall('label'):
        labels.append(l.text)


    path = root.find('dir').text
    if path[-1:] != '/': path += '/'
    create_directory(path)

def start_date_timestamp(tzinfo):
    year = int(start_Date.split('-')[0])
    mounth = int(start_Date.split('-')[1])
    day = int(start_Date.split('-')[2])

    date_init =  datetime(year, mounth, day, 0, 0,0,0,tzinfo=tzinfo)
    timestamp_init = float(time.mktime(date_init.timetuple()))
    return timestamp_init


def end_date_timestamp(tzinfo):

    year = int(end_Date.split('-')[0])
    mounth = int(end_Date.split('-')[1])
    day = int(end_Date.split('-')[2])
    date_end =  datetime(year, mounth, day, 23, 59,59,999999,tzinfo=tzinfo)
    timestamp_end = float(time.mktime(date_end.timetuple()))
    return timestamp_end



def create_directory(path):
    if not os.path.isdir(path):
        splitpath = path.split('/')
        completPath = ''
        for dir in splitpath:
            completPath += dir + '/'
            if not os.path.isdir(dir) and dir != "":
                os.makedirs(completPath)



def read_emails(lab,listaFinal):

    mail.select(lab)
    result, data = mail.search(None, "ALL")


    ids = data[0]
    id_list = ids.split()

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

        init_date_compare = start_date_timestamp(date.tzinfo)
        end_date_compare = end_date_timestamp(date.tzinfo)


        if init_date_compare <= fdate and fdate <= end_date_compare:
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
    lista_links = []
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

            if download: download(l)
            lista_links.append(l)

        except:
            continue
    return lista_links


def create_file(lista,lab):
    today = datetime.now().strftime("%Y-%m-%d");

    name = lab + "_" +str(today);
    finalname = name + ".txt"
    num = 1
    while os.path.isfile(path+finalname):
        finalname = name + "_" + str(num) + ".txt"
        num += 1

    f = open(path+finalname, 'w')

    for l in lista:
        f.write(l + "\n")

    print "\nCreado el fichero "+finalname+" en la ruta "+ path+finalname +" con los enlaces encontrados.\n"

if __name__ == "__main__":
    read_config()

    start_conexion()

    for lab in labels:
        listaFinal = []
        read_emails(lab,listaFinal)
        lista_links = read_links(listaFinal)
        if len(lista_links) > 0: create_file(lista_links,lab)
        else: print "\nNo hay links en los emails de estas fechas.\n"



