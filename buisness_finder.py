# -*- coding: utf-8 -*-

import re
import csv
import urllib2
import urllib
import simplejson as json
import time

reader = csv.reader(open('clients.csv', 'rb'))

class YandexSearch:
    def biz(self, query):
        url = "http://maps.yandex.ru/?text="+query+"&where=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0&sll=37.581343%2C55.747313&sspn=0.01987%2C0.002965&l=map&source=form.biz&output=json";

        f = urllib2.urlopen(url)

        return json.loads(f.read())

addresses = []

with open('client_phones.csv', 'wb') as f:
    for row in reader:
        query = row[0]
        query = urllib.quote_plus(query)

        result = YandexSearch().biz(query)

        items = result['vpage']['data']['businesses']['items']

        if len(items) > 0:
            address = items[0]['address']['text']

            try:
                phones = ", ".join([phone['number'] for phone in items[0]['phones']])
            except:
                phones = ""

            link = "http://maps.yandex.ru/?text="+query+"&where=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0&results=20&z=15&l=map"

            item = [row[0].decode('utf-8'), address, phones, u"%d адресов" % result['vpage']['data']['businesses']['found'], link]
        else:
            item = [row[0].decode('utf-8')]

        line = ";".join(item)+"\n"
        f.write(line.encode('utf-8'))

        print row[0].decode('utf-8')

        time.sleep(0.5)


