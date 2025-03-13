from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Chapter, Comment, Genre, UserBook
from django.http import HttpResponseForbidden

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import CommentForm,BookForm # 修改视图来使用表单
from django.db.models import Q #全局的搜索视图函数
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm



def profile_view(request):
    # 假设你有用户模型和资料需要展示
    return render(request, 'novels/my_books.html')  # 你可以根据需要修改模板路径



# 首页视图 展示所有小说
def home(request):
    # 获取最新的5本书籍
    latest_books = Book.objects.all().order_by("-created_at")[:6]
    # 获取热门书籍（按评论数量排序，可以根据需要更改排序逻辑）
    popular_books = Book.objects.annotate(num_comments=Count("comments")).order_by(
        "-num_comments"
    )[:4]
    # 获取所有书籍分类
    genres = Genre.objects.all()
    books = Book.objects.all()
    # 推荐书籍（根据用户历史书籍）
    recommended_books = []
    if request.user.is_authenticated:
        # 推荐用户最近添加到书架的书籍
        user_books = UserBook.objects.filter(user=request.user).order_by("-added_at")[
            :5
        ]
        recommended_books = [ub.book for ub in user_books]

    return render(
        request,
        "novels/home.html",
        {
            "latest_books": latest_books,
            "popular_books": popular_books,
            "genres": genres,
            "recommended_books": recommended_books,
        },
    )


# 小说详情视图，展示小说信息和章节列表
def book_detail(request, book_id):
    comment_id = request.GET.get('comment_id')
    book = get_object_or_404(Book, id=book_id)
    chapters = book.chapters.all().order_by("order")
    comments = book.comments.all().order_by("-created_at")  # 按照创建时间倒序排序评论
     # 检查当前用户是否已经将书籍添加到书架
    book_in_shelf = UserBook.objects.filter(user=request.user, book=book).exists() if request.user.is_authenticated else False
    
    # 如果 comment_id 不为空，表示是修改评论
    if comment_id:
        comment = get_object_or_404(Comment, id=comment_id, book=book)
        # 如果当前用户不是该评论的作者，禁止修改
        if comment.user != request.user:
            return HttpResponseForbidden("你没有权限修改这个评论。")
        form = CommentForm(request.POST or None, instance=comment)
    else:
        # form = CommentForm(request.POST or None)
        form = CommentForm()
    return render(
        request,
        "novels/book_detail.html",
        {
            "book": book,
            "chapters": chapters,
            "comments": comments,
            "form": form,
            "comment_id": comment_id,  # 传递 comment_id 来决定是编辑还是新增评论
            "book_in_shelf": book_in_shelf,
        },
    )

# 章节阅读视图，展示章节内容
def chapter_read(request, chapter_id):  # # 这里的 chapter_id 是接收 URL 中传递的参数
    chapter = get_object_or_404(Chapter, id=chapter_id)
    return render(request, "chapter_read.html", {"chapter": chapter})


