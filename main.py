import discord, asyncio
from discord.ext import commands
import os
import numpy as np
import json

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime
# 사용자 정의 모듈
from PointManager import PointManager
bot = commands.Bot(command_prefix='!')




def find_id(find_name, members):
    '''
    이름 ->고유 id 반환
    :param find_name: 조회할 유저 이름
    :param memebers: 채널 멤버 리스트
    '''
    for member in members:
        if member.name == find_name:
            return member.id
        if member.nick == find_name:
            return member.id
    return -1

def find_name(find_id, members):
    '''
    고유 id -> 이름 반환
    :param find_id: 조회할 유저 id
    :param members: 채널 멤버 리스트
    '''
    for member in members:
        if member.id == find_id:
            return member.name
    return -1


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)  # 봇의 이름 출력
    print(bot.user.id)  # 봇의 고유 ID넘버 출력
    print('------')

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()  # PyNaCl 라이브러리 필요

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command(aliases=['h', '도움말'])
async def 도움(ctx):
    embed = discord.Embed(title=f"해당 봇은 투표 기능이 있는 봇입니다.", description=f'개발자: gagip')
    embed.add_field(name=f'!롤자랭', value=f'!롤자랭 / 채널 멤버들에게 랜덤 포지션을 부여합니다.\n'
                                        '!롤자랭 2 4 / 2번째, 4번째 멤버를 제외하고 실행합니다.')
    embed.add_field(name=f'!롤전적', value=f'롤전적 아이디 / 해당 아이디의 최근 롤 전적을 간단하게 보여줍니다.')
    embed.add_field(name=f'!투표', value=f'!투표 / 투표장이 투표 세팅을 한 후 투표를 진행합니다.')
    await ctx.send(embed=embed)


@bot.command(aliases=['자랭'])
async def 롤자랭(ctx, *dis_member):
    # 현재 음성 채널에 있는 사람들 호출
    user = ctx.author  # 호출한 사람
    channel = user.voice.channel
    members = [member.name for member in channel.members]
    print(members)

    # 특정 멤버 제외
    if len(dis_member) != 0:
        idx_list = [abs(int(member)) - 1 for member in dis_member]
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


@bot.command()
async def 투표(ctx, title, *choice):
    '''
    투표
    :param title: 투표 제목
    :param choice: 선택지 (최대 9개)
    '''
    # TODO 웹
    # TODO 중복투표 불가능하게
    # TODO 익명투표 만들기
    # 투표 도움말
    if title is None and choice == ():
        embed = discord.Embed(title=f'투표 도움말', description=f'개발자: gagip')
        embed.add_field(name=f'좋아요/싫어요', value=f'!투표 제목')
        embed.add_field(name=f'복수응답(1-9)', value=f'!투표 제목 내용1 내용2 ...')
        await ctx.send(embed=embed)
    
    # 투표 진행
    else:
        embed = discord.Embed(title=title)
        if choice == ():
            # 좋아요/싫어요
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
            await message.add_reaction('👎')
        else:
            # 복수응답(1-10)
            emoji_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']  # 선택지 번호 라벨

            s = ''
            emoji = iter(emoji_list)
            for cont in choice:
                try:
                    s += f'{next(emoji)} {cont}\n'
                except ValueError:
                    await ctx.sent('투표 선택지는 9개까지만 가능합니다.')
                    return

            # 디스코드에 제목 출력
            embed.add_field(name=s, value='1은 기본적으로 있음, 중복투표 가능')
            message = await ctx.send(embed=embed)

            # 디스코드에 선택지 출력
            for i in range(len(choice)):
                await message.add_reaction(emoji_list[i])


