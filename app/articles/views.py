from articles.forms import PostForm, AnswerForm
from articles.models import Post, Answer, Tag, LikeDislike
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404


def index(request: WSGIRequest):
    query_filter = None

    filters = request.GET.keys()
    if len(filters) == 1:
        query_filter = list(filters)[0]
    filter_map = {
        "popular": "-total_answers",
        "pinned": "-is_pinned",
    }

    sort_key = filter_map.get(query_filter, '-create_date')
    if sort_key == '-is_pinned':
        questions_list = Post.objects.all().filter(is_pinned=True).order_by('-create_date')
    else:
        questions_list = Post.objects.all().order_by(sort_key)
    question_context = paginate(questions_list, request, 3)
    question_context.update({'sort_key': sort_key})
    return render(request, 'articles/index.html', context=question_context)


def new_post(request):
    if request.method == 'GET':
        form = PostForm()
        if request.user.is_authenticated:
            return render(request, 'articles/utils/new_post.html', {'form': form})
        return redirect('accounts:login')
    else:
        form = PostForm(request.POST)
        if not form.is_valid():
            return redirect(request.META['HTTP_REFERER'])
        tags = form.cleaned_data['tags'].split()
        post_full = Post.objects.create_post(author=request.user, title=form.cleaned_data['title'],
                                                         text=form.cleaned_data['text'], is_pinned=form.cleaned_data['pinned'], tags=tags)
        if post_full:
            post_full.save()
            return redirect('../post/{}'.format(post_full.id))
        else:
            return render(request, 'articles/utils/new_post.html', {'error': 'Something went wrong. Please try again'})


def display_single(request, post_id):
    context = {}
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        form = AnswerForm(request.POST)
        if not form.is_valid():
            context.update({'form': form})
        answer_full = Answer.objects.create_answer(author=request.user, post=post,
                                                   text=form.cleaned_data['text'])
        answer_full.save()
        return redirect('../post/{}'.format(post.id))
    answers = Answer.objects.filter(post=post_id).order_by('-create_date')
    answers_context = paginate(answers, request, 3)
    form = AnswerForm()
    context.update({'form': form, 'post': post,
                    'page_object': answers_context['page_object'],
                    'is_paginated': answers_context['is_paginated'],
                    'next_url': answers_context['next_url'],
                    'prev_url': answers_context['prev_url']})
    return render(request, 'articles/utils/post.html', context=context)


def tags_list(request, tag_id):
    context = {}
    tag = get_object_or_404(Tag, id=tag_id)
    questions = Tag.objects.filter(id=tag_id)
    context.update({'questions': questions, 'tag': tag})
    return render(request, 'articles/utils/tags.html', context=context)


def paginate(objects_list, request, per_page):
    data_on_page = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    page = data_on_page.get_page(page_number)
    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''
    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
    }
    return context


@login_required
def vote(request):
    post = request.POST
    user = request.user

    action = post['action']
    data_id = post['data_id']
    data_type = post['data_type']
    if data_type == 'post':
        data_object = Post.objects.get(pk=data_id)
    else:
        data_object = Answer.objects.get(pk=data_id)
    LikeDislike.objects.create_like_dislike(user, instance=data_object, object_id=data_id, action=action)

    return HttpResponse(data_object.total_likes, status=200)
