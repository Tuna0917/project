from django.shortcuts import render, redirect
from django.views.generic import *
from photo.models import *
from photo.form import PhotoInlineFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from myblog.views import OwnerOnlyMixin
# Create your views here.


class AlbumListView(ListView):
    model = Album

class AlbumDetailView(DetailView):
    model = Album

class PhotoDetailView(DetailView):
    model = Photo



class PhotoCreateView(CreateView):
    model = Photo
    fields = ('album', 'title', 'image', 'description')
    success_url = reverse_lazy('photo:index')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class PhotoChangeListView(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo/photo_change_list.html'

    def get_queryset(self):
        return Photo.objects.filter(owner=self.request.user).order_by('id')

class PhotoUpdateView(OwnerOnlyMixin, UpdateView):
    model = Photo
    fields = ('album', 'title', 'image', 'description')
    success_url = reverse_lazy('photo:index')

class PhotoDeleteView(OwnerOnlyMixin, DeleteView):
    model = Photo
    success_url = reverse_lazy('photo:index')

class AlbumChangeListView(LoginRequiredMixin, ListView):
    model = Album
    template_name= 'photo/album_change_list.html'

    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user).order_by('id')

class AlbumDeleteView(OwnerOnlyMixin, DeleteView):
    model = Album
    success_url = reverse_lazy('photo:index')

class AlbumPhotoCreateView(LoginRequiredMixin, CreateView):
    model = Album
    fields = ('name', 'description')
    success_url = reverse_lazy('photo:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset']= PhotoInlineFormSet(self.request.POST, self.request.FILES)
        else:
            context['formset'] = PhotoInlineFormSet()
        return context
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        context = self.get_context_data()
        formset = context['formset']
        for photoform in formset:
            photoform.instance.owner = self.request.user
        if formset.is_vaild():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class AlbumPhotoUpdateView(OwnerOnlyMixin, UpdateView):
    model = Album
    fields = ('name', 'description')
    success_url = reverse_lazy('photo:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset']= PhotoInlineFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = PhotoInlineFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_vaild():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))