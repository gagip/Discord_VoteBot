"""
트위코드 (twitch + discord) 봇
작성자: gagip
"""
import discord, asyncio
from discord.ext import commands
import os
import numpy as np
import json

from bs4 import BeautifulSoup
import time
import datetime
# 사용자 정의 모듈
import Utils
from PointManager import PointManager

# intents = discord.Intents(messages=True, guilds=True, members=True) # 괄호 안에 활성화할 인텐트를 작성해야함
intents = discord.Intents.all()  # bot에게 모든 작업 권한 주기
bot = commands.Bot(command_prefix='!')


@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()  # PyNaCl 라이브러리 필요


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.event
async def on_voice_state_update(member, before, after):
    # 보이스톡에 들어왔을 때
    if before.channel is None and after.channel is not None:
        try:
            with open(f"./data/log/{member.id}.json", "r") as f:
                data = json.load(f)
                date_date = datetime.datetime.strptime(data['daily']['date'], "%Y/%m/%d %H:%M")
                if (datetime.datetime.today().date() != date_date.date()):
                    data["daily"] = {"point": 0, "date": datetime.datetime.now().strftime("%Y/%m/%d %H:%M")}
                data["log"][str(len(data['log']))] = \
                    [datetime.datetime.now().strftime("%Y/%m/%d %H:%M"), after.channel.id, "in"]

            with open(f"./data/log/{member.id}.json", "w") as f:
                json.dump(data, f, indent=4, sort_keys=True)

        except:
            with open(f"./data/log/{member.id}.json", "w") as f:
                data = {}
                data["daily"] = {"point": 0, "date": datetime.datetime.now().strftime("%Y/%m/%d %H:%M")}
                data["log"] = {0: [datetime.datetime.now().strftime("%Y/%m/%d %H:%M"), after.channel.id, "in"]}
                json.dump(data, f, indent=4, sort_keys=True)
                pass

    # 보이스톡에 나갈 때
    elif before.channel is not None and after.channel is None:
        try:
            with open(f"./data/log/{member.id}.json", "r") as f:
                data = json.load(f)
                data['log'][str(len(data['log']))] = \
                    [datetime.datetime.now().strftime("%Y/%m/%d %H:%M"), before.channel.id, "out"]

            # 참가할 때마다 포인트 제공
            mes = pointManager.give_point_for_joining_chennel(member, data)

            with open(f"./data/log/{member.id}.json", "w") as f:
                json.dump(data, f, indent=4, sort_keys=True)
            if mes != -1:
                await before.channel.guild.text_channels[0].send(mes)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    # bot 토큰 불러오기
    token = ""
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/token.txt", 'r', encoding='utf-8') as t:
        token = t.read().split()[0]

    pointManager = PointManager()
    bot.run(token)
