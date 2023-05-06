from django.urls import path
from articles import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'articles'
urlpatterns = [
	path('', views.index, name='10-ka Labs'),
	path('new_post/', views.new_post, name='new_post'),
	path('labs_catalog/', views.labs_catalog, name='labs_catalog'),
	path('display_lab/<int:lab_id>', views.display_lab, name='display_lab'),
	path('task_status/<int:user_id>&<str:task_id>', views.task_status, name='task_status'),
	path('post/<int:post_id>', views.display_single, name='display_single'),
	path('tags/<int:tag_id>', views.tags_list, name='tags_list'),
	path('ajax/vote/', views.vote, name="vote"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



