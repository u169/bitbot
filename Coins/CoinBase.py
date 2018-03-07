import parser.cmcParser as parser
import time


class CoinBase():

    def __init__(self, fileName, url="https://api.coinmarketcap.com/v1/ticker/"):
        self.fileName = fileName
        self.url = url
        self.updateCoinList()
        self.date = time.time()

    def getCoin(self, coinText):
        tDelta = time.time() - self.date
        if tDelta >= 300:
            self.updateCoinList()
            print("Changed")
        coin = parser.getCoin(self.fileName, coinText)
        self.date = time.time()
        return coin

    def updateCoinList(self):
        parser.getCoinList(self.fileName, self.url)


if __name__ == "__main__":
    print("Basinga...")

    path = "../coinList.json"
    Base = CoinBase(path)

    print(Base.getCoin("xrp")["price_usd"])
    print(Base.getCoin("btc")["price_usd"])

    # req = 1
    # for i in range(49999999):
    #     req = req * i
    # after = time.time()
    print(Base.getCoin("fadfda"))