@bot.command(aliases=['도네', 'give'])
async def 후원(ctx, name, money):
    '''
    다른 유저에게 포인트를 후원합니다
    :param name: 후원해줄 이름
    :param money: 후원 포인트
    '''
    members = ctx.guild.members             # 현 채널의 멤버들
    sponsor_id = ctx.author.id              # 후원자 id
    beneficiary_id = find_id(name, members) # 수혜자 id
    
    if beneficiary_id == -1: await ctx.send("해당 아이디가 존재하지 않습니다."); return
    
    money = int(money)
    complte = False     # 후원 성공 여부

    
    pointManager.set_ctx(ctx)
    data = pointManager.load_data()

    # 자기 자신 허용 X
    if sponsor_id == beneficiary_id:
        await ctx.send(f"자기 자신에게 후원할 수 없습니다")
        return

    # 후원자가 충분한 돈이 있는가?
    if data[str(sponsor_id)] >= money:
        data[str(sponsor_id)] -= money
        data[str(beneficiary_id)] += money
        await ctx.send(f"{ctx.guild.get_member(sponsor_id)}님이 {ctx.guild.get_member(beneficiary_id)}님에게 {money:,}포인트 후원하였습니다.")

        complte = True
    else:
        await ctx.send("후원할 금액이 충분하지 않습니다.")
        return

    # 저장 
    if complte: pointManager.save_data(data)

@bot.command(aliases=['순위'])
async def 랭킹(ctx, top=10):
    '''
    현 채널의 멤버 포인트 랭킹 조회
    :param top: 상위 몇까지 보여줄지
    ''' 
    print(ctx.guild.members)
    pointManager.set_ctx(ctx)
    data = pointManager.load_data()
    
    # money 내림차순 정렬
    sorted_data = sorted(data.items(), key=(lambda x:x[1]), reverse=True)
    
    # 결과 텍스트 작성
    s = ''; rank = 0;
    for d in sorted_data:
        rank += 1
        s += f'{rank}등 {pointManager.find_name(d[0])} : {d[1]:,} 포인트\n'

    # 결과 텍스트를 디스코드에 전달
    embed = discord.Embed(title=f"랭킹", description=f'디버그용')
    embed.add_field(name=f"한 달 간격으로 초기화 됩니다.", value=s)
    await ctx.send(embed=embed)
                
@bot.command()
async def tts(ctx, voice, mes):
    """
    !tts 오덕(할아버지|잼민이) "메시지"
    :param voice: 목소리 타입
    :param mes: 메세지
    """
    # await ctx.author.voice.channel.connect() # 봇이 보이스 채널에 들어감

    # 크롬창 열기
    browser = webdriver.Chrome(executable_path=r'C:\selenium\chromedriver.exe')
    browser.get("https://typecast.ai/create-v2")
    time.sleep(0.5)

    # typecast 로그인
    with open(path + "/typecast.txt", 'r', encoding='utf-8') as typecast:
        cont = typecast.readlines()
        id = cont[0].strip()
        pw = cont[1].strip()
    browser.find_element_by_id("email").send_keys(id)
    browser.find_element_by_id("password").send_keys(pw)
    browser.find_elements_by_tag_name("button")[0].click()
    print(f"로그인완료: {mes}")
    time.sleep(10)
    
    # 스크립트 작성
    soup = BeautifulSoup(browser.page_source, "html.parser")
    browser.find_element_by_class_name('ProseMirror').send_keys(mes)            # 본문에 글 적기
    share_btn = browser.find_elements_by_class_name('menu-list-item')[3]        # 3번째 버튼 (공유하기)
    browser.execute_script('arguments[0].click();', share_btn)
    print(f"공유 성공: {mes}")
    time.sleep(10)
    
    # url 호출
    soup = BeautifulSoup(browser.page_source, "html.parser")
    url = soup.find('div', class_='code-background').get_text().strip()
    
    # TODO 보이스 채널에 url 재생 
    soup = BeautifulSoup(browser.page_source, "html.parser")
    
    
    
   

    browser.close()
    print(f"추출 완료: {mes}")
    await ctx.send(url)
    pass

