from peewee import *
import datetime


def getDbPath():
    if __name__ == "__main__":
        return "../bot_database.db"
    return "bot_database.db"

db = SqliteDatabase(getDbPath())


class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    chat_id = CharField(unique=True)
    user_name = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    reg_date = DateTimeField(default=datetime.datetime.now)
    need_update = BooleanField(default=False)

class UserList(BaseModel):
    chat_id = CharField(unique=True)
    user_coins = TextField(null=True)

if __name__ == "__main__":
    print("started...")
    db.connect()
    db.create_tables([User])

    users = User.select()
    counter = int(users.count())

    # for i in range(100):
    #     newUser = User(chat_id=counter)
    #     newUser.save()
    #     print("added {}'th".format(counter))
    #     counter+=1
    print()
    for i in User.select():
        print(i.reg_date)
