from mongoengine import *


#connect('matches',host='ds223685.mlab.com', port=23685,username='heroku_xs74xv52', password='6ak8s2geflvkb2tl3rudf5bikn')
connect('matches',host='mongodb://heroku_xs74xv52:6ak8s2geflvkb2tl3rudf5bikn@ds223685.mlab.com:23685/heroku_xs74xv52')

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

