from django.urls import path
from labs import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'labs'
urlpatterns = [
    path('new_lab/', views.new_lab, name='new_lab'),
    path('labs_catalog/', views.labs_catalog, name='labs_catalog'),
    path('display_lab/<int:lab_id>', views.display_lab, name='display_lab'),
    path('task_status/<int:user_id>&<str:task_id>', views.task_status, name='task_status')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



