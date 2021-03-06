# Discord_VoteBot
Discord_VoteBot은 디스코드 서버 멤버들이 좀 더 다양하고 유용한 활동을 할 수 있게 파이썬 디스코드 API를 활용하여 개발하였습니다. 투표 기능 이외에 새로운 기능들을 추가할 계획이기에 피드백 및 문의사항은 [Issues](https://github.com/gagip/Discord_VoteBot/issues)에 게시해주시기 바랍니다.



## Features

- 롤자랭 구현
- 롤전적 구현 (개발 완료, 디버깅 작업)
- 투표 구현 (개발 완료, 업데이트 중)
- 후원 시스템
- tts 시스템 (개발예정)
- 배팅 시스템 (임시 개발 완료, 홈페이지 기능 추가 예정)

## Setting

### Requirements

- python 3.6버전 이상
- discord 계정



### Discord App 생성

https://blog.naver.com/wpdus2694/221192640522 에서 설명이 잘 되어 있으니 참고바랍니다. 



### Clone or Download

명령 프롬포트에 해당 코드를 입력하거나 Clone or download 버튼을 눌러 Zip 파일을 다운받아주세요.

```
git clone https://github.com/gagip/Discord_VoteBot.git
```



## Execution

### token.txt 만들기

해당 봇을 연결하기 위해 자신의 계정 토큰을 세팅할 필요가 있습니다. token은 개인 정보라 공개된 장소에 업로드하면 안 되기 때문에 github에서는 token.txt를 업로드하지 않았습니다.  (.gitignore에서 설정)

여러분들의 토큰은 디스코드 개발자 홈페이지에 접속한 뒤 SETTINGS - Bot 에 들어가 Copy 버튼을 클릭하시면 토큰이 복사됩니다. 

![image](https://user-images.githubusercontent.com/27941099/83189182-cb251880-a16b-11ea-86cd-61f6f8e23e85.png)

그 다음 Discord_VoteBot 경로로 들어가 새로 token.txt 파일을 만들어주고, 텍스트 파일 안에 토큰을 붙여넣어주시면 됩니다.

![image](https://user-images.githubusercontent.com/27941099/103454230-3e57c400-4d25-11eb-83ae-88e4390c7165.png)

 Gateway Intents라는 항목이 생겼습니다. 두 가지 항목을 다 체크해주세요. 체크하지 않으면 나중에 요청 결과가 원활히 이뤄지지 않습니다. 
