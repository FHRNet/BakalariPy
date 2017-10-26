#!/usr/bin/python 
# -*- coding: utf-8 -*-

from bakalari import BakalariAPI

# Login
api = BakalariAPI("user", "pass", "http://url/bakalari/")
api.login()

rozvrh = api.rozvrh()

print("Tento tyden je *%s*, *%s*" % (rozvrh["nazevcyklu"], rozvrh["zkratkacyklu"]))
