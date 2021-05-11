from django.shortcuts import render
from django.views.generic import *
from .models import *
from django.conf import settings
from blog.forms import PostSearchForm
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from myblog.views import OwnerOnlyMixin

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    #disqus 댓글기능
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disqus_short'] = f"{settings.DISQUS_SHORTNAME}"
        context['disqus_id'] = f"post-{self.object.id}-{self.object.slug}"
        context['disqus_url'] = f"{settings.DISQUS_MY_DOMAIN}{self.object.get_absolute_url}"
        context['disqus_title'] = f'{self.object.slug}'
        return context



# Post를 쓴 적이 없으면 안됨
class PostArchiveView(ArchiveIndexView):
    model = Post
    date_field = 'modify_date'
    template_name = 'blog/archive/post_archive.html'

class PostYearArchiveView(YearArchiveView):
    model = Post
    date_field = 'modify_date'
    template_name = 'blog/archive/post_archive_year.html'
    make_object_list = True

class PostMonthArchiveView(MonthArchiveView):
    model = Post
    date_field = 'modify_date'
    template_name = 'blog/archive/post_archive_month.html'

class PostDayArchiveView(DayArchiveView):
    model = Post
    date_field = 'modify_date'
    template_name = 'blog/archive/post_archive_day.html'

class PostTodayArchiveView(TodayArchiveView):
    model = Post
    date_field = 'modify_date'
    template_name = 'blog/archive/post_archive_day.html'



#taggit
class TagCloudTemplateView(TemplateView):
    template_name = 'taggit/taggit_cloud.html'

class TaggedObjectListView(ListView):
    model = Post
    template_name = 'taggit/taggit_post_list.html'

    def get_queryset(self):
        return Post.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context



class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name = 'blog/post_search.html'

    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word']
        post_list = Post.objects.filter(Q(title__icontains=searchWord) | Q(description__icontains=searchWord) | Q(content__icontains=searchWord)).distinct()

        context = dict()
        context['form'] = form
        context['search_term'] = searchWord
        context['object_list'] = post_list

        return render(self.request, self.template_name, context)



#CRUD
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'description', 'content', 'image', 'tags']
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse('blog:detail',kwargs={'pk': self.object.id })

class PostChangeListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/post_change_list.html'    

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user).order_by('id')

class PostUpdateView(OwnerOnlyMixin, UpdateView):
    model = Post
    fields = ['title', 'description', 'content', 'image', 'tags']
    success_url = reverse_lazy('blog:index')

    def get_success_url(self):
        return reverse('blog:detail',kwargs={'pk': self.object.id })

class PostDeleteView(OwnerOnlyMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')