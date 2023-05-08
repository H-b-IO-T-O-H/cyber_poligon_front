from django.urls import path
from articles import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'articles'
urlpatterns = [
	path('', views.index, name='10-ka Labs'),
	path('new_post/', views.new_post, name='new_post'),
	path('post/<int:post_id>', views.display_single, name='display_single'),
	path('get_posts/', views.get_posts, name='get_posts'),
	path('tags/<int:tag_id>', views.tags_list, name='tags_list'),
	path('ajax/vote/', views.vote, name="vote"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



