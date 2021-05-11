from django.urls import path, re_path
from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('post/', PostListView.as_view(), name='post_list'),
    #path('post/<slug:slug>/', PostDetailView.as_view(), name='detail'), 이러면 한글을 처리 못함
    re_path(r'^post/(?P<slug>[-\w]+)/$', PostDetailView.as_view(), name='post_detail'),
]
urlpatterns += [
    path('archive/', PostArchiveView.as_view(),name='post_archive'),
    path('archive/<int:year>/', PostYearArchiveView.as_view(),name='post_year_archive'),
    path('archive/<int:year>/<str:month>/', PostMonthArchiveView.as_view(), name='post_month_archive'),
    path('archive/<int:year>/<str:month>/<int:day>/', PostDayArchiveView.as_view(),name='post_day_archive'),
    path('archive/today/', PostTodayArchiveView.as_view(), name='post_today_archive'),
]
urlpatterns += [
    path('tag/', TagCloudTemplateView.as_view(), name='tag_cloud'),
    path('tag/<str:tag>/', TaggedObjectListView.as_view(), name='tagged_object_list'),
]

urlpatterns += [
    path('search/', SearchFormView.as_view(), name='search'),
]
# CRUD
urlpatterns += [
    path('add/', PostCreateView.as_view(), name='add'),
    path('change/', PostChangeListView.as_view(), name='change'),
    path('update/<int:pk>/', PostUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='delete')
]