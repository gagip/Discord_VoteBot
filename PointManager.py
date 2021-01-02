import json
import discord, asyncio
from discord.ext import commands

import datetime

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
    
    def load_data(self):
        '''json 파일 불러오기'''
        try:
            with open(f"./data/{self.ctx.guild}.json", "r") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            self.init_data()

    def save_data(self, data):
        '''
        json 파일 쓰기
        :param data: 작성할 데이터
        '''
        with open(f"./data/{self.ctx.guild}.json", "w") as json_file:
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