import json
import discord, asyncio
import os
from discord.ext import commands

import datetime

path = os.path.dirname(os.path.abspath(__file__))

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
        self.join_point = 50
        self.date_format = "%Y/%m/%d %H:%M"

    def set_ctx(self, ctx):
        self.ctx = ctx
        self.members = self.ctx.guild.members
    
    def get_ctx(self):
        print(self.ctx)

    def init_data(self):
        '''
        채널 멤버 포인트 DB 생성 (json)
        '''
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
        
        with open(f"./data/{self.ctx.guild}.json", "w") as json_file:
            json.dump(data, json_file, indent=4, sort_keys=True)
            print("완료")

    def reset_data(self, year, month):
        '''
        한달마다 포인트 DB 초기화
        :param year: 기존 파일 작성 년도
        :param month: 기존 파일 작성 월
        '''
        # DB 최신 작성 날짜가 한 달 이상 지났는지 확인
        today = datetime.datetime.today()
        if not (today.year == year and today.month == month):
            init_data(self.ctx)      # DB 초기화
    
    def load_data(self, guild=None):
        '''json 파일 불러오기'''
        if guild is None: guild = self.ctx.guild
        try:
            with open(f"./data/{guild}.json", "r") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            # TODO 임시로 해놨는데 고치기
            if guild != "toto":
                self.init_data()

    def save_data(self, data, guild=None):
        '''
        json 파일 쓰기
        :param data: 작성할 데이터
        '''
        if guild is None: guild = self.ctx.guild
        with open(f"./data/{guild}.json", "w") as json_file:
            json.dump(data, json_file, indent=4, sort_keys=True)

    def find_id(self, user_name):
        '''
        이름 ->고유 id 반환
        :param user_name: 조회할 유저 이름
        :param memebers: 채널 멤버 리스트
        '''
        for member in self.members:
            if member.name == user_name:
                return member.id
            if member.nick == user_name:
                return member.id
        return -1

    def find_name(self, user_id):
        '''
        고유 id -> 이름 반환
        :param user_id: 조회할 유저 id
        :param members: 채널 멤버 리스트
        '''
        user_id = int(user_id)
        for member in self.members:
            if member.id == user_id:
                return member.name
        return -1
    
    def find_point(self, user_id):
        data = self.load_data()
        return data[str(user_id)]

    def give_point_for_joining_chennel(self, member, data):
        '''
        멤버에게 채널 참여 포인트를 줍니다
        :param member: 참여 멤버
        :param data: 채널 참여 로그 data
        '''
        # 현재 보이스톡 
        member_id = member.id

        before = data[str(len(data)-2)]
        after = data[str(len(data)-1)]

        if (before[2] == "in" and after[2] == "out") and\
                (before[1] == after[1]):
            before_time = datetime.datetime.strptime(before[0], "%Y/%m/%d %H:%M")
            after_time = datetime.datetime.strptime(after[0], "%Y/%m/%d %H:%M")

            diff_time = (after_time - before_time).seconds // 60
            
            # 30분마다 점수 주기
            score = (diff_time//30) * self.join_point
            
            # json data에 반영
            if (score > 0):
                guild_data = self.load_data(member.guild.name)
                guild_data[str(member_id)] += score
                self.save_data(guild_data, member.guild.name)
                return (f"{member.name}님 {diff_time}분간 참여로 {score} 포인트 획득!!")

        return -1

    def create_toto(self, member_id, title, choice):
        '''
        놀이터를 만듭니다
        '''
        try:
            if os.path.exists(path+"/data/toto.json"):
                data = self.load_data("toto")
                if (data["author"] != member_id): return

            # 새로 파일을 만듭니다
            with open(f"./data/toto.json", "w") as f:
                data = {}
                data["author"] = member_id
                data["date"] = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
                data["title"] = title
                data["choice1"] = choice[0]
                data["choice2"] = choice[1]
                data["isbetting"] = 1
                data["log"] = []
                json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)
        except:
            # 새로 파일을 만듭니다
            with open(f"./data/toto.json", "w") as f:
                data = {}
                data["author"] = member_id
                data["date"] = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
                data["title"] = title
                data["choice1"] = choice[0]
                data["choice2"] = choice[1]
                data["isbetting"] = 1
                data["log"] = []
                json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)
    
    def betting(self, member_id, choice, point):
        '''
        선택지에 배팅합니다
        '''
        point_amount = self.find_point(member_id)
        choice = int(choice)
        point = int(point)
        if (point_amount < point):
            return f"잔액이 부족합니다. 현재 소지하신 포인트는 {point_amount}입니다."
        else:
            if not (choice == 1 or choice == 2): return
            # 배팅 기록 저장
            toto_data = self.load_data("toto")
            if (toto_data["isbetting"] == 0): return f"주최자가 배팅을 제한하였습니다" 

            for t_member, t_choice, t_point in toto_data["log"]:
                if (t_member == member_id and t_choice != choice): return f"다른 곳에 배팅할 수 없습니다."

            toto_data["log"].append([member_id, choice, point])

            # 배팅 차감
            point_amount -= point
            point_data = self.load_data()
            point_data[str(member_id)] = point_amount
            self.save_data(point_data)

            with open("./data/toto.json", "w") as f:
                json.dump(toto_data, f, indent=4, sort_keys=True, ensure_ascii=False)

            return f"{self.find_name(member_id)}님이 {choice}에 {point} 포인트를 배팅하셨습니다."

    def end_toto(self, member_id, result_choice):
        '''
        놀이터를 종료합니다
        '''
        toto_data = self.load_data("toto")
        result_choice = int(result_choice)

        if (member_id == toto_data["author"]):
            if not (result_choice == 1 or result_choice == 2): return

            # 포인트 정산
            c1, c2 = self.view_toto()
            point_data = self.load_data()
            c = c1 if result_choice == 1 else c2
            mes = ""
            for member, choice, point in toto_data["log"]:
                if (choice == result_choice):
                    get_point = int(point * c[2])
                    point_data[str(member)] += get_point
                    mes += f"{self.find_name(member)}님 {get_point}포인트 획득!\n"
            self.save_data(point_data)

            with open("./data/toto.json", "w") as f:
                json.dump("", f)
            return mes
        else:
            # 다른 사람이지만 20분이 지나면 초기화 시킬 수 있습니다
            mes = f"이미 토토를 {toto_data['author']}님이 만드셨습니다. 60분이 지나면 다른 분이 초기화 시킬 수 있습니다."
            date = datetime.datetime.strptime(toto_data["date"], self.date_format)
            if (date - datetime.timedelta(minutes=60).seconds > 0):
                mes = "토토 종료. 주최자 이외의 사람이 종료하였기에 배팅 무산"

                # 포인트 돌려주기
                point_data = self.load_data()
                toto_data = self.load_data("toto")
                for member, choice, point in toto_data["log"]:
                    point_data[str(member)] += point

                self.save_data()
                with open("./data/toto.json", "w") as f:
                    json.dump("", f)
                
            return mes

    def end_betting(self, member_id):
        try: 
            toto_data= self.load_data("toto")
            if toto_data["author"] == member_id:
                toto_data["isbetting"] = 0
        except:
            pass

    def view_toto(self):
        '''
        토토 현재 상황을 볼 수 있습니다.
        '''
        toto_data = self.load_data("toto")
        choice1 = 0
        max_choice1 = ["", 0]

        choice2 = 0
        max_choice2 = ["", 0]

        # 데이터에서 합산
        for member, choice, point in toto_data["log"]:
            if (choice == 1):
                if (max_choice1[1] < point):
                    max_choice1[0] = self.find_name(member)
                    max_choice1[1] = point
                choice1 += point
            else:
                if (max_choice2[1] < point):
                    max_choice2[0] = self.find_name(member)
                    max_choice2[1] = point
                choice2 += point

        # 배당 구하기
        total = choice1 + choice2
        choice1_rate = int(choice1/total * 100) if total != 0 else 0
        choice2_rate = int(choice2/total * 100) if total != 0 else 0
        choice1_dividend = total/choice1 if choice1 != 0 else 0
        choice2_dividend = total/choice2 if choice2 != 0 else 0

        # 총 포인트, 비율, 배당, 최대투자자, 최대투자금
        choice1_result = [choice1, choice1_rate, choice1_dividend, max_choice1[0], max_choice1[1]]
        choice2_result = [choice2, choice2_rate, choice2_dividend, max_choice2[0], max_choice2[1]]

        return choice1_result, choice2_result