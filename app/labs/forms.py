from django import forms


class LabForm(forms.Form):
    title = forms.CharField(label='Заголовок', max_length=255)
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'rows': '2'}), required=False)
    script = forms.CharField(label='Исполняемый скрипт', widget=forms.Textarea(attrs={'rows': '5'}), required=False)
    pinned = forms.BooleanField(label="Добавить ссылку на пост", required=False)
    linked_post = forms.IntegerField(disabled=True, required=False)

    def clean_pinned(self):
        return self.cleaned_data['pinned']

    def clean_description(self):
        return self.cleaned_data['description']

    def clean_title(self):
        return self.cleaned_data['title']

    def clean_linked_post(self):
        return self.cleaned_data['linked_post']
