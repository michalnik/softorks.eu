"""
URL configuration for www project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, reverse, include
from django.views.generic import TemplateView
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['homepage', 'robots.txt', 'security.txt']

    def location(self, item):
        return reverse(item)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='homepage'),
    path('activities/', include('activities.urls')),
    path('references/', include('references.urls')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt'), name='robots.txt'),
    path('.well-known/security.txt', TemplateView.as_view(template_name='security.txt'), name='security.txt'),
    path('sitemap.xml', sitemap, {'sitemaps': {'static': StaticViewSitemap}}, name='sitemap'),
]
