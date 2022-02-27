from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

from board.models import Board

# CRUD == create, read, update, delete == sql(insert, select, update, delete) == HTTP(post, get, update, delete)

# request 는 클라이언트가 서버에게 요청한것, 클라이언트 -> 서버
# response 는 서버가 클라이언트에 보낸 것, 서버 -> 클라이언트

# 서버코드

# 클라이언트 -> 서버 -> 클라이언트
# 클라이언트 -req-> 서버 -> db data get -> 서버 -response-> 클라이언트

# 이 request 는 클라이언트에서 온거
# 클라이언트는 단순히 보드의 게시물 리스트를 요청

# 클라이언트 get method로 url 에 요청을 하는거, list를 달라고
# ex. GET https://example.com/board
# 그러면 서버가 이걸 response
"""
[
    {
        "id": id,
        "title": title,
        "created_at": created_at,
        "updated_at": updated_at,
        "created_by": created_by,
    },
    { ... },
    ...
]
"""
# https://example.com/board?id=1 중에 id=1 이 query string이고, 이거는 장고에서 request.GET['id'] 접근가능.

# /board url은 board_list view에 연결될 예정
def board_list(request): # 클라이언트가 보낸것
    if request.method == "GET": # 클라이언트가 요청한 method
        result = []
        for board in Board.objects.all():
            result.append({
                "id": board.id,
                "title": board.title,
            })
        template = loader.get_template('board/index.html')
        return HttpResponse(template.render({"board_data": result}, request))

# 크론 프로그램 예로 들면
# input
# process
# output

# 이거는 다시 말하면
# input 사용자로부터 받은 요청
# process 사용자로부터 받은 요청을 처리하는것
# output 처리한걸 되돌려주는것

# 웨더 크론프로그램에서 input은 날씨를 알려달라는 요청을 하는것
# process 는 기상청 홈페이지에 접근해서 오늘 날씨를 긁어와 모양을 만드는것
# output 은 카카오로 모양 만든걸 전송하는거

# 웹
# input은 클라이언트가 서버로 요청하는것
# process 는 요청한 것을 받아 서버가 처리하는것
# output 은 처리한 걸 respnose 하는것


# view 의 flow : (request -> process -> response)

#def board_list(request): << request 를 받아온것
#    if request.method == "GET": << request 처리 (이 부분은 클라이언트의 요청 method를 구별하기 위함)
#        data = Board.objects.all() << process (디비에서 받아온것; Board는 모델이고 -> 모델은 db table 과 1:1 관계)
#        return data << 여기가 response

# request 객체에는 클라이언트의 요청이 들어가 있음
# 클라이언트(브라우저) <-->|<--> 서버(장고, 프로그램) <-->|<--> db(mysql)
# 크론 프로그램의 경우에는
# 클라이언트(크론) <-->|<--> 서버(ec2의 크론탭내의 프로그램) <-->|<--> db(기상청 웹페이지)

# 클라이언트는 서버에 http://example.com/board/ url로 GET method 요청을 할거임
# 서버는 [{...}] 구조의 json을 내려줄거임

# http://example.com/board/ GET으로 이 url이 브라우저를 통해 요청되면
# http://example.com 서버가 받아서 url routing 을 해줌
# board로 라우팅 (url pattern -> -> 서버내 프로그램 어딘가로..) ("/board", board.as_view)...
# board_list 라는 함수가(위에서 정의한) request 객체에 클라이언트의 요청을 넣어놓고 호출됌
# board_list 라는 함수는 적절한 처리(db 에서 데이터를 가져와)한 뒤 return
# 이 return 은 response 로 처리되어 브라우저로 반환됌
