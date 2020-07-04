import random
import csv
import requests
import subprocess
title=str(input("Film : "))
#year=str(input("Année : "))
d=requests.get("https://yts.mx/api/v2/list_movies.json?query_term="+str(title)+"&quality=720p&limit=1&sort_by=download_count")
di=d.json()
try:
	has=di['data']['movies'][0]['torrents'][0]['hash']
except KeyError:
	print("J'ai pas désolé!")
	quit()
magnet="magnet:?xt=urn:btih:"+str(has)+"&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80&tr=udp://tracker.opentrackr.org:1337/announce"
#get them subs on opensubtitles
try:
	langsub=input("Sous-titres? (en/fr) (no si pas besoin) : ")
except ValueError:
	print("(en/fr/no) : ")

if langsub=="no":
	if input("Stream dans VLC? (o/N) : ")=="o":
		command="webtorrent --vlc "+str(magnet)
	else:
		command="webtorrent "+str(magnet)
	subprocess.call(command, shell=True)
auth=requests.post("https://www.opensubtitles.com/api/v1/login", data={"username":"helloapi","password":"g1231230"})
tokensub=auth.json()["token"]
titlel=list(title)
titlefl=[]
for i in titlel:
	if i==" ":
		titlefl.append("+")
	else:
		titlefl.append(i)
titlef="".join(titlefl)
subqueryurl="https://www.opensubtitles.com/api/v1/search/movie?query="+titlef
subqueryr=requests.get(subqueryurl,headers={"Authorization":tokensub})
subquery=subqueryr.json()["data"]
# for i in subquery:
# 	if i["attributes"]["year"]==str(year):
# 		idmov=i["id"]
# 	else:
# 		continue
idmov=subquery[0]["id"]
try:
	idmov
except NameError:
	print("Not on opensubtitle!")
	quit()
movsuburl="https://www.opensubtitles.com/api/v1/find?id="+str(idmov)+"&languages="+str(langsub)
movpagr=requests.get(movsuburl,headers={"Authorization":tokensub})
movpag=movpagr.json()
idsub=movpag["data"][0]["attributes"]["files"][0]["id"]
dlsubr=requests.post("https://www.opensubtitles.com/api/v1/download", data={"file_id": int(idsub),"sub_format": "srt"},headers={"Authorization":tokensub})
dlsuburl=dlsubr.json()['link']
dlsub = requests.get(dlsuburl)
subtitle=str(title)+".srt"
with open(subtitle, 'wb') as f:
    f.write(dlsub.content)
if input("Stream in VLC? (o/N) : ")=="o":
	command="webtorrent --vlc "+str(magnet)
else:
	command="webtorrent "+str(magnet)
subprocess.call(command, shell=True)
