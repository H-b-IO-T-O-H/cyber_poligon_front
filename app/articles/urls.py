from django.urls import path
from articles import views
from articles.models import LikeDislike, Post, Answer

app_name = 'articles'
urlpatterns = [
	path('', views.index, name='Cat In Hat'),
	path('new_post/', views.new_post, name='new_post'),
	path('post/<int:post_id>', views.display_single, name='display_single'),
	path('tags/<int:tag_id>', views.tags_list, name='tags_list'),
	path('ajax/vote/', views.vote, name="vote")
]


