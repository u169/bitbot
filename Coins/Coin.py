from Coins.CoinBase import CoinBase


class Coin:

    def __init__(self, coinText, base):
        self.CoinBase = base
        self.coinJSON = base.getCoin(coinText)

    def getName(self):
        if self.coinJSON == None:
            return None
        return self.coinJSON["name"]

    def getId(self):
        if self.coinJSON == None:
            return None
        return self.coinJSON["id"]

    def getSymbol(self):
        if self.coinJSON == None:
            return None
        return self.coinJSON["symbol"]

    def getPrice(self):
        if self.coinJSON == None:
            return None
        return self.coinJSON["price_usd"]

    def isValid(self):
        return self.coinJSON != None

if __name__ == "__main__":
    path = "../coinList.json"
    Base = CoinBase(path)

    btc = Coin("xmr", Base)

    print(btc.getPrice())