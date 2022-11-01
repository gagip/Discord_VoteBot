from main import *


@bot.command(aliases=['놀이터', '승부예측'])
async def 토토시작(ctx, title, *choice):
    pointManager.set_ctx(ctx)

    # 포맷에 맞추지 못할 때
    if title is None or len(choice) != 2:
        await ctx.send('잘못입력하셨습니다')
        return

    mes = pointManager.create_toto(ctx.author, title, choice)

    if mes == 1:
        await ctx.send(f'토토 배팅 생성! {title}\n\n"!토토"를 입력하여 배팅현황을 파악하고\n"!배팅 [선택지] [포인트]"를 입력하여 배팅을 해보세요')
        await 토토(ctx)
    else:
        await ctx.send(mes)


@bot.command()
async def 토토(ctx):
    """
    토토 배팅 현황을 보여줍니다
    """
    try:
        # 토토 관련 데이터
        pointManager.set_ctx(ctx)
        toto_data = pointManager.load_data('toto')
        author = pointManager.find_name(toto_data['author'])
        c1, c2 = pointManager.view_toto()

        # 토토 현행 결과 mesage 입력
        embed = discord.Embed(title=f"{toto_data['title']}", description=f'주최자:{author} 개발자: gagip')
        s1 = Utils.to_long_string(f'''\
        총 포인트: {c1[0]}
        비율: {c1[1]}%
        배당:1: {c1[2]}
        최고배팅자: {c1[3]}
        최고배팅액: {c1[4]}\
        ''')
        embed.add_field(name=f"[1] {toto_data['choice1']}",
                        value=Utils.to_str_color(s1, 'red'))

        s2 = Utils.to_long_string(f'''\
        총 포인트: {c2[0]}
        비율: {c2[1]}%
        배당:1: {c2[2]}
        최고배팅자: {c2[3]}
        최고배팅액: {c2[4]}\
        ''')
        embed.add_field(name=f"[2] {toto_data['choice2']}",
                        value=Utils.to_str_color(s2, "blue"))
        await ctx.send(embed=embed)
    except:
        await ctx.send('진행중인 토토가 없습니다. 혹시 "!토토시작"을 안하셨나요?')


@bot.command(aliases=[])
async def 배팅(ctx, choice, point):
    pointManager.set_ctx(ctx)
    mes = pointManager.betting(ctx.author, choice, point)

    if mes != -1:
        await ctx.send(mes)
        await 토토(ctx)
    else:
        await ctx.send('진행중인 토토가 없습니다. 혹시 "!토토시작"을 안하셨나요?')


@bot.command(aliases=['마감', '배팅마감', '배팅제한'])
async def 배팅종료(ctx):
    pointManager.set_ctx(ctx)
    mes = pointManager.end_betting(ctx.author)

    if mes != -1:
        await ctx.send(mes)
    else:
        await ctx.send('진행 중인 토토가 없습니다. 혹시 "!토토시작"을 안하셨나요?')


@bot.command(aliases=[])
async def 토토종료(ctx, choice):
    pointManager.set_ctx(ctx)

    mes = pointManager.end_toto(ctx.author, choice)

    if mes != -1:
        await ctx.send(mes)
        await ctx.send('토토 종료')
    else:
        await ctx.send('명령어를 잘못 입력하신거 같아요')
