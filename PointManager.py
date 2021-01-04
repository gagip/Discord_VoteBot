import json
import discord, asyncio
import os
from discord.ext import commands

import datetime

path = os.path.dirname(os.path.abspath(__file__))

def to_str_color(s, color):
    """
    디스코드 글씨 색을 바꿉니다
    디스코드 문법 참고: https://docs.google.com/document/d/1a93Obt9BDMGh-SL3quzU6OoyOJ3ZKN78Ez2CBA4FeEw/edit
    https://docs.google.com/document/d/1JxA085nOZgVIWXMPUrjJcGhX6MDVgZ1rD8OZ-hcYCmk/edit
    
    Parameter
    ---------
    s : str
        문자열
    color : str
        문자열(s)의 색깔

    Return
    ------
    result : str
        색깔이 바뀐 문자열
    """

    result = "```"
    if color == "red":
        result += "diff\n"
        result += "\n".join(["-"+line for line in s.split("\n")])
    elif color == "blue":
        result += "md\n"
        result += "\n".join(["#"+line for line in s.split("\n")])
    elif color == "yellow":
        result += "css\n"
    result += "```"
    return result

def to_long_string(long_str):
    """긴 문자열 처리"""
    return '\n'.join([line.strip() for line in long_str.splitlines()])

<<<<<<< HEAD

