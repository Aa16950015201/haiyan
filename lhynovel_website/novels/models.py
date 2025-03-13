from django.db import models  # type: ignore

# from .models import
# Chapter,Comment
from django.contrib.auth.models import User  # type: ignore


# 小说分类模型
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="分类名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "小说分类"
        verbose_name_plural = "小说分类"


# 小说模型
class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="书名")
    author = models.CharField(max_length=100, verbose_name="作者")
    description = models.TextField(verbose_name="描述")
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name="分类"
    )  # 外键关联分类
    cover_image = models.ImageField(
        upload_to="image/", null=True, blank=True, verbose_name="封面图片"
    )  # 封面图片
    created_at = models.DateField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "小说"
        verbose_name_plural = "小说"


# 章节模型
class Chapter(models.Model):
    book = models.ForeignKey(
        Book, related_name="chapters", on_delete=models.CASCADE, verbose_name="书籍"
    )
    title = models.CharField(max_length=200, verbose_name="章节标题")
    content = models.TextField(verbose_name="章节内容")
    order = models.IntegerField(
        default=1, verbose_name="章节顺序"
    )  # 章节顺序 默认从1开始，也可以选择其他默认值
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return f"Chapter{self.order}:{self.title}"

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = "章节"


# 评论模型
class Comment(models.Model):
    book = models.ForeignKey(
        Book,
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name="书籍",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    content = models.TextField(verbose_name="评论内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return f"Comment by{self.user.username} on {self.book.title}"

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"


# 存储用户和书籍的关系，表示哪些书籍用户已经添加到书架
class UserBook(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="用户"
    )  # 关联到用户
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name="书籍"
    )  # 关联到书籍
    added_at = models.DateTimeField(
        auto_now_add=True, verbose_name="添加时间"
    )  # 书籍添加到书架的时间
    # 你可以根据需要加入其他字段，比如书籍的状态（正在阅读、已完成、已收藏等）
    STATUS_CHOICES = (
        ("reading", "正在阅读"),
        ("completed", "已完成"),
        ("favorite", "已收藏"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="reading")

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    class Meta:
        verbose_name = "用户书籍关系"
        verbose_name_plural = "用户书籍关系"
