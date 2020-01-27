from django import forms
from blog.models import BlogPost


class CreateBlogPostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image']


class UpdateBlogPostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image']

    # this will only going to by call if commit = True
    def save(self, commit=True):
        # cleaned_data takes new argument from form I think
        blog_post = self.instance
        blog_post.title = self.cleaned_data['title']
        blog_post.body = self.cleaned_data['body']

        # if blog post has new image, save that image
        if self.cleaned_data['image']:
            blog_post.image = self.cleaned_data['image']
        # else: do nothing

        if commit:
            blog_post.save()
        return blog_post
