from django.conf.urls import url

from .views import (
    collection_create,
    collection_detail,
    collection_update,
    collection_delete,
    link_add,
    search_link,
    home,
    about,
    link_delete,
)

urlpatterns = [
    # url(r'^$', collection_list, name='list'),
    url(r'^create$', collection_create, name="create"),
    url(r'^(?P<slug>[\w-]+)/add$', link_add, name='add'),
    url(r'^(?P<slug>[\w-]+)(?:/(?P<tag>[\w-]+))?/$', collection_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/search$', search_link, name="search_link"),
    url(r'^(?P<slug>[\w-]+)/edit$', collection_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete$', collection_delete, name='delete'),
    url(r'^$', home, name='home'),
    url(r'^about$', about, name='about'),
    url(r'^link/(?P<id>\d+)/delete$', link_delete, name='link_delete' ),
    # url(r'^(?P<slug>[\w-]+)/delete$', collection_delete, name='collection_delete'),
]
