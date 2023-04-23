from django.urls import path
from articles import views
from articles.models import LikeDislike, Question, Answer

app_name = 'articles'
urlpatterns = [
	path('', views.index, name='Cat In Hat'),
	path('ask/', views.ask_question, name='ask'),
	path('question/<int:question_id>', views.display_single, name='display_single'),
	path('tags/<int:tag_id>', views.tags_list, name='tags_list'),
	path('ajax/vote/', views.vote, name="vote")
]


