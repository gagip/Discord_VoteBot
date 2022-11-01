from main import *


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
    else:  # 언랭일 시
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


@bot.command(aliases=['point', '점수'])
async def 포인트(ctx, name=None):
    pointManager.set_ctx(ctx)

    if name is None:
        id = ctx.author.id
    else:
        id = pointManager.find_id(name)

    if id == -1: await ctx.send('해당 아이디가 존재하지 않습니다.'); return

    await ctx.send(f'{pointManager.find_name(id)}님의 현재 포인트는 {pointManager.find_point(id)}입니다.')

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
