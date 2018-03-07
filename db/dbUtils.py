from Coins.Coin import Coin
from Coins.coinUtils import getAnswer
from db import modelsSql
from db.modelsSql import User, UserList


def addUser(message):
    db = modelsSql.db
    db.create_tables([User])

    id = message.chat.id
    name = message.chat.username
    firstname = message.chat.first_name
    lastname = message.chat.last_name

    newUser = User(chat_id=id,
                   user_name=name,
                   first_name=firstname,
                   last_name=lastname)
    try:
        newUser.save()
    except:
        return False

    print("\"{} {} {} {}\" added\n".format(id, name, firstname, lastname))
    return True


def addUserList(message):
    db = modelsSql.db
    db.create_tables([User])

    id = message.chat.id
    newUserList = UserList(chat_id=id,
                           user_coins="btc")
    try:
        newUserList.save()
    except:
        return False
    return True

def getUsers():
    users = User.select()
    result = ""
    for i in users:
        result += "{} {} {} {}\n".format(i.chat_id,
                                         i.user_name,
                                         i.first_name,
                                         i.last_name)
    return result


def getUserCoinListPrice(id, cBase):
    db = modelsSql.db
    db.create_tables([UserList])
    result = ""
    uList = []

    userCoinList = UserList.select().where(UserList.chat_id == id)
    for i in userCoinList:
        uList = i.user_coins.split(" ")
    for coin in uList:
        result += getAnswer(coin, cBase) + "\n"
    return result


def addCoinToList(id, cointext, cBase):
    db = modelsSql.db
    db.create_tables([UserList])

    coin = Coin(cointext, cBase)
    if not coin.isValid():
        return "Invalid coin id \"{}\"".format(cointext)
    oldListSet = UserList.select().where(UserList.chat_id == id)
    oldList = []
    for i in oldListSet:
        oldList = i
    newList = set(oldList.user_coins.split(" "))
    if cointext.lower() in newList:
        return "\"{}\" is also in your list.".format(cointext)
    newList.add(cointext.lower())
    newList = " ".join(newList)
    oldList.user_coins = newList
    oldList.save()
    print("{} added {} in his list".format(oldList.chat_id, cointext))
    return "\"{}\" was added in your list.".format(cointext)

def removeCoinFromList(id, cointext):
    db = modelsSql.db
    db.create_tables([UserList])
    oldListSet = UserList.select().where(UserList.chat_id == id)
    oldList = []
    for i in oldListSet:
        oldList = i
    newList = set(oldList.user_coins.split(" "))
    if not cointext.lower() in newList:
        return "You have no \"{}\" in your list.".format(cointext)
    elif len(newList) == 1:
        return "You have just one coin in your list. I cann't to delete them."
    newList.remove(cointext.lower())
    newList = " ".join(newList)
    oldList.user_coins = newList
    oldList.save()
    print("{} removed {} in his list".format(oldList.chat_id, cointext))
    return "\"{}\" was removed from your list.".format(cointext)

def getUserCoinList(id):
    db = modelsSql.db
    db.create_tables([UserList])
    result = "\nYour coin list contain:\n"
    uList = []

    userCoinList = UserList.select().where(UserList.chat_id == id)
    for i in userCoinList:
        uList = i.user_coins.split(" ")

    return result + "\n".join(uList)