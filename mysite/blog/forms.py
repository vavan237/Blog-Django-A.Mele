from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
	#форма для почты
	name = forms.CharField(max_length = 25)
	email= forms.EmailField()
	to = forms.EmailField()
	comments = forms.CharField(required=False, widget = forms.Textarea)


class CommentForm(forms.ModelForm):
	#форма для комментов
	class Meta:
		model = Comment
		fields = ('name', 'email', 'body')