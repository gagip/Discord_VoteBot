from main import *


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
