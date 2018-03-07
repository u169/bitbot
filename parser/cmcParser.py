import requests
import json
from pprint import pprint


def getCoinList(coinFilePath, url='https://api.coinmarketcap.com/v1/ticker/'):
    r = requests.get(url)
    coinList = r.json()
    with open(coinFilePath, "w") as file:
        json.dump(coinList, file)

def getCoin(coinFilePath, coinName):
    with open(coinFilePath, "r") as file:
        coinList = json.load(file)
    for c in coinList:
        if isItCoin(coinName, c):
            return c
    return None

def isItCoin(coinName, coinDict):
    id = str(coinName).lower()
    sym = str(coinName).upper()
    dictVals = {coinDict["id"], coinDict["symbol"]}
    if id in dictVals or sym in dictVals:
        return True
    return False

if __name__ == "__main__":
    print("Parsing...")

    path = "../coinList.json"

    getCoinList(path, "https://api.coinmarketcap.com/v1/ticker/?limit=1000")

    coin = getCoin(path, "xrp")
    pprint(coin)
    coin = getCoin(path, "xmr")
    pprint(coin)