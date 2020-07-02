from django.urls import path,re_path,include
from blog import views



urlpatterns = [
    path('',views.index,name='index'),
    path('blog/',views.blog,name='blog'),
    re_path(r'^post/(?P<pk>\d+)/$',views.post,name='post'),
    path('search/',views.search,name='search'),
    re_path(r'^post/(?P<pk>\d+)/update/$',views.post_update,name='post_update'),
    re_path(r'^post/(?P<pk>\d+)/delete/$',views.post_delete,name='post_delete'),
    path('create/',views.post_create,name='post_create'),
    path('contact.html',views.contact,name='contact')

]
