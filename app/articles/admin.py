from django.contrib import admin
from articles.models import Question, Tag, LikeDislike, Answer

admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(LikeDislike)
admin.site.register(Answer)

