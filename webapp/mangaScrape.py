import os
import urllib.request as url_request
import urllib.error as url_error
import requests
from bs4 import BeautifulSoup as bs
import re
from difflib import SequenceMatcher as sm
from PIL import Image
from io import StringIO
from requests.exceptions import ConnectionError


#proxy = "http://<username>:<password>@<host>:<port>"
#proxyDict = {
#              "http": proxy,
#              "https": proxy,
#              "ftp": proxy
#            }

#proxy_support = urllib2.ProxyHandler(proxyDict)
opener = url_request.build_opener()
url_request.install_opener(opener)
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


def findNextURL(imageUrl):

    return imageUrl.parent["href"]


def saveImg(data, base_host, base_url, base_path, image_title):
    maxval = 0
    maxurl = ""
    imglinks = data.findAll("img")
    check_link = base_host.split("//")[1]
    if len(check_link.split('.')) > 2:
        check_link = check_link.split('.')[1] + "." + check_link.split('.')[2]
    for link in imglinks:
        if check_link in str(link['src']) and sm(None, str(link['src']), base_url.replace("http", "")).ratio() > maxval:
            maxval = sm(None, str(link['src']), base_url).ratio()
            maxl = link
            maxurl = link['src']
    if maxurl == '':
        for link in imglinks:
            if sm(None, str(link['src']), base_url.replace("http", "")).ratio() > maxval:
                maxval = sm(None, str(link['src']), base_url).ratio()
                maxl = link
                maxurl = link['src']

    if "http" not in str(maxurl):
        maxurl = base_host.split("//")[0] + maxurl

    print(maxurl)
    try:
        image = requests.get(maxurl)
        print("Images Saved Successfully")
    except:
        print ("Error")
        exit(0)

    file = open(os.path.join(base_path, "%s.jpg") % image_title, 'wb')
    try:
        Image.open(StringIO(image.content)).save(file, 'JPEG')
    except IOError as e:
        print("Couldnt Save:", e)

    finally:
        file.close()

    return maxl


def linkData(base_url):
    try:
        #req = urllib2.Request(base_url, headers=hdr)
        #resp = urllib2.urlopen(req).read()
        r = requests.get(base_url)

        data = bs("".join(r.text))

        return data
    except url_error as e:
        print(e.fp.read())


def main(base_url, base_path, total_img):
    base_host = re.split(r"/", base_url)[0] + "//" + re.split(r"/", base_url)[2]
    #base_path = re.split(r"/", base_url)[3] + "_"+re.split(r"/", base_url)[4]

    #print base_host
    image_title = 0

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    imageUrl = saveImg(linkData(base_url), base_host, base_url, base_path, image_title)
    #print imageUrl.parent['href']

    ctr = 0
    while ctr < total_img - 1:
        image_title = image_title + 1
        next_rel = findNextURL(imageUrl)
        #print next_rel
        if not "://" in next_rel:
            if next_rel.startswith("/"):
                base_url = base_host + next_rel
            else:
                base_url = re.sub(r"\w+.html", next_rel, base_url)
        else:
            base_url = next_rel

        print("Next page is", base_url)
        imageUrl = saveImg(linkData(base_url), base_host, base_url, base_path, image_title)
        ctr = ctr + 1
    print("Total Pages Downloaded: ", (ctr + 1))