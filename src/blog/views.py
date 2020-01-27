# for blog post
from blog.models import BlogPost
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# for queryset
from django.db.models import Q


def create_blog_view(request):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    # we can post something or None, FILES to upload images, it is required
    form = CreateBlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        # it is going to create form after all the fields have been validated
        obj = form.save(commit=False)
        # we have to collect author of the post
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = CreateBlogPostForm()

    # after creating post we render again create post view
    context['form'] = form

    return render(request, 'blog/create_blog.html', context)


def detail_blog_view(request, slug):

    context = {}

    blog_post = get_object_or_404(BlogPost, slug=slug)
    context['blog_post'] = blog_post

    return render(request, 'blog/detail_blog.html', context)


def edit_blog_view(request, slug):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticated')

    blog_post = get_object_or_404(BlogPost, slug=slug)

    # it will not allow to edit someone's post
    if blog_post.author != user:
        return HttpResponse('You are not the author of that post.')

    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None,
                                  instance=blog_post)
        if form.is_valid():
            # that will load the parameters given access to cleaned_data in
            # form
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = 'Updated'
            blog_post = obj

    # setting new values to post and show it in edit_blog.html
    form = UpdateBlogPostForm(
        initial={
            'title': blog_post.title,
            'body': blog_post.body,
            'image': blog_post.image
        }
    )

    context['form'] = form

    return render(request, 'blog/edit_blog.html', context)


def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ") # python install 2019 = [python, install, 2019]
    for q in queries:
        posts = BlogPost.objects.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        ).distinct()

        for post in posts:
            queryset.append(post)

    return list(set(queryset))
