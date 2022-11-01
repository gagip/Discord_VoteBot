from main import *


@bot.command(aliases=['도네', 'give', '기부'])
async def 후원(ctx, name, money):
    '''
    다른 유저에게 포인트를 후원합니다
    :param name: 후원해줄 이름
    :param money: 후원 포인트
    '''
    pointManager.set_ctx(ctx)

    members = ctx.guild.members  # 현 채널의 멤버들
    sponsor_id = ctx.author.id  # 후원자 id
    beneficiary_id = pointManager.find_id(name)  # 수혜자 id

    if beneficiary_id == -1: await ctx.send("해당 아이디가 존재하지 않습니다."); return

    money = int(money)
    complte = False  # 후원 성공 여부

    if money < 0: await ctx.send('1 포인트 이상 하셔야 합니다'); return

    data = pointManager.load_data()

    # 자기 자신 허용 X
    if sponsor_id == beneficiary_id:
        await ctx.send(f"자기 자신에게 후원할 수 없습니다")
        return

    # 후원자가 충분한 돈이 있는가?
    if data[str(sponsor_id)] >= money:
        data[str(sponsor_id)] -= money
        data[str(beneficiary_id)] += money
        await ctx.send(
            f"{ctx.guild.get_member(sponsor_id)}님이 {ctx.guild.get_member(beneficiary_id)}님에게 {money:,}포인트 후원하였습니다.")

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
    pointManager.set_ctx(ctx)
    data = pointManager.load_data()

    # money 내림차순 정렬
    sorted_data = sorted(data.items(), key=(lambda x: x[1]), reverse=True)

    # 결과 텍스트 작성
    s = '';
    rank = 0;
    for d in sorted_data[:min(len(sorted_data), top)]:
        rank += 1
        s += f'{rank}등 {pointManager.find_name(d[0])} : {d[1]:,} 포인트\n'

    # 결과 텍스트를 디스코드에 전달
    embed = discord.Embed(title=f"랭킹", description=f'디버그용')
    embed.add_field(name=f"한 달 간격으로 초기화 됩니다.", value=s)
    await ctx.send(embed=embed)
