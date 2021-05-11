from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils.text import slugify

class Post(models.Model):
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(verbose_name='TITLE', max_length=100)
    slug = models.SlugField('SLUG', unique=True, allow_unicode=True, help_text='one word for title alias.')
    description = models.CharField('DESCRIPTION', max_length=100, blank=True, help_text='simple description text.')
    content = models.TextField('CONTENT')
    image = models.ImageField('IMAGE', upload_to='SorlPhoto/%Y', null=True)
    created_date = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_date = models.DateTimeField('MODIFY DATE', auto_now=True)
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        db_table = 'blog.posts'
        ordering = ('-modify_date',)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=(self.slug,))
    
    def get_previous(self):
        return self.get_previous_by_modify_date()
    
    def get_next(self):
        return self.get_next_by_modify_date()
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args,**kwargs)