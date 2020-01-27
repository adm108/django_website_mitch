from django.urls import path
from blog.views import create_blog_view, detail_blog_view, edit_blog_view


app_name = 'blog'

urlpatterns = [
    path('create/', create_blog_view, name='create'),
    # slug for post id - every post has the slug - it is unique url for every
    # post
    path('<slug>/', detail_blog_view, name='detail'),
    path('<slug>/edit', edit_blog_view, name='edit'),
]
