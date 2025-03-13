from django import forms
from .models import Comment
from .models import Book


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]  # 只允许提交评论内容字段

        content = forms.CharField(
            widget=forms.Textarea(
                attrs={"placeholder": "请输入评论...", "rows": 5, "cols": 40}
            ),
            required=False,  # 让 content 字段变为可选字段
        )


def __init__(self, *args, **kwargs):
    super(CommentForm, self).__init__(*args, **kwargs)
    self.fields["content"].widget = forms.Textarea(
        attrs={"class": "form-control", "rows": 3, "placeholder": "写一条评论"}
    )


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'genre', 'cover_image']  # 选择要展示的字段
