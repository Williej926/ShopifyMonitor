import requests
import discord_webhook
from discord_webhook import  DiscordWebhook,DiscordEmbed
import random
import json
import time
from datetime import datetime

productList = {}
numProd = 0;
webhookURL = ""
storeUrl = ""
def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)
# def getProxy():
#     proxy = (str) (random_line("proxies.txt"))
#     ip = proxy[:proxy.find(":")]
#     rest = proxy[proxy.find(":")-1:]
#     rest = rest[2:]
#     port = rest[:rest.find(":")]
#     rest = rest[6:]
#     print(rest)

#     user = rest[:rest.find(":")]
#     pw = rest[rest.find(":"):]
#     pw = pw[1:]
#     proxyFinal = ("http://"+user+":"+pw+"@"+ip+":"+port)
#     proxyDict = {
#         "https": proxyFinal
#     }
#     print(proxyDict)
#     return proxyDict

def getProxy():
    proxy = (str) (random_line("proxies.txt"))
    if(proxy.count(":")>1):
        ip = proxy[:proxy.find(":")]
        rest = proxy[proxy.find(":")-1:]
        rest = rest[2:]
        port = rest[:rest.find(":")]
        rest = rest[6:]
        print(rest)
        user = rest[:rest.find(":")]
        pw = rest[rest.find(":"):]
        pw = pw[1:]
        proxyFinal = ("http://"+user+":"+pw+"@"+ip+":"+port)
        proxyDict = {
            "https": proxyFinal
        }
        return proxyDict
    else:
        print(proxy)
        ip = proxy[:proxy.find(":")]
        rest = proxy[proxy.find(":"):]
        rest = rest[1:]
        port = rest[:rest.find(":")]
        print(rest[6:])
        rest = rest[6:]
        user = rest[:rest.find(":")]
        pw = rest[rest.find(":"):]
        proxyFinal = ("http://"+proxy)
        proxyDict = {
            "https": proxyFinal
        }
        return proxyDict
s = requests.Session()
s.proxies = getProxy()
req = s.get(storeUrl+"/products.json")

try:
    j = json.loads(req.content)
    print(j)
    prod = j["products"]
    for p in prod:
        productList[p['id']] = p['title']
    numProd = len(prod)
except:
    productList = {}
    numProd = 0




print(productList)
while True:
    while True:
        s = requests.Session()
        s.proxies = getProxy()
        try:
            req = s.get(storeUrl + "/products.json", timeout=3)
            print(req.status_code)
            if(req.status_code == 403):
                print("PASSWORD PAGE UP, RETRYING")
                currentDT = datetime.now()
                print(currentDT.strftime("%I:%M:%S %p"))

                time.sleep(5)
                break

            j = json.loads(req.content)
        except:
            print("PW Page/Banned")
            currentDT = datetime.now()


            print(currentDT.strftime("%I:%M:%S %p"))
            time.sleep(0.5)
            break
        prod = j["products"]

        if(len(prod) > numProd):
            numProd = len(prod)
            for p in prod:
                variants = ""

                if(p['id'] not in productList):
                    print("NEW PRODUCT: " + str(p['title']))
                    print(str(p['variants']))
                    productList[p['id']] = p['title']
                    for id in p['variants']:
                        variants = variants + (id['title']+": " + storeUrl+ "/cart/" + str(id['id'])+":1") +  " --- "+ str(id['id'])+ "\n"

                #print(variants)
                    embed = DiscordEmbed(title=("NEW PRODUCT: " + str(p['title'])), description=variants, color=12212731)
                    images = p['images']
                    if(len(images)>0):
                        images = str(images[0]).replace("'", '"')
                        images = json.loads(images)
                        embed.set_thumbnail(url=str(images['src']))
                    embed.set_url(url=(storeUrl+"/products/" + str(p['handle'])))
                    webhook = DiscordWebhook(
                        webhookURL)
                    webhook.add_embed(embed)
                    webhook.execute()


        for p in prod:

            if(p['id'] not in productList):
                variants = ""
                variantList = ""
                productList[p['id']] = p['title']
                for id in p['variants']:
                    variantList += str(id['title'])  + " : " + str(id['id'])+"\n"
                    variants = variants + (
                            str(id['title']) + ": " + storeUrl+ "/cart/" + str(id['id']) + ":1" + "  " + str(id['price'])) + "\n"
                print("CHANGE DETECTED: " + str(p['title']))
                embed = DiscordEmbed(title=("NEW PRODUCT: " + str(p['title'])), description=variants+variantList, color=12212731)
                images = p['images']
                if(len(images)>0):
                    images = str(images[0]).replace("'", '"')
                    images = json.loads(images)
                    embed.set_thumbnail(url=str(images['src']))


                embed.set_url(url=(storeUrl + "/products/" + str(p['handle'])))
                webhook = DiscordWebhook(
                    webhookURL)
                webhook.add_embed(embed)
                webhook.execute()

        print(numProd)
        print(str(len(prod)))

        currentDT = datetime.now()

        print(currentDT.strftime("%I:%M:%S %p"))
        time.sleep(0.5)



