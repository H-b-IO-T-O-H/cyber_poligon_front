from accounts.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


class TagManager(models.Manager):
    def add_tags(self, tag):
        if Tag.objects.filter(tag_name=tag).exists():
            tag = self.get(tag_name=tag)
            tag.total += 1
            tag.save(update_fields=['total'])
        else:
            tag = self.create(tag_name=tag)
            tag.save()
        return tag


class Tag(models.Model):
    objects = TagManager()
    tag_name = models.TextField()
    total = models.IntegerField(default=1)

    def __str__(self):
        return self.tag_name


class LikeDislikeManager(models.Manager):
    def create_like_dislike(self, user, instance, object_id, action):
        try:
            like = self.filter(user=user).get(object_id=object_id)
            if like.beenPut and action == 'down':
                like.beenPut = False
                if instance.total_likes >= 1:
                    instance.total_likes -= 1
            elif not like.beenPut and action == 'up':
                like.beenPut = True
                instance.total_likes += 1
            like.save(update_fields=['beenPut'])
        except:
            like = self.create(user=user, obj=instance, object_id=instance.id)
            if action == 'up':
                like.beenPut = True
                instance.total_likes += 1
            like.save()

        instance.save(update_fields=['total_likes'])
        return like


class LikeDislike(models.Model):
    objects = LikeDislikeManager()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    beenPut = models.BooleanField(default=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    obj = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.user


class PostManager(models.Manager):
    def create_post(self, **kwargs):
        tags = kwargs['tags']
        post = self.create(author=kwargs.get('author'), title=kwargs.get('title'), text=kwargs.get('text'),
                               is_pinned=kwargs.get('is_pinned'))
        post.save()
        for tag in tags:
            current_tag = Tag.objects.add_tags(tag)
            post.tags.add(current_tag)
        return post


class Post(models.Model):
    objects = PostManager()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    total_answers = models.IntegerField(default=0)
    total_likes = models.IntegerField(default=0)
    is_pinned = models.BooleanField(default=True)

    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class AnswerManager(models.Manager):
    def create_answer(self, author, post, text):
        answer = self.create(author=author, post=post, text=text)
        post = Post.objects.get(id=post.id)
        post.total_answers += 1
        post.save(update_fields=['total_answers'])

        return answer


class Answer(models.Model):
    objects = AnswerManager()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    total_likes = models.IntegerField(default=0)
    correct = models.BooleanField(blank=True, default=False)

    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.text

class Lab(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    linked_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    total_likes = models.IntegerField(default=0)
    correct = models.BooleanField(blank=True, default=False)

    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.text