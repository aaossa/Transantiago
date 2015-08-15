import requests
import random
import time
import os

"Example: http://paraderos.cl/paraderos#/paraderos/paradero:PI470/bus:"


def manualCut(html):
    A = list(html)
    out = []
    s = ''
    text = False
    while(len(A) > 0):
        char = A.pop(0)
        if char == '<':
            text = False
            if len(s) > 0:
                out.append(s)
            s = ''
        elif text and char != '\n' and char != '\t':
            s = s + char
        if char == '>':
            text = True
    return out


def cutHtml(html):
    a = html[
        html.find("""<div data-role="header" data-position="fixed" data-theme="b">"""):]
    return a[:a.find("""</div><!-- /content -->""")]


def LoadUserAgents(uafile="user_agents.txt"):
    # http://willdrevo.com/using-a-proxy-with-a-randomized-user-agent-in-python-requests/
    """
    uafile : string
        path to text file of user agents, one per line
    """
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1 - 1])
    random.shuffle(uas)
    return uas


def sendRequest(paradero):
    uas = LoadUserAgents()
    ua = random.choice(uas)

    url = "http://paraderos.cl/paraderos/paradero:" + paradero + "/bus:"
    headers = {
        "Connection": "close",
        "User-Agent": ua}
    r = requests.get(url, headers=headers)
    s = cutHtml(r.text)
    plano = manualCut(s)
    return plano


# LR -> BQ
Paraderos_SUR = ["PI470", "PI400", "PI1042", "PI457", "PI438", "PI339", "PI448", "PI401", "PI340", "PI439", "PI341", "PI440", "PI342", "PI343", "PI402", "PI368", "PA657", "PA335", "PA163", "PA369", "PA336", "PA164", "PA370", "PA337",
                 "PA165", "PA668", "PA28", "PA338", "PA215", "PA598", "PA350", "PA167", "PA339", "PA340", "PA371", "PA168", "PA166", "PA350", "PA371", "PA341", "PA169", "PA372", "PA342", "PA383", "PC198", "PC1147", "PC1148", "PC199", "PC147"]

# BQ -> LR
Paraderos_NORTE = ["PC196", "PA384", "PA343", "PA373", "PA41", "PA42", "PA692", "PA385", "PA182", "PA344", "PA374", "PA183", "PA375", "PA345", "PA184", "PA365", "PA376", "PA346", "PA366", "PA185", "PA377", "PA347",
                   "PA187", "PA348", "PA186", "PA349", "PA551", "PA367", "PA16", "PI403", "PI344", "PI454", "PI404", "PI345", "PI405", "PI449", "PI471", "PI450", "PI406", "PI458", "PJ538", "PJ539", "PJ113", "PJ112", "PJ165"]

# Código principal
"""
for i in Paraderos_SUR:
	with open(r"Paraderos/Sur/" + i + ".txt", "a") as file:
		pass
for j in Paraderos_NORTE:
	with open(r"Paraderos/Norte/" + j + ".txt", "a") as file:
		pass
"""


def Recopilar_datos():
    for i in Paraderos_NORTE:
        data = sendRequest(i)
        with open(r"Paraderos/Norte/" + i + ".txt", "a") as file:
            file.write(str(data) + "\n")
    print("Iteracion NORTE completada... " + time.ctime())

    for j in Paraderos_SUR:
        data = sendRequest(j)
        with open(r"Paraderos/Sur/" + j + ".txt", "a") as file:
            file.write(str(data) + "\n")
    print("Iteracion SUR completada... " + time.ctime())

while time.localtime().tm_hour < 8:
    print("Esperando... " + time.ctime())
    time.sleep(120)
    if (time.localtime().tm_min > 15) and (time.localtime().tm_hour == 7):
        break

last_min = time.localtime().tm_min

while time.localtime().tm_hour <= 9 and (time.localtime().tm_min < 25):
    time.sleep(5)
    if time.localtime().tm_min != last_min:
        Recopilar_datos()
    last_min = time.localtime().tm_min

print("FIN de programa")
