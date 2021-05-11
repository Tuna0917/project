from django.contrib import admin
from .models import Bookmark

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id','title','url')

'''
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id','title','url')
admin.site.register(Bookmark, BookmarkAdmin)
'''