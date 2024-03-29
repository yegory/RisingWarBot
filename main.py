import os
import discord
from discord.ext import commands
import requests  # to be able to make http requests
import json

client = commands.Bot(command_prefix = '.')

aws = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjlkODhiNzQxLWY4MTEtNGUzNy04NmZkLWIyMTYwODQ0MTVhNiIsImlhdCI6MTY0NzczNTAzNiwic3ViIjoiZGV2ZWxvcGVyLzU4M2RiYjBmLWI3OWYtNjAxOC04YWUzLTg0YmZhNmMzZjIwNiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjM0LjIxNC4xMzUuOTMiXSwidHlwZSI6ImNsaWVudCJ9XX0.DWjD73DNVGrNqmoNRGstAfDZ7dGp_fDIDcmycINIHlhB9TjerL6H3A0TNwRAHG7zA3b_5cyTTypDzs4BRxuDNw"
home = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjE2YTk4MTE5LTA4MDMtNDc5Ni1hNDFhLTgzZmU4YmU2YjE1OSIsImlhdCI6MTY0NzQ3ODM1Niwic3ViIjoiZGV2ZWxvcGVyLzU4M2RiYjBmLWI3OWYtNjAxOC04YWUzLTg0YmZhNmMzZjIwNiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjI0Ljg1LjI0Ni45NSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.mrhRIsg3VVn2qmdalA96Wl92iOSHtqvoSvlb4rB341BkiBcmnS_V_NeWDQNkn2zulm0zWUB8kKoCb9z834MfMA"

headers = {
    'authorization': 'Bearer ' + aws,
    'Accept': 'application/json'
}     

def get_player_info(player_tag):
    # return user profile information
    response = requests.get("https://api.clashofclans.com/v1/players/%23" + player_tag, headers=headers)
    #print(response.status_code)
    return response.json()


def get_clan_info(clan_tag="L8VU00CY"):
    # submit a clan search
    response = requests.get("https://api.clashofclans.com/v1/clans/%23" + clan_tag, headers=headers)
    #print(response.status_code)
    return response.json()


def player_info_helper(data):
    output_str = '''
Player Name              {}
Player Level                {}
Town Hall	               {}
Trophy Record           {}
War Stars                   {}
Attacks this season  {}
Friend in Need           {}'''.format(data['name'],
                                      data['expLevel'],
                                      data['townHallLevel'],
                                      data['bestTrophies'],
                                      data['warStars'],
                                      data['expLevel'],
                                      data["achievements"][14]["value"])
    return output_str


def clan_info_helper(data):
    if (data['isWarLogPublic'] == False):
        loss_var="War Log is set to Private"
    else: 
        loss_var=data['warLosses']
    output_str = "Clan Tag: {tag}\nClan Name: {name}\nType: {type}\nClan Level: {level}\nClan Trophies: {trophies}\nClan Wins: {wins}\nWar Losses: {losses}\nCWL: {league}\n".format(
        tag=data['tag'],
        name=data['name'],
        type=data['type'],
        level=data['clanLevel'],
        trophies=data['clanPoints'],
        wins=data['warWins'],
        losses=loss_var,
        league=data['warLeague']['name'])
    return output_str


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # check if message is from ourselves
    if message.author == client.user:
        return

    msg = message.content
    msend = message.channel.send
    if msg.startswith(".help"):
        await message.channel.send('''
		-- List of commands --
.playerinfo <PlayerTag> : gets information about a player with the #PlayerTag
.claninfo <ClanTag> : gets clan informatin for clan with #ClanTag. 
    ->If .claninfo is called without a ClanTag, the default clan is used''')
        
    if msg.startswith(".playerinfo"):

        player_tag = msg.split('.playerinfo ', 1)[1]
        if player_tag[0] == "#":
            player_tag = player_tag[1:]

        data = get_player_info(player_tag)
        try:
            output_str = player_info_helper(data)
            await msend(output_str)
        except Exception:
            await msend("Failed to find a player with the provided tag...")

    if msg.startswith(".claninfo"):
        if len(msg.strip()) != 9:
            clan_tag = msg.split('.claninfo ', 1)[1]
            if clan_tag[0] == "#":
                clan_tag = clan_tag[1:]
            data = get_clan_info(clan_tag)
        else:
            data = get_clan_info()

        try:
            output_str = clan_info_helper(data)
            await msend(output_str)
        except Exception:
            await msend("Something went wrong")

client.run('OTUzNzA3MjcyMTQyNDcxMjA4.YjIfHA.PMT9g77nRgi7qTRMO0kwKbTPUBs')
