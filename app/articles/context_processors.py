def popular_data(request):
    from articles.models import User
    from articles.models import Tag
    return {'users': User.objects.all().order_by('-date_joined')[:8], 'tags': Tag.objects.all().order_by('-total')[:10]}