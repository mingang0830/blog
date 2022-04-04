"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from board.views import board_list, detail, remove_post, write, edit_post, signup, signin, signout, new_comment

urlpatterns = [
    path('admin/', admin.site.urls),
    path('board/', board_list),
    path('board/<int:id>', detail),
    path('board/write', write),
    path('board/<int:id>/remove', remove_post),
    path('board/<int:id>/edit', edit_post),
    path('board/signup', signup),
    path('board/signin', signin),
    path('board/logout', signout),
    path('board/new_comment/<int:id>', new_comment)
]
