import discord, asyncio
from discord.ext import commands
import os
import numpy as np

bot = commands.Bot(command_prefix='!')
# 토큰
path = os.path.dirname(os.path.abspath(__file__))
t = open(path+"/token.txt", 'r', encoding='utf-8')
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
    embed.add_field(name=f'!롤자랭', value=f'!롤자랭 / 채널 멤버들에게 랜덤 포지션을 부여합니다.\n'
                                        '!롤자랭 2 4 / 2번째, 4번째 멤버를 제외하고 실행합니다.')
    embed.add_field(name=f'!롤전적', value=f'롤전적 아이디 / 해당 아이디의 최근 롤 전적을 간단하게 보여줍니다.')
    embed.add_field(name=f'!투표', value=f'!투표 / 투표장이 투표 세팅을 한 후 투표를 진행합니다.')
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

# TODO 투표 기능 추가
@bot.command()
async def 투표(ctx):
    pass

# TODO 롤 전적
@bot.command()
async def 롤전적(ctx, id):
    import requests
    from bs4 import BeautifulSoup
    import re

    url = f'http://www.op.gg/summoner/userName={id}'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, features='html.parser')
    info_data = []
    def add_data(info):
        print(info)
        if info is not None:
            if re.search(r"\<.*\>", str(info)) is None: # 태그가 있는지 확인
                info_data.append(info)
            else:
                info_data.append(info.get_text().strip()) # 텍스트 추출
        else:
            info_data.append(None)
        print(info_data)

    # 해당아이디가 존재하지 않는 경우
    if soup.find('div', class_='SummonerNotFoundLayout'):
        await ctx.send("해당 아이디가 존재하지 않네요. 혹시 오타는 아니시죠?")
        return

    add_data("tier info")
    info_data.append(id) # id 추가
    rank_info = soup.find('div', class_='TierRankInfo')
    add_data(rank_info.find('div', class_='TierRank')) # 솔로랭크 티어 추가
    if "Unranked" not in info_data: # 언랭이 아니면
        add_data(rank_info.find('div', class_='TierInfo').find('span', 'LeaguePoints')) # 리그 포인트 추가
        for i in rank_info.find('div', class_='TierInfo').find('span', 'WinLose').find_all('span'): # 승,패,승률 추가
            add_data(i)

    # 모스트 추가
    add_data("most champ")
    if soup.find('div', class_='MostChampionContent') is not None:
        most_champ = soup.find('div', class_='MostChampionContent').find_all('div', 'ChampionBox Ranked')
        # 모스트 3 추출
        for champ in most_champ[: min(3, len(most_champ))]:
            info_data.append(champ.find('div', class_='Face')['title']) # 챔피언 이름
            add_data(champ.find('span', class_='KDA')) # KDA
            for i in champ.find('div', class_='Played').find_all('div'): # 승률, 플레이 수
                add_data(i)

    # 최근 7일간 랭크 승률
    add_data("lately 7days")
    if soup.find('div', class_='Content') is not None:
        for champ in soup.find('div', class_='Content').find_all('div', class_='ChampionWinRatioBox'):
            info_data.append(champ.find('div', class_='ChampionName')['title'])
            add_data(champ.find('div', class_='WinRatio'))
            add_data(champ.find('div', class_='Text Left'))
            add_data(champ.find('div', class_='Text Right'))
    add_data("end")

    # TODO 데이터 전처리

    # 데이터 출력
    def print_data(start, end):
        start_idx = info_data.index(start)
        end_idx = info_data.index(end)
        result = ""
        if end_idx - start_idx == 1:
            return "해당 데이터가 존재하지 않습니다."
        for txt in info_data[start_idx+1:end_idx]:
            if txt is None:
                result += "값이 없습니다" + "\n"
            else:
                if re.search(r"^[a-zA-Z]+",txt) and start != "tier info":
                    result += "-------\n"
                result += txt + "\n"
        return result

    # TODO 디자인 고안
    embed = discord.Embed(title=f"{id}님 전적", description=f'디버그용')
    embed.add_field(name=f"Tire info", value=print_data("tier info", "most champ"))
    embed.add_field(name=f"모스트 챔프", value=print_data("most champ", "lately 7days"))
    embed.add_field(name=f"최근 전적", value=print_data("lately 7days", "end"))
    await ctx.send(embed=embed)


bot.run(token)