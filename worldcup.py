#!/usr/bin/python

import requests
import json
import time
import datetime
import xmpp

def check_ticket(games):
    r = requests.get("https://fwctickets.fifa.com/TopsAkaCalls/Calls.aspx/getRefreshChartAvaDem?l=en&c=BRA")

    header = json.loads(r.text)['d']
    inner_json = json.loads(header['data'])
    products = inner_json['BasicCodes']['PRODUCTPRICES']

    for p in products:
        if p['PRPProductId'] in games and int(p['Quantity']) not in [-1, 0]:
            yield p

def notify(msg):
    user = "my_dummy_account@gmail.com"
    password = "my_dummy_password"
    target = "gtalk_to_receive_message@gmail.com"

    jid = xmpp.JID(user)
    connection = xmpp.Client('gmail.com', debug=[])
    connection.connect(('talk.google.com',5222))

    result = connection.auth(jid.getNode(), password, "Penguin")
    connection.sendInitPresence()
    connection.send(xmpp.Message(target, msg))

def main():
    games = ['IMT36', 'IMT47', 'IMT55', 'IMT62']

    while True:
        try:
            dt = datetime.datetime.now()
            print '[%02d/%02d - %02d:%02d:%02d]' % (dt.day, dt.month, dt.hour, dt.minute, dt.second)

            found = [p for p in check_ticket(games)]

            if len(found) == 0:
                time.sleep(60)
                continue

            msg = '-- Found tickets:'
            for p in found:
                msg += "Game: %s - Category %s - Quantity - %s\n" % (p['PRPProductId'], p['PRPCategoryId'], p['Quantity'])

            print msg

            notify(msg)

            time.sleep(1800);
        except:
           print "Something bad happened..."
           time.sleep(60)


if __name__ == "__main__":
    main()
