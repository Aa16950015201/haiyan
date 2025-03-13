from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

# from .templates.novels import views
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("home/",RedirectView.as_view(url='/')),
    path("login/", views.user_login, name="login"),
    path(
        "accounts/", include("django.contrib.auth.urls")
    ),  # 引入 Django 内置认证系统的 URL 配置
    path("book/<int:book_id>/", views.book_detail, name="book_detail"),
    path("books/<int:book_id>/comment/", views.add_comment, name="add_comment"),
    path(
        "book/<int:book_id>/add_to_bookshelf/",
        views.add_to_bookshelf,
        name="add_to_bookshelf",
    ), 
    #移除出书架
    path('book/<int:book_id>/remove_from_bookshelf/', views.remove_from_bookshelf, name='remove_from_bookshelf'),
      # 添加到书架" 的功能定义一个 URL 路由。
    path("my-books/", views.my_books, name="my_books"),
    # 其他路由
    # path("login/", auth_views.LoginView.as_view(), name="login"),
    path("chapter/<int:id>/", views.chapter_read, name="chapter_read"),  
    # 章节的详情
    # path("genres/<int:id>/", views.genres, name="genres"),  # 使用视图函数名而不是模型名
    # 删除评论
    # path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment),
    path("comment/add/<int:book_id>/", views.add_comment),
    path("comment/delete/<int:id>/", views.delete_comment, name="delete_comment"),
    # 编辑评论
    path("edit_comment/<int:id>/", views.edit_comment, name="edit_comment"),
    #寻找书籍
    path('search/', views.search_books, name='search_books'),
     # 添加这个路由来匹配 genres/ 路径
    path('genres/', views.genre_list, name='genre_list'),  # 假设你有一个用于展示所有分类的视图
    path('genre/<int:genre_id>/', views.genre_detail, name='genre_detail'),

    # 书籍增删改查
    path('books/', views.book_list, name='book_list'),  # 显示所有书籍
    path('books/add/', views.book_create, name='book_create'),  # 添加新书籍
    path('books/<int:id>/edit/', views.book_edit, name='book_edit'),  # 编辑书籍
    path('books/<int:id>/delete/', views.book_delete, name='book_delete'),  # 删除书籍
    #登录页
    # path('login/', views.login, name='login'),  # 登录处理
    #   # 添加这个配置
    # path('accounts/profile/', views.profile_view, name='profile_view'),

]
