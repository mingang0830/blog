from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import DetailView
from django.core.paginator import Paginator

from board.models import Board, Comment
from board.forms import SubCommentForm, WritePost, UpdatePost, UserForm, LoginForm, CommentForm


def index_page(request):
    return render(request, 'board/index.html')

def board_list(request): # 클라이언트가 보낸것
    if request.method == "GET": # 클라이언트가 요청한 method
        board_list = Board.objects.all().order_by('-created_at')
        paginator = Paginator(board_list, 5)
        page = request.GET.get('page', 1)
        page_obj = paginator.get_page(page)
        return render(request, 'board/list.html', {'page_obj': page_obj})

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

# class DetailView(View):

#     def get(self, request, id):
#         board = Board.objects.get(pk=id)
#         comment_form = CommentForm()
#         return render(request, 'board/detail.html', {'detail': board, 'comment_form': comment_form})

#     def delete(self, request, id):
#         board = Board.objects.get(pk=id)
#         board.delete()
#         return redirect('/board/')

def detail(request, id):
    if request.method == "GET": 
        post_from_id = Board.objects.get(pk=id)
        comment_form = CommentForm()
        subcomment_form = SubCommentForm()
        return render(request, 'board/detail.html', {'detail': post_from_id, 'comment_form': comment_form, 'subcomment_form': subcomment_form})

def remove_post(request, id):
    post_from_id = Board.objects.get(pk=id)
    if request.method == "GET":
        post_from_id.delete()
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

def update_post(request, id):
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
            return redirect("/board/signin")
    
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


def new_comment(request, id): 
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.comment = comment_form.cleaned_data['comment']
            comment = comment_form.save()
            comment.post_id = id
            comment.save()

            return redirect(f'/board/{id}')

def delete_comment(request, id, c_id):
    comment_id = Comment.objects.get(pk=c_id)
    if request.method == "GET":
        comment_id.delete()
        return redirect(f'/board/{id}')

def new_subcomment(request, id):
    subcomment_form = SubCommentForm(request.POST)
    if subcomment_form.is_valid():
        subcomment_form.subcomment = subcomment_form.cleaned_data['subcomment']
        subcomment = subcomment_form.save()
        subcomment.post_id = id
        subcomment.parent_comment_id = request.POST.get('comment_id')
        subcomment_form.save()
        return redirect(f'/board/{id}')