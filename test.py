
import requests, getpass, json, datetime, re, sys, copy, inspect, os, argparse
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession
from time import sleep

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

fNovel = open("Novel.txt", "w")

sess = requests.session()

r = sess.get('https://members.popo.tw/apps/login.php', headers=headers)
login_data = {}
try:
    login_data = json.loads(open('account.json').read())
except:
    print("Unexpected error:", sys.exc_info()[0])
res = sess.post(r.url, data = login_data, headers=headers)

origUrl = "https://www.popo.tw"
url = "https://www.popo.tw/books/583771/articles/6772370"

while True:
    response = sess.get(url, headers=headers)
    # fileName = "test.html"
    # f = open(fileName, "w")
    # f.write(response.content.decode('utf-8'))
    # f.close()
    
    soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
    readmask = soup.find(id="readmask")
    title = readmask.find_next("h2")
    fNovel.write(title.text)
    fNovel.write("\n\n")
    ps = readmask.find_all_next("p")
    ps = ps[:-3]
    for p in ps:
        s = p.text
        if len(s) > 0:
            s = s[:-1]
    
        fNovel.write(s)
        fNovel.write("\n")
    
    fNovel.write("----------------\n")

    nexts = soup.findAll("a", {"class": "next"})
    if len(nexts) == 0:
        break
    else:
        url = origUrl + nexts[0]["href"]

fNovel.close()
