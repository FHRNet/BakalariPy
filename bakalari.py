#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib
import hashlib
import base64
import datetime
import xmltodict

from urllib.request import urlopen
from xml.dom import minidom


class BakalariAPI:
    username = ""
    password = ""
    url = ""
    token = ""

    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url + "/login.aspx"

    # Misc functions
    def http_call(self, params):
        return(urlopen(self.url + "?ifaceVer=1&hx=" + self.token + "&" + params, timeout=5).read())

    def parse_xml(self, xml):
        return(xmltodict.parse(xml))

    def check_token(self):
        if(self.token == ""):
            raise Exception("Not logged in")

    # Authentication
    def get_seeds(self):
        data = urlopen(self.url + "?gethx=" + self.username, timeout=5).read()
        xml = minidom.parseString(data.decode('utf-8'))

        try:
            res = (xml.getElementsByTagName('res')[0]).childNodes[0].data
            salt = (xml.getElementsByTagName('salt')[0]).childNodes[0].data
            ikod = (xml.getElementsByTagName('ikod')[0]).childNodes[0].data
            typ = (xml.getElementsByTagName('typ')[0]).childNodes[0].data
        except Exception:
            raise Exception("Wrong credentials")

        return(salt, ikod, typ, res)

    def get_prehash(self, salt, ikod, typ):
        vals = salt + ikod + typ + self.password
        prehash = base64.b64encode(hashlib.sha512(vals.encode('utf-8')).digest()).decode('utf-8')

        return(prehash)

    def get_token(self, prehash):
        date = datetime.date.today()

        vals = str("*login*" + self.username + "*pwd*" + prehash + "*sgn*" + "ANDR" + str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2)).encode("utf-8")
        hash = base64.b64encode(hashlib.sha512(vals).digest()).decode('utf-8')
        token = hash.replace('\\', '_').replace('+', '-').replace('/', "_")

        return(token)

    def login(self):
        salt, ikod, typ, res = self.get_seeds()
        self.token = self.get_token(self.get_prehash(salt, ikod, typ))
        return(self.token)


    # API
    def info(self):
        self.check_token()
        return(self.parse_xml(self.http_call("pm=login").decode('utf-8'))["results"])

    def znamky(self):
        self.check_token()
        return(self.parse_xml(self.http_call("pm=znamky").decode('utf-8'))["results"]["predmety"])

    def znamky_vahy(self):
        self.check_token()
        return(self.parse_xml(self.http_call("pm=predvidac").decode('utf-8'))["results"]["typypru"])

    def ukoly(self):
        self.check_token()
        return(self.parse_xml(self.http_call("pm=ukoly").decode('utf-8'))["results"]["ukoly"])

    def rozvrh(self):
        self.check_token()
        return(self.parse_xml(self.http_call("pm=rozvrh").decode('utf-8'))["results"]["rozvrh"])

    def predmety(self):
        self.check_token()
        return(self.parse_xml(self.http_call("pm=predmety").decode('utf-8'))["results"]["predmety"])

    def absence(self):
        self.check_token()
        return(self.parse_xml(self.http_call("pm=absence").decode('utf-8'))["results"]["absence"])

    def pololeti(self):
        self.check_token()
        return(self.parse_xml(self.http_call("pm=pololetni").decode('utf-8'))["results"])
