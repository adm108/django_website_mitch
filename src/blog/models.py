from django.db import models

# images
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


# file path to upload pictures
def upload_location(instance, filename, **kwargs):
    file_path = f'blog/{str(instance.author.id)}/{str(instance.title)}' \
                f'-{filename}'
    return file_path


class BlogPost(models.Model):
    # can't be blank and null, this field is required
    title = models.CharField(max_length=50, null=False, blank=False)
    body = models.TextField(max_length=5000, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location, null=False,
                              blank=False)
    # auto now add - saves date right after creating model
    date_published = models.DateTimeField(auto_now_add=True,
                                          verbose_name='date published')
    # auto now - saves date right after updating model
    date_updated = models.DateTimeField(auto_now=True, verbose_name='date '
                                                                    'updated')
    # settings.AUTH_USER_MODEL searches our user model in settings.py
    # models.CASCADE - delete all things with this model except author
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    # url of blog post
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title


# if the post is deleted delete also image
@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


# create url for every post before saving it in database
def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)


# every time when you want to add pictures, call this function and create url
pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)
