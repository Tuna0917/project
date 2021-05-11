from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from bookmark.models import Bookmark

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from myblog.views import OwnerOnlyMixin

# Create your views here.
class BookmarkLV(ListView):
    model = Bookmark
    
class BookmarkDV(DetailView):
    model = Bookmark

class BookmarkCreateView(LoginRequiredMixin, CreateView):
    model = Bookmark
    fields = ['title', 'url']
    success_url = reverse_lazy('bookmark:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('bookmark:detail',kwargs={'pk': self.object.id })
    
class BookmarkUpdateView(OwnerOnlyMixin, UpdateView):
    model = Bookmark
    fields = ['title', 'url']
    success_url = reverse_lazy('bookmark:index')
    
    def get_success_url(self):
        return reverse('bookmark:detail',kwargs={'pk': self.object.id })

class BookmarkDeleteView(OwnerOnlyMixin, DeleteView):
    model = Bookmark
    success_url = reverse_lazy('bookmark:index')