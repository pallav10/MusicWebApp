from django.conf.urls import url
import views


urlpatterns = [
    url(r'^users/login/$', views.user_login),
    url(r'^users/$', views.user_registration),
    url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
    url(r'^users/(?P<pk>[0-9]+)/genre/$', views.genre),
    url(r'^users/(?P<pk>[0-9]+)/song/$', views.song),
]



