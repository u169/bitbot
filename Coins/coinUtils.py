from Coins.Coin import Coin
from Coins.CoinBase import CoinBase


def getAnswer(text, cBase):
    text = text.split(" ")
    coin = Coin(text[-1], cBase)
    if coin.coinJSON == None:
        return "Invalid coin id '{}'".format(text[-1])
    if len(text) == 1:
        return getOne(coin, cBase)
    return getOneSum(coin, text[0], cBase)

def getOneSum(coin, volume, cBase):
    volume = float(volume)
    cost = volume * float(coin.getPrice())
    cost = round(cost, 2)

    result = "{} {} = {} USD".format(volume,
                                    coin.getSymbol(),
                                    cost)
    return result

def getOne(coin, cBase):
    result = "{}({}) = {} USD".format(coin.getName(),
                                  coin.getSymbol(),
                                  coin.getPrice())
    return result


if __name__ == "__main__":
    base = CoinBase("../coinList.json")

    print(getAnswer("btc", base))
    print(getAnswer("25 xrp", base))
    print(getAnswer("25 fdaf", base))
    print(getAnswer("fdsaf 31 42 5252rfaf", base))
