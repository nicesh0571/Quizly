"""
URL configuration for quizly_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from quizly import views  # 👈 앱 이름에 맞게 import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.upload_files, name='upload'),
    # path('summarize/pdf/', views.summarize_pdf_view, name='summarize_pdf'),
    # path('summarize/audio/', views.summarize_audio_view, name='summarize_audio'),  # ✅ 오디오 요약용
    

]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