# 添加评论视图
@login_required(login_url='/login/')
def add_comment(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        content = request.POST.get("content")
        Comment.objects.create(book=book, user=request.user, content=content)
    # return redirect("novels/book_detail.html", book_id=book_id)
    return redirect(f"/book/{book_id}")


# 删除评论
@login_required
def delete_comment(request, id):
    if request.user.is_authenticated:
        # user = request.user
        comment = get_object_or_404(Comment, pk=id)
        if request.user == comment.user:
            book_id = comment.book.id  # 获取关联的书籍ID
            comment.delete()
       
    return redirect(f"/book/{book_id}")
   

@login_required
def edit_comment(request, id):
    comment = get_object_or_404(Comment, pk=id)

    # 检查 book_id 是否存在
    book_id = comment.book.id if comment.book else None

    if request.user != comment.user:
        return redirect("book_detail", book_id=comment.book.id)  # 或者返回错误信息

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()  # 保存评论修改
            return redirect("book_detail", book_id=comment.book.id)
    else:
        form = CommentForm(instance=comment)
        
    return redirect(f"/book/{book_id}")
 


# 小说分类视图
# 用户点击某个分类时，展示该分类下的所有书籍。
def genres(request, id):
    genre = Genre.objects.get(id=id)
    books_in_genre = Book.objects.filter(genre=genre)
    genre_list = Genre.objects.all()
    return render(
        request,
        "novels/genres.html",
        {"genre": genre, "books_in_genre": books_in_genre},
    )


@login_required
def my_books(request):
    # 获取当前用户添加到书架上的所有书籍
    user_books = UserBook.objects.filter(user=request.user)  # 获取当前用户的书架书籍
    books = [user_book.book for user_book in user_books]  # 提取出书籍对象
    return render(request, "novels/my_books.html", {"books": books})


# 书籍详情页添加一个“添加到书架”的功能
@login_required
def add_to_bookshelf(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # 检查用户是否已经添加过这本书
    if not UserBook.objects.filter(user=request.user, book=book).exists():
        UserBook.objects.create(user=request.user, book=book)
    return redirect("book_detail", book_id=book.id)
# 从书架移除
@login_required
def remove_from_bookshelf(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # 确保书籍已经在用户书架中
    user_book = UserBook.objects.filter(user=request.user, book=book).first()
    if user_book:
        user_book.delete()
    return redirect("book_detail", book_id=book.id)



# 分类页视图
def genre_list(request):
    # 获取所有分类
    genres = Genre.objects.all()

    context = {
        'genres': genres,
    }

    return render(request, 'novels/genre_list.html', context)

# 分类详情页，展示该分类下的所有小说
def genre_detail(request, genre_id):
    # 获取特定分类
    genre = Genre.objects.get(id=genre_id)
    # 获取该分类下的所有小说
    books = Book.objects.filter(genre=genre)
    context = {
        'genre': genre,
        'books': books,
    }

    return render(request, 'novels/genre_detail.html', context)
#显示所有书籍
def book_list(request):
    books=Book.objects.all() #获取所有书籍
    if not Book.cover_image:
            Book.cover_image = None  # 确保没有封面图的书籍不会抛出错误
    return render(request, 'novels/book_list.html', {'books': books})

# 添加新书籍
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)  # 获取表单数据
        if form.is_valid():
            form.save()  # 保存到数据库
            return redirect('book_list')  # 添加完成后跳转到书籍列表页面
    else:
        form = BookForm()
    return render(request, 'novels/book_form.html', {'form': form})

# 编辑书籍
def book_edit(request, id):
    book = get_object_or_404(Book, id=id)  # 获取书籍对象
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)  # 获取编辑表单
        if form.is_valid():
            form.save()  # 保存修改
            return redirect('book_list')  # 修改完成后跳转到书籍列表页面
    else:
        form = BookForm(instance=book)
    return render(request, 'novels/book_form.html', {'form': form})

# 删除书籍
def book_delete(request, id):
    book = get_object_or_404(Book, id=id)  # 获取要删除的书籍
    if request.method == 'POST':
        book.delete()  # 删除书籍
        return redirect('book_list')  # 删除完成后跳转到书籍列表页面
    return render(request, 'novels/bookdelete.html', {'book': book})
#查书籍
def search_books(request):
    query = request.GET.get('q', '')  # 获取搜索关键字

    if query:
        # 在书籍标题、作者或描述中进行模糊查询
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(description__icontains=query)
        )
    else:
        books = Book.objects.none()  # 如果没有搜索关键字，则返回空列表

    return render(request, 'novels/search_results.html', {
        'query': query,
        'books': books
    })



# 这是处理登录页面的视图函数
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # 获取用户并登录
            user = form.get_user()
            login(request, user)
            # 登录成功后跳转到 'home' 或者你想跳转的首页 URL
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'novels/login.html', {'form': form})