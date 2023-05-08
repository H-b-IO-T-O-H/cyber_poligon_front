from django import forms


class PostForm(forms.Form):
    title = forms.CharField(label='Заголовок', max_length=255)
    text = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'rows': '3'}))
    tags = forms.CharField(label="Тэги", required=False, max_length=50)
    pinned = forms.BooleanField(label="Закрепить", required=False)

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if tags:
            tags.split()
        return tags

    def clean_text(self):
        text = self.cleaned_data['text']
        return text

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_pinned(self):
        return self.cleaned_data['pinned']


class CommentForm(forms.Form):
    text = forms.CharField(label='Your comment', widget=forms.Textarea(attrs={'rows': '3'}))

    def clean(self):
        return self.cleaned_data
