from mongoengine import *


connect('matches', alias='default')


class Match(Document):
    ID = IntField()
    time = StringField()
    date = StringField()
    tournament = StringField()
    posted = BooleanField(default=False)
    player1 = StringField()
    player2 = StringField()
    player1k = FloatField()
    player2k = FloatField()
    start_total = FloatField()
    finish_total = FloatField()

