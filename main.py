import discord, asyncio
from discord.ext import commands
import os
import numpy as np

bot = commands.Bot(command_prefix='!')
# 토큰
token_path = os.path.dirname(os.path.abspath(__file__))+"/token.txt"
t = open(token_path, 'r', encoding='utf-8')
token = t.read().split()[0]

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name) # 봇의 이름 출력
    print(bot.user.id) # 봇의 고유 ID넘버 출력
    print('------')

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect() # PyNaCl 라이브러리 필요

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def 도움(ctx):
    embed = discord.Embed(title=f"해당 봇은 투표 기능이 있는 봇입니다.", description=f'개발자: gagip')
    embed.add_field(name=f'!롤자랭', value=f'랜덤 다섯 명을 골라 랜덤 포지션')
    await ctx.send(embed=embed)

@bot.command()
async def 롤자랭(ctx, *dis_member):
    # 현재 음성 채널에 있는 사람들 호출
    user = ctx.author # 호출한 사람
    channel = user.voice.channel
    members = np.array([member.name for member in channel.members])
    # 특정 멤버 제외
    if len(dis_member) != 0:
        print(dis_member)
        idx_list = [abs(int(member))-1 for member in dis_member]
        # TODO dis_member의 숫자가 아닐 시 예외처리 해줘야 함
        members = np.delete(members, idx_list)

    # 샘플링
    import random
    position = ['탑', '정글', '미드', '원딜', '서폿']
    random_position = random.sample(position, len(members))
    # 각 멤버들에게 할당
    embed = discord.Embed(title=f"투표 결과", description=f'다시 하자고 하는 흑우 없재')
    for i in range(len(random_position)):
        embed.add_field(name=members[i], value=f"{random_position[i]}\n")
    await ctx.send(embed=embed)

bot.run(token)