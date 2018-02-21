from django.conf.urls import url, include
from . import views
from . import rest_api
from django.shortcuts import HttpResponse
# from wadibyte.shorturls.views import redirect_view
# from wadibyte.accounts.views import registration_view
# from wadibyte.accounts import urls as accounts_urls

from rest_framework import routers
from . import rest_api

router = routers.DefaultRouter()
router.register(r'care',rest_api.CareViewSet)
router.register(r'news',rest_api.NewsViewSet)
router.register(r'management',rest_api.ManagementViewSet)

urlpatterns=[
url(r'^org_all_api/$',views.get_all_org_api,name='get-all-api'),
url(r'^org_create/$',views.org_create,name='org_create'),

url(r'^api_sehha/care/create/$',views.api_care_create,name='api-care-create'),
url(r'^api_sehha/care/$',views.api_care,name='api-care'),

url(r'^api_sehha/news/create/$',views.api_news_create,name='api-news-create'),
url(r'^api_sehha/news/$',views.api_news,name='api-news'),

url(r'^ajax/',views.ajax,name='ajax'),
url(r'^uploads/image/$',views.dashboard_upload_image,name='dashboard-upload-image'),
url(r'^uploads/image_bootstrip/$',views.dashboard_upload_image_bootstrip,name='dashboard-upload-image'),
# url(r'^url/(?P<url_value>[\w-]+)/',redirect_view,name='short_urls'),


url(r'^dashboard/(?P<mod>[\w-]+)/(?P<id>[0-9]+)/$',views.dashboard,name='org-mod-id-dashboard'),
url(r'^dashboard/(?P<mod>[\w-]+)/$',views.dashboard,name='org-mod-dashboard'),
url(r'^dashboard/$',views.dashboard,name='org-dashboard'),



url(r'^management/create/$',views.NewsCreateView.as_view(init_tags='management'),name='management-create'),
url(r'^educational/create/$',views.NewsCreateView.as_view(init_tags='educational'),name='educational-create'),
url(r'^educational/$',views.NewsListView.as_view(tag_name='educational'),name='educational-list'),
url(r'^news/create/$',views.NewsCreateView.as_view(init_tags='news'),name='news-create'),
url(r'^news/(?P<pk>[0-9]+)/change/$',views.NewsUpdateView.as_view(),name='news-update'),
url(r'^news/(?P<pk>[0-9]+)/delete/$',views.NewsDeleteView.as_view(),name='news-delete'),
# url(r'^news/(?P<pk>[0-9]+)/(?P<slug>[\w-]+)/$',views.NewsDetailView.as_view(),name='news-detail'),
url(r'^news/(?P<pk>[\w-]+)/$',views.NewsDetailView.as_view(),name='news-detail'),
url(r'^news/$',views.NewsListView.as_view(),name='news-list'),


url(r'^care/create/$',views.OrgCreateView.as_view(),name='org-create'),
url(r'^care/(?P<uuid>[0-9]+)\.html/change/$',views.OrgUpdateView.as_view(),name='org-update'),
url(r'^care/(?P<uuid>[0-9]+)\.html/delete/$',views.OrgDeleteView.as_view(),name='org-delete'),
url(r'^care/(?P<uuid>[\w-]+)/(?P<slug>[\w-]+)\.html$',views.OrgDetailView.as_view(),name='org-detail'),
url(r'^cares\.html$',views.OrgListView.as_view(),name='org-list'),

#url(r'^api/(?P<pk>[0-9])$',rest_api.get_select_org,name='rest-select-org'),
#url(r'^api/$',rest_api.get_all_org,name='rest-all-org'),



url(r'^api/', include(router.urls)),
url(r'^$',views.HomeView.as_view(),name='org_home'),
# url('',include(accounts_urls)),
]
