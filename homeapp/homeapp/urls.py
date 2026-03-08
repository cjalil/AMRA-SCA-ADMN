"""homeapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls.static import static
# for staticfile
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
# fin static file

urlpatterns = [

# for staticfile
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    # fin static file
    path('myspace/', admin.site.urls),
    path('', include('amra.urls')),
    path('', include('Marconi.urls')),
    #path('', include('Andaloussia.urls')),
    #path('', include('Andaloussia2.urls')),
    path('', include('Presentation.urls')),
    path('', include('Mimosas_P.urls')),
    path('', include('Mimosas_M.urls')),
    #path('', include('La_Guirlande.urls')),
    #path('', include('Dream_School.urls')),
    #path('', include('Dream_School1.urls')),
    #path('', include('Paul_Arene.urls')),
    #path('', include('Initiative_2.urls')),
    path('', include('Benhanza.urls')),
    #path('', include('Benniss.urls')),
    path('', include('ZENITH.urls')),
    #path('', include('ZGHARI.urls')),
    #path('', include('CHKAIL.urls')),
    path('', include('DiwaneAlmaarifa.urls')),
    path('', include('DiwaneAlmaarifa2.urls')),
    #path('', include('JEANCOCTEAU.urls')), 
    path('', include('ALMADINA.urls')),
    path('', include('ALMADINA2.urls')),
    path('', include('PALOALTO.urls')),
    #path('', include('ZAIR_AL_AMIN.urls')),
    path('', include('LEADERSCHOOL.urls')),
    path('', include('CHAARANE.urls')),
    path('', include('MONECOLE.urls')),
    path('', include('SAMAE.urls')),
    #path('', include('MADINACALIFORNIE.urls')),
    #path('', include('NOUVELLEGENERATION.urls')),
    path('', include('ZGHARIKNT.urls')),
    #path('', include('AlAnware.urls')),
    path('api/', include('school_api.urls')),
    path('', include('school_api.urls')),
    
    
   
    
    
    
    
    
    



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
