from django.urls import path
from photo.views import *

app_name = 'photo'
urlpatterns = [
    path('', AlbumListView.as_view(), name='index'),
    path('album', AlbumListView.as_view(), name='album_list'),
    path('album/<int:pk>', AlbumDetailView.as_view(), name='album_detail'),
    path('photo/<int:pk>', PhotoDetailView.as_view(), name='photo_detail'),
]

urlpatterns += [
    path('photo/add/', PhotoCreateView.as_view(), name='photo_add'),
    path('photo/change/', PhotoChangeListView.as_view(), name='photo_change'),
    path('photo/<int:pk>/update/', PhotoUpdateView.as_view(),name='photo_update'),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete'),
]

urlpatterns += [
    path('album/add/', AlbumPhotoCreateView.as_view(), name='album_add'),
    path('album/change/', AlbumChangeListView.as_view(), name='album_change'),
    path('album/<int:pk>/update/', AlbumPhotoUpdateView.as_view(),name='album_update'),
    path('album/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album_delete'),
]