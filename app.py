import telebot
import json

from peewee import SqliteDatabase
from telebot import types

from Coins.CoinBase import CoinBase
from Coins.coinUtils import getAnswer
from db.dbUtils import addUser, getUserCoinList, addCoinToList, addUserList, getUserCoinListPrice, removeCoinFromList

with open('config.json', 'r') as confile:
    config = json.load(confile)

ptrnOneCoin = r"(\A[a-zA-Z-]+\Z)"
ptrnSomeCoins = r"\A(\d*.?\d*)\s([A-Za-z-]+\Z)"
urlCmcApi = config["coinmarketcap"]["url"] + config["coinmarketcap"]["limit"]

coinBase = CoinBase("coinList.json", urlCmcApi)
API_TOKEN = config["bot"]["token"]

db = SqliteDatabase('bot_database.db')
db.connect()
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(m):
    bot.send_message(m.chat.id, "Получи курс криптовалюты в USD.\n"
                                "Введи :\n"
                                "\"Bitcoin\" - узнай курс Биткоина.\n"
                                "\"23 bitcoin-cash\" - узнай сколько стоит 23 Биткоин Кэш.\n"
                                "\"0.005 Ethereum\" - узнай сколько стоит 0.005 Эфира.\n"
                                "Добавлена новая функция /mylist. Введи /mylist чтобы узнать больше.\n"
                                "Не забудь ввести /help, чтобы обновить клавиатуру.\n"
                                "Курс берётся с сайта coinmarketcap.com.\n"
                                "Поддержать прокет) - /goodBot\n"
                                "Обратная связь @ku113p\n")
    addMainKeyboard(m)
    afterAll(m)

@bot.message_handler(commands=['goodBot'])
def goodBot(m):
    answer = "1PfTuLa4bUTKgFWMhASFzzCLy7qUbghY8J"
    bot.send_message(m.chat.id, "Кошелёк (BTC):")
    bot.send_message(m.chat.id, answer)
    afterAll(m)

@bot.message_handler(commands=['ul'])
def getUsers(m):
    result = getUsers()
    bot.send_message(m.chat.id, result)
    afterAll(m)

@bot.message_handler(commands=['mylist'])
def myList(m):
    result = getUserCoinListPrice(m.chat.id, coinBase)
    bot.send_message(m.chat.id,
                     "Введи команду /addtolist, чтобы добавить коин в список.\n"
                     "Введи команду /removefromlist, чтобы убрать коин из списка.")
    bot.send_message(m.chat.id, str(result))
    afterAll(m)

@bot.message_handler(commands=['addtolist'])
def wantAddToList(m):
    result = "Какой коин хочешь добавить в свой список?"
    bot.send_message(m.chat.id, str(result))
    bot.register_next_step_handler(m, addToList)
    afterAll(m)

def addToList(m):
    result = addCoinToList(m.chat.id, m.text, coinBase)
    bot.send_message(m.chat.id, result)

@bot.message_handler(commands=['removefromlist'])
def wantRemoveFromList(m):
    result = "Какой коин хочешь убрать из своего списка?"
    result += getUserCoinList(m.chat.id)
    bot.send_message(m.chat.id, str(result))
    bot.register_next_step_handler(m, removeFromList)
    afterAll(m)

def removeFromList(m):
    result = removeCoinFromList(m.chat.id, m.text)
    bot.send_message(m.chat.id, result)

@bot.message_handler(regexp=ptrnOneCoin)
def getOneCoin(m):
    result = getAnswer(m.text, coinBase)
    bot.send_message(m.chat.id, result)
    afterAll(m)

@bot.message_handler(regexp=ptrnSomeCoins)
def getCoinPrice(m):
    result = getAnswer(m.text, coinBase)
    bot.send_message(m.chat.id, result)
    afterAll(m)

@bot.message_handler(func=lambda m: True)
def unknownCommand(m):
    bot.send_message(m.chat.id, "Invalid request")
    afterAll(m)

def addMainKeyboard(m):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    itembtn1 = types.KeyboardButton('BTC')
    itembtn2 = types.KeyboardButton('ETH')
    itembtn3 = types.KeyboardButton('LTC')
    itembtn4 = types.KeyboardButton('DASH')
    itembtn5 = types.KeyboardButton('XMR')
    itembtn6 = types.KeyboardButton('XZC')
    itembtn7 = types.KeyboardButton('/help')
    itembtn8 = types.KeyboardButton("/mylist")

    keyboard.add(itembtn1, itembtn2, itembtn3)
    keyboard.add(itembtn4, itembtn5, itembtn6)
    keyboard.add(itembtn7, itembtn8)
    bot.send_message(m.chat.id, "Курс чего хочешь узнать?", reply_markup=keyboard)

def afterAll(m):
    addUser(m)
    addUserList(m)
    print("{} : {}".format(m.chat.id, m.text))

def run():
    while True:
        try: bot.polling()
        except: pass

if __name__ == "__main__":
    print("Started...\n")
    # run()
    bot.polling()

