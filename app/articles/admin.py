from django.contrib import admin
from articles.models import Post, Tag, LikeDislike, Answer

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(LikeDislike)
admin.site.register(Answer)

