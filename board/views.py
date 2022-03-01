from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

from board.models import Board


def board_list(request): # 클라이언트가 보낸것
    if request.method == "GET": # 클라이언트가 요청한 method
        result = []
        for board in Board.objects.all():
            result.append({
                "id": board.id,
                "title": board.title,
                "writer": board.created_by
            })
        template = loader.get_template('board/index.html')
        return render(request, 'board/index.html', {"board_data": result})

def detail(request,id):
    if request.method == "GET": 
        content_from_id = Board.objects.get(pk=id)
        return render(request, 'board/detail.html', {'detail': content_from_id})

