from main import *


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)  # 봇의 이름 출력
    print(bot.user.id)  # 봇의 고유 ID넘버 출력
    print('------')


@bot.command(aliases=['h', '도움말', '명령어'])
async def 도움(ctx):
    embed = discord.Embed(title=f"해당 봇은 투표 기능이 있는 봇입니다.", description=f'개발자: gagip')
    embed.add_field(name=f'!롤자랭', value=f'!롤자랭 \n 채널 멤버들에게 랜덤 포지션을 부여합니다.\n'
                                        '!롤자랭 [2] [4] \n 2번째, 4번째 멤버를 제외하고 실행합니다.')
    embed.add_field(name=f'!롤전적', value=f'롤전적 [아이디]\n 해당 아이디의 최근 롤 전적을 간단하게 보여줍니다.')
    embed.add_field(name=f'!투표', value=f'!투표 [선택지1] [선택지2]...\n 투표장이 투표 세팅을 한 후 투표를 진행합니다. 선택지가 없을 시 찬반투표로 진행')
    embed.add_field(name=f'!tts', value=f'!tts [오덕] [메시지]\n tts 목소리로 해당 메시지를 읽어줍니다. (개발중)')
    embed.add_field(name=f'!후원', value=f'!후원 [후원할 유저 id] [후원할 포인트]\n 유저에게 후원')
    embed.add_field(name=f'!랭킹', value=f'!랭킹 [숫자]\n 1위부터 [숫자]까지 포인트 랭킹 목록을 보여줍니다.')
    embed.add_field(name=f'!포인트', value=f'!포인트 [해당 유저]\n [해당 유저]의 잔여 포인트를 보여줍니다.')
    embed.add_field(name=f'!토토시작', value=f'!토토시작 [제목] [선택지1] [선택지2]\n 토토 배팅을 시작합니다.')
    embed.add_field(name=f'!토토', value=f'!토토\n 토토 배팅 현황을 파악합니다.')
    embed.add_field(name=f'!배팅', value=f'!배팅 [선택지(1 or 2)] [포인트]\n 해당 선택지에 배팅을 합니다.')
    embed.add_field(name=f'!배팅종료', value=f'!배팅종료 [선택지(1 or 2)]\n 토토 배팅을 종료합니다.')
    embed.add_field(name=f'!토토종료', value=f'!토토종료 [선택지(1 or 2)]\n 토토 배팅을 종료하고 포인트를 정산합니다.')

    await ctx.send(embed=embed)

    embed = discord.Embed(title=f"주의", description=f'개발자: gagip')
    embed.add_field(name=f"명령어는 띄어쓰기에 민감합니다. 띄어쓰기가 있는 문자열을 입력하고 싶을 땐 쌍따옴표(\")를 사용하세요",
                    value=f'예시\n!포인트 살인마 싸대기 딱대  (x)\n!포인트 "살인마 싸대기 딱대" (O)')

    await ctx.send(embed=embed)
