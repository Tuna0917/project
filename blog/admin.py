from django.contrib import admin
from blog.models import *
# Register your models here.

# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'modify_date', 'tag_list')
    list_filter = ('modify_date',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')
    
    def tag_list(self, obj):
        return ', '.join(o.name for o in obj.tags.all())