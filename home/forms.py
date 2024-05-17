from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    created_at = forms.DateTimeField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Comment
        fields = ['comment']
        error_messages = {
            'comment': {'required': 'Vui lòng điền nội dung bình luận.'}
        }



class ReplyForm(forms.Form):
    reply = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nhập phản hồi của bạn'}))