# TODO UNKOWN 데이터 처리
@bot.command()
async def 롤전적(ctx, id):
    """
    op.gg에서 가져온 해당 유저의 롤 전적 조회
    :param id: 조회할 유저 id
    """
    import requests
    from bs4 import BeautifulSoup
    import re

    url = f'http://www.op.gg/summoner/userName={id}'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, features='html.parser')

    # 태그 안에서 텍스트 추출
    def get_data(info):
        if info is not None:
            if re.search(r"\<.*\>", str(info)) is None:  # 태그가 있는지 확인
                return info
            else:
                return info.get_text().strip()  # 텍스트 추출
        else:
            return 'None'

    # 데이터 출력
    def print_data(info_type):
        result = ''
        # 해당 데이터가 존재하지 않는다면
        if len(info_type) == 1:
            return '해당 정보가 존재하지 않습니다.'
        else:
            for row in info_type[1:]:  # 데이터
                count = 0
                for data in info_type[0]:  # 해더
                    result += data + ': ' + row[count] + '\n'
                    count += 1
                if row is not info_type[-1]:
                    result += '-' * 10 + '\n'
            return result

    # 해당아이디가 존재하지 않는 경우
    if soup.find('div', class_='SummonerNotFoundLayout'):
        await ctx.send("해당 아이디가 존재하지 않네요. 혹시 오타는 아니시죠?")
        return

    # 소환사 정보
    user_info = [['소환사 이름', '티어', '리그 포인트', '승리', '패배', '승률']]
    name = id  # id 추가
    rank_info = soup.find('div', class_='TierRankInfo')
    tier = get_data(rank_info.find('div', class_='TierRank'))  # 솔로랭크 티어 추가
    if tier != 'Unranked': 
        lp = get_data(rank_info.find('div', class_='TierInfo').find('span', 'LeaguePoints'))  # 리그 포인트 추가
        win = get_data(rank_info.find('span', class_='wins'))  # 승리 수 추가
        lose = get_data(rank_info.find('span', class_='losses'))  # 패배 수 추가
        winratio = get_data(rank_info.find('span', class_='winratio'))  # 승률 추가
    else: # 언랭일 시
        lp, win, lose, winratio = 'None', 'None', 'None', 'None'
    user_info.append([name, tier, lp, win, lose, winratio])

    # 모스트 추가
    most_champ_lst = [['챔피언', 'kda', '승률']]
    if soup.find('div', class_='MostChampionContent') is not None:
        most_champ = soup.find('div', class_='MostChampionContent').find_all('div', 'ChampionBox Ranked')
        # 모스트 3 추출
        for champ in most_champ[: min(3, len(most_champ))]:
            champ_name = get_data(champ.find('div', class_='Face')['title'])  # 챔피언 이름 추가
            kda = get_data(champ.find('span', class_='KDA'))  # KDA
            champ_winratio = get_data(champ.find('div', class_='WinRatio normal tip'))  # 승률
            most_champ_lst.append([champ_name, kda, champ_winratio])

    # 최근 7일간 랭크 승률
    last_7 = [['챔피언 이름', '승률', '승리', '패배']]
    if soup.find('div', class_='Content') is not None:
        for champ in soup.find('div', class_='Content').find_all('div', class_='ChampionWinRatioBox'):
            champ_name = get_data(champ.find('div', class_='ChampionName')['title'])
            champ_winratio = get_data(champ.find('div', class_='WinRatio'))
            champ_win = get_data(champ.find('div', class_='Text Left'))
            champ_lose = get_data(champ.find('div', class_='Text Right'))
            last_7.append([champ_name, champ_winratio, champ_win, champ_lose])

    # TODO 데이터 전처리

    

    # TODO 디자인 고안
    embed = discord.Embed(title=f"{id}님 전적", description=f'디버그용')
    embed.add_field(name=f"Tire info", value=print_data(user_info))
    embed.add_field(name=f"모스트 챔프", value=print_data(most_champ_lst))
    embed.add_field(name=f"최근 전적", value=print_data(last_7))
    await ctx.send(embed=embed)

if __name__ == "__main__":
    # bot 토큰 불러오기
    token = ""
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/token.txt", 'r', encoding='utf-8') as t:
        token = t.read().split()[0]
    
    pointManager = PointManager()
    bot.run(token)