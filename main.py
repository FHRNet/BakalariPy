from bakalari import BakalariAPI

# Login
api = BakalariAPI("user", "pass", "https://url/bakalari/")
api.login()

rozvrh = api.rozvrh()

print("Tento tyden je *%s*, *%s*" % (rozvrh["nazevcyklu"], rozvrh["zkratkacyklu"]))