=======
>>>>>>> 402cf0814d786fe8df43f91c23d10164e8ec2ec2
class PointManager():
    # Singleton Pattern
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.ctx = None
        self.members = None
        self.join_point = 10
        self.date_format = "%Y/%m/%d %H:%M"

    def set_ctx(self, ctx):
        self.ctx = ctx
        self.members = self.ctx.guild.members
    
    def get_ctx(self):
        print(self.ctx)

    
    def init_data(self):
        """
        채널 멤버 포인트 DB 생성 (json)
        """
        # 데이터 생성
        members = self.ctx.guild.members # 현 채널의 멤버들
        """
        members[0] example:
        <Member id=363536605249798154 name='gagip' discriminator='7145' bot=False nick=None 
        guild=<Guild id=715541406772625475 name='API test' shard_id=None chunked=True member_count=3>>
        """
        members_id = [member.id for member in members] # 현 채널의 멤버들 id
        
        # json 파일에 저장
        data = {}
        for id in members_id:
            data[id] = 100
        self.save_data(data)

    def reset_data(self, ctx, year, month):
        """
        한달마다 포인트 DB 초기화
        :param year: 기존 파일 작성 년도
        :param month: 기존 파일 작성 월
        """
        # TODO 어떻게 자동 초기화 시킬 것인지? 
        # DB 최신 작성 날짜가 한 달 이상 지났는지 확인
        today = datetime.datetime.today()
        if not (today.year == year and today.month == month):
            init_data(self.ctx)      # DB 초기화
    
    def load_data(self, guild=None):
        """json 파일 불러오기"""
        if guild is None: guild = self.ctx.guild
        try:
            with open(f'./data/{guild}.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # TODO 임시로 해놨는데 고치기
            if guild != "toto":
                self.init_data()

    def save_data(self, data, guild=None):
        """
        json 파일 쓰기
        :param data: 작성할 데이터
        """
        # TODO 롤백 기능 추가
        if guild is None: guild = self.ctx.guild
        with open(f'./data/{guild}.json', 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

    def find_id(self, user_name):
        """
        이름 ->고유 id 반환
        :param user_name: 조회할 유저 이름
        :param memebers: 채널 멤버 리스트
        """
        for member in self.members:
            if member.name == user_name:
                return member.id
            if member.nick == user_name:
                return member.id
        return -1

    def find_name(self, user_id):
        """
        고유 id -> 이름 반환
        :param user_id: 조회할 유저 id
        :param members: 채널 멤버 리스트
        """
        user_id = int(user_id)
        for member in self.members:
            if member.id == user_id:
                return member.name
        return -1
    
    def find_point(self, user_id):
        """포인트 조회"""
        data = self.load_data()
        return data[str(user_id)]

    def give_point_for_joining_chennel(self, member, data):
        """
        멤버에게 채널 참여 포인트를 줍니다
        :param member: 참여 멤버
        :param data: 채널 참여 로그 data
        """
        member_id = member.id

        # 최신 로그 추출
        before = data[str(len(data)-2)]
        after = data[str(len(data)-1)]

        # in -> out : 보이스 채널에서 나갔다면
        if (before[2] == 'in' and after[2] == 'out') and\
                (before[1] == after[1]):
            before_time = datetime.datetime.strptime(before[0], self.date_format)
            after_time = datetime.datetime.strptime(after[0], self.date_format)

            diff_time = (after_time - before_time).seconds // 60        # 분 단위로 환산
            
            # 10분마다 점수 주기
            score = (diff_time//10) * self.join_point
            
            # json data에 반영
            if (score > 0):
                guild_data = self.load_data(member.guild.name)
                guild_data[str(member_id)] += score
                self.save_data(guild_data, member.guild.name)
                return (f"{member.name}님 {diff_time}분간 참여로 {score} 포인트 획득!!")

        return -1

    def create_toto(self, member, title, choice):
        """
        배팅 시스템을 만듭니다
        """
        try:
            # 주최자인지 비교
            data = self.load_data("toto")
            member_id = member.id

            if (data["author"] != member_id): return '이미 만들어진 배팅 시스템이 있습니다. !토토종료 명령어를 호출하세요'

            # 새로 파일을 만듭니다
            data = {}
            data["author"] = member_id
            data["date"] = datetime.datetime.now().strftime(self.date_format)
            data["title"] = title
            data["choice1"] = choice[0]
            data["choice2"] = choice[1]
            data["isbetting"] = 1
            data["log"] = []
            
            self.save_data(data, 'toto')

            return 1
        except:
            # 새로 파일을 만듭니다
            member_id = member.id
            data = {}
            data["author"] = member_id
            data["date"] = datetime.datetime.now().strftime(self.date_format)
            data["title"] = title
            data["choice1"] = choice[0]
            data["choice2"] = choice[1]
            data["isbetting"] = 1
            data["log"] = []
            
            self.save_data(data, 'toto')
            return 1
    
    def betting(self, member, choice, point):
        """
        선택지에 배팅합니다
        """
        try:
            member_id = member.id
            point_amount = self.find_point(member_id)
            choice = int(choice)
            point = int(point)

            if (point_amount < point):
                return f'잔액이 부족합니다. 현재 소지하신 포인트는 {point_amount}입니다.'
            else:
                if not (choice == 1 or choice == 2): return '선택지는 1 또는 2만 가능합니다'
                
                # DB load
                toto_data = self.load_data("toto")

                # 배팅 제한 여부 확인
                if (toto_data['isbetting'] == 0): return '주최자가 배팅을 제한하였습니다' 

                # 배팅 기록
                prebetting = False          # 이전에 배팅했는지 여부
                idx = 0                     # toto_data['log'] 인덱스
                for t_member, t_choice, t_point in toto_data['log']:
                    # 다른 선택지에 배팅 제한
                    if (t_member == member_id and t_choice != choice): 
                        return '다른 곳에 배팅할 수 없습니다.'
                    
                    # 추가 배팅
                    elif (t_member == member_id and t_choice == choice):
                        toto_data['log'][idx][2] += point
                        prebetting = True
                    
                    idx += 1

                # 신규 배팅 유저를 기록
                if not prebetting: toto_data['log'].append([member_id, choice, point])

                # 포인트 차감
                point_amount -= point
                point_data = self.load_data()
                point_data[str(member_id)] = point_amount

                # DB save
                self.save_data(point_data)
                self.save_data(toto_data, 'toto')

                return f'{member.name}님이 {toto_data["choice"+str(choice)]}에 {point} 포인트를 배팅하셨습니다.'
        except:
            return '잘못 입력하셨습니다'

    def end_toto(self, member, result_choice):
        """
        토토 시스템을 종료하고 포인트를 정산합니다
        """
        try:
            toto_data = self.load_data('toto')

            member_id = member.id
            result_choice = int(result_choice)

            # 주최자인지 확인
            if (member_id == toto_data['author']):
                # 선택지가 1이나 2가 아니라면 종료
                if not (result_choice == 1 or result_choice == 2): return '선택지는 1 또는 2만 선택가능합니다'

                # 포인트 정산
                point_data = self.load_data()
                c1, c2 = self.view_toto()
                c = c1 if result_choice == 1 else c2        # 최종 결과 선택지
                
                mes = f'최종 결과 {toto_data["choice"+str(result_choice)]}을(를) 선택한 사람들이 포인트를 획득합니다'
                for t_member, t_choice, t_point in toto_data['log']:
                    if (t_choice == result_choice):
                        get_point = int(t_point * c[2])           # 획득 포인트 = point * 배당
                        point_data[str(t_member)] += get_point
                        mes += f'{self.find_name(t_member)}님 {get_point}포인트 획득!\n'
                
                # json 파일 저장
                self.save_data(point_data)
                with open("./data/toto.json", "w") as f:
                    json.dump("", f)

                return mes
            else:
                # 다른 사람이지만 60분이 지나면 초기화 시킬 수 있습니다
                mes = f'이미 토토를 {toto_data["author"]}님이 만드셨습니다. 60분이 지나면 다른 분이 초기화 시킬 수 있습니다.'
                
                date = datetime.datetime.strptime(toto_data["date"], self.date_format)
                # 직역하면 '시작날짜+60분 후'보다 '지금'이 더 미래니? 
                if (date + datetime.timedelta(minutes=60) <=\
                        datetime.datetime.now()):
                    mes = '토토 종료. 주최자 이외의 사람이 종료하였기에 배팅 무산'

                    # DB load
                    point_data = self.load_data()
                    toto_data = self.load_data('toto')

                    # 토토에 참여한 사람들 포인트 돌려받기
                    for t_member, t_choice, t_point in toto_data['log']:
                        point_data[str(t_member)] += t_point

                    # DB save
                    self.save_data()
                    self.save_data('', 'toto')
                    
                return mes
        except:
            return -1

    def end_betting(self, member):
        """
        추가 배팅을 제한합니다
        """
        try: 
            toto_data= self.load_data('toto')
            member_id = member.id
            # 주최자인지 확인
            if member_id == toto_data['author']:
                toto_data['isbetting'] = 0          # 배팅 제한
                self.save_data(toto_data, 'toto')

                return '배팅을 제한합니다. 이후 배팅을 하실 수 없습니다. 아예 배팅시스템을 종료하려면 !토토종료 [최종선택지] 명령어로 호출해주세요.'
            
            return '주최자만 배팅을 제한할 수 있습니다'
        except:
            return -1

    def view_toto(self):
        """
        토토 현재 상황을 볼 수 있습니다.
        """
        try:
            toto_data = self.load_data("toto")

            choice1 = 0                 # 선택지1 누적 포인트
            max_choice1 = ["", 0]       # 선택지1 최대 기여자 및 포인트
            choice2 = 0                 # 선택지2 누적 포인트
            max_choice2 = ["", 0]       # 선택지2 최대 기여자 및 포인트

            # 배팅 기록을 확인하여 변수에 값 입력
            for t_member, t_choice, t_point in toto_data['log']:
                if (t_choice == 1):
                    if (max_choice1[1] < t_point):
                        max_choice1[0] = self.find_name(t_member)
                        max_choice1[1] = t_point
                    choice1 += t_point
                else:
                    if (max_choice2[1] < t_point):
                        max_choice2[0] = self.find_name(t_member)
                        max_choice2[1] = t_point
                    choice2 += t_point

            # 배당 구하기
            total = choice1 + choice2                                                   # 전체 배팅 포인트
            choice1_rate = int(choice1/total * 100) if total != 0 else 0                # 선택지1 포인트 비율
            choice2_rate = int(choice2/total * 100) if total != 0 else 0                # 선택지2 포인트 비율
            choice1_dividend = round(total/choice1, 3) if choice1 != 0 else 0           # 선택지1 포인트 배당
            choice2_dividend = round(total/choice2, 3) if choice2 != 0 else 0           # 선택지2 포인트 배당

            # 총 포인트, 비율, 배당, 최대투자자, 최대투자금
            choice1_result = (choice1, choice1_rate, choice1_dividend, max_choice1[0], max_choice1[1])
            choice2_result = (choice2, choice2_rate, choice2_dividend, max_choice2[0], max_choice2[1])

            return choice1_result, choice2_result
        except:
<<<<<<< HEAD
            return -1
=======
            return -1
>>>>>>> 402cf0814d786fe8df43f91c23d10164e8ec2ec2
