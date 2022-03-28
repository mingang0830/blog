from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from board.models import Board
from board.forms import WritePost, UpdatePost, UserForm, LoginForm


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
        return render(request, 'board/index.html', {"board_data": result})


def detail(request, id):
    if request.method == "GET": 
        post_from_id = Board.objects.get(pk=id)
        return render(request, 'board/detail.html', {'detail': post_from_id})


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


def remove_post(request, id):
    post_from_id = Board.objects.get(pk=id)
    if request.method == "GET":
        post_from_id.delete()
        return redirect('/board/')


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

