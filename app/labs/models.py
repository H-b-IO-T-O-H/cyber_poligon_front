from django.db import models
from django.utils import timezone

from articles.models import Post
from accounts.models import User


class LabManager(models.Manager):
    def create_lab(self, author, title, description, executable, linked_post_id):
        return self.create(author=author,
                           title=title,
                           description=description,
                           linked_post=Post.objects.get(pk=linked_post_id) if linked_post_id is not None else None,
                           executable=executable)


class Lab(models.Model):
    objects = LabManager()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=512)
    executable = models.CharField(max_length=1024)
    linked_post = models.ForeignKey(Post, on_delete=models.SET_NULL, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def publish(self):
        self.create_date = timezone.now()
        self.save()
