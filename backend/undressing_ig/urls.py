"""undressing_ig URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from data_donors import views as dataDonorsViews
from ig_observer import views as igObserverViews
from addon_updates.views import addon_updates_view, latest_firefox_view

# v1
routerV1 = routers.DefaultRouter()
routerV1.register(r'donation',
                  dataDonorsViews.DataDonationViewSet,
                  basename='donation')
routerV1.register(r'donor', dataDonorsViews.DataDonorViewSet, basename='donor')
routerV1.register(r'account',
                  igObserverViews.IgUserViewSet,
                  basename='account')
# v2
routerV2 = routers.DefaultRouter()
routerV2.register(r'donation',
                  dataDonorsViews.DataDonationViewSet,
                  basename='donation')
routerV2.register(r'donor', dataDonorsViews.DataDonorViewSet, basename='donor')
routerV2.register(r'account',
                  igObserverViews.IgUserViewSet2,
                  basename='account')
routerV2.register(r'project',
                  igObserverViews.ProjectViewSet,
                  basename='project')
routerV2.register(r'user-followed-by',
                  igObserverViews.IgUserFollowedByViewSet,
                  basename='user-followed-by')
urlpatterns = [
    path('api/v1/', include(routerV1.urls)),
    path('api/v2/', include(routerV2.urls)),
    path('monitoradmin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('addon-updates.json', addon_updates_view),
    path('latest-firefox/', latest_firefox_view),
]
