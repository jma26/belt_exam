from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^quotes$', views.quote),
    url(r'^add_quote/(?P<user_id>\d+)$', views.add_quote),
    url(r'^users/(?P<user_id>\d+)$', views.user_info),
    url(r'^logout$', views.logout),
    url(r'^quotes/add_favorite/(?P<quote_id>\d+)$', views.add_favorite),
    url(r'^quotes/remove_favorite/(?P<quote_id>\d+)$', views.remove_favorite)
]