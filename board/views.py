from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import DetailView

from board.models import Board, Comment
from board.forms import WritePost, UpdatePost, UserForm, LoginForm, CommentForm


def board_list(request): # 클라이언트가 보낸것
    if request.method == "GET": # 클라이언트가 요청한 method
        result = []
        for board in Board.objects.all():
            result.append({
                "id": board.id,
                "title": board.title,
                "user": board.created_by,
                "created_at": board.created_at
            })
        return render(request, 'board/index.html', {"board_data": result})


# def detail(request, id): # GET / POST / PUT / DELETE (detail read, detail insert, detail edit, detail delete)
#     board = Board.objects.get(pk=id)
#     if request.method == "GET": 
#         comment_form = CommentForm()
#         return render(request, 'board/detail.html', {'detail': board, 'comment_form': comment_form})
#     elif request.method == "PUT":
#         form = UpdatePost(instance=board)
#         return render(request, 'board/edit.html', {'detail': form})
#     elif request.method == "DELETE":
#         board.delete()
#         return redirect('/board/')

class DetailView(View):

    def get(self, request, id):
        board = Board.objects.get(pk=id)
        comment_form = CommentForm()
        return render(request, 'board/detail.html', {'detail': board, 'comment_form': comment_form})

    def delete(self, request, id):
        board = Board.objects.get(pk=id)
        board.delete()
        return redirect('/board/')


def write(request):
    write_post_form = WritePost(request.POST or None)
    if request.method == "POST":      
        if write_post_form.is_valid():
            Board.objects.create(
                title = write_post_form.cleaned_data['title'],
                content = write_post_form.cleaned_data['content'],
                created_by = request.user,
            )
            return redirect('/board/')
    return render(request, 'board/write.html', {'write_form': write_post_form})

def edit_post(request, id):
    post = Board.objects.get(pk=id)
    if request.method == "POST":
        update_post_form = UpdatePost(request.POST)
        if update_post_form.is_valid():
            post.title = update_post_form.cleaned_data["title"]
            post.content = update_post_form.cleaned_data["content"]       
            post.save()
        return redirect(f'/board/{post.id}')
    form = UpdatePost(instance=post)
    return render(request, 'board/edit.html', {'detail': form})


def signup(request):
    user_form = UserForm(request.POST or None)
    if request.method == 'POST':
        if user_form.is_valid():
            user_form.save()
            return redirect("/board/login")
    
    return render(request, 'board/signup.html', {'user_form': user_form})


def signin(request):
    login_form = LoginForm(request.POST or None)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/board/')
        else:
            return HttpResponse("로그인 실패. 다시 시도해 주세요.")
    return render(request, 'board/signin.html', {'login_form': login_form})


def signout(request):
    logout(request)
    return redirect('/board/')


def comment(request, id): 
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.comment = comment_form.cleaned_data['comment']
            comment = comment_form.save()
            comment.post_id = id
            comment.save()

            return redirect(f'/board/{id}')
