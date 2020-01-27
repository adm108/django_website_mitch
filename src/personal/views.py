# Question and Accounts models were earlier
from django.shortcuts import render
# from personal.models import Question
# from account.models import Account

# for view blog posts, Blog Post was previous, now is get_blog_queryset
from blog.models import BlogPost
from operator import attrgetter

# for queries
from blog.views import get_blog_queryset

# for pagination
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def home_screen_view(request):
    context = {'some_string': "this is some string",
    'some_number': 21312312312}
    list_of_values = []
    list_of_values.append('first entry')
    list_of_values.append('second entry')
    list_of_values.append('third entry')
    list_of_values.append('fourth entry')
    context['list_of_values'] = list_of_values

    questions = Question.objects.all()
    context = {'questions': questions}

    context = {}

    query = ""
    if request.GET:
        # searching q parameter - name='q' in html INPUT tag
        query = request.GET['g']
        context['query'] = query

    blog_posts = sorted(get_blog_queryset(query), key=attrgetter(
        'date_updated'), reverse=True)

    context['blog_posts'] = blog_posts

    return render(request, 'personal/home.html', context)


BLOG_POSTS_PER_PAGE = 1


def home_screen_view(request, *args, **kwargs):
    context = {}

    # Search
    query = ""
    if request.GET:
        # get the value of q if it is nothing (empty parameters problem):
        query = request.GET.get('q', '')
        context['query'] = str(query)

    blog_posts = sorted(get_blog_queryset(query),
                        key=attrgetter('date_updated'), reverse=True)

    # Pagination
    page = request.GET.get('page', 1)
    blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
    try:
        blog_posts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
    except EmptyPage:
        blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

    context['blog_posts'] = blog_posts

    return render(request, "personal/home.html", context)
