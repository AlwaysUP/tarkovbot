import discord
import constants
from time import time, ctime
import psycopg2
import os

def setupDB():
    if (os.getenv('DATABASE_URL')==None):
        print("*****************THE DATABSE URL DOES NOT EXIST!!!*****************")
    else:
        conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS kills (id serial primary key, killerid varchar(255), killedid varchar(255));")
        cur.execute("CREATE TABLE IF NOT EXISTS player (playerid varchar(255), playername varchar(255), PRIMARY KEY (playerid));")
        conn.commit()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
        cur = conn.cursor()
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content.lower().startswith('!log'):
            if len(message.mentions) == 2:
                cur.execute("select * from player where playerid LIKE '%s';"%(message.mentions[0].id))
                if len(cur.fetchall())==0:
                    cur.execute("insert into player (playerid, playername) VALUES ('%s','%s');"%(message.mentions[0].id, message.mentions[0].display_name))
                cur.execute("select * from player where playerid LIKE '%s';"%(message.mentions[1].id))
                if len(cur.fetchall())==0:
                    cur.execute("insert into player (playerid, playername) VALUES ('%s','%s');"%(message.mentions[1].id, message.mentions[1].display_name))
                cur.execute("INSERT INTO kills (killerid, killedid) VALUES('%s','%s');"%(message.mentions[0].id, message.mentions[1].id))
                conn.commit()
                await message.channel.send("%s +1"%(message.mentions[0].display_name))
            else:
                await message.channel.send('Usage: `!log @killer @killed`')
        if message.content.lower().startswith('!kills'):
            cur.execute("select playername from player inner join kills on player.playerid=kills.killedid where kills.killerid='%s';"%(message.author.id))
            kills = cur.fetchall()
            for kill in kills:
                await message.channel.send(kill[0])
            conn.commit()
        if message.content.lower().startswith('!resetkills'):
            await message.channel.send('`Restting all kills, player records will remain`')
            cur.execute("TRUNCATE kills;")
            conn.commit()
        if message.content.lower().startswith('!leader'):
            cur.execute("select player.playername, (select count(*) from kills where killerid=player.playerid) as killcount from player order by killcount DESC LIMIT %d;"%(10))
            players = cur.fetchall()
            for player in players:
                await message.channel.send("%s: %d"%(player[0], player[1]))
            conn.commit()
        conn.close()

setupDB()
client = MyClient()
client.run(constants.token)