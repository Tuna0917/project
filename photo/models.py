from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# from photo.fields import ThumbnailImageField

# Create your models here.
class Album(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('photo:album_detail', arg=(self.id,))

class Photo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True)
    title = models.CharField('TITLE', max_length=30)
    description = models.TextField('Photo description', blank=True)
    # image = ThumbnailImageField(upload_to='photo/%Y/%m')
    image = models.ImageField('IMAGE', upload_to='SorlPhoto/%Y')
    upload_date = models.DateTimeField('Upload date', auto_now_add=True)

    class Meta:
        ordering = ('title',)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('photo:photo_detail', args=(self.id,))
