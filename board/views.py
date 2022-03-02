from django.shortcuts import redirect, render
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
                "writer": board.created_by,
                "created_at": board.created_at
            })
        template = loader.get_template('board/index.html')
        return render(request, 'board/index.html', {"board_data": result})


def detail(request,id):
    if request.method == "GET": 
        post_from_id = Board.objects.get(pk=id)
        return render(request, 'board/detail.html', {'detail': post_from_id})


def write(request):
    if request.method == "POST":
        new_post = Board.objects.create(
            title = request.POST['title'],
            content = request.POST['content'],
            created_by = request.POST['created_by'],
        )
        return redirect('/board/')
    return render(request, 'board/write.html')


def remove_post(request, id):
    post_from_id = Board.objects.get(pk=id)
    if request.method == "GET":
        post_from_id.delete()
        return redirect('/board/')


def edit_post(request, id):
    post_from_id = Board.objects.get(pk=id)
    if request.method == "POST":
        post_from_id.title = request.POST["title"]
        post_from_id.content = request.POST["content"]
        
        post_from_id.save()
        return redirect(f'/board/{post_from_id.id}')
    return render(request, 'board/edit.html', {'detail': post_from_id})
