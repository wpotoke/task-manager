"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from tasks.views import TaskAPIView
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [
    path("tasklist/", TaskAPIView.as_view()),
    path("task/create/", TaskAPIView.as_view()),
    path("task/update/<str:uuid>/", TaskAPIView.as_view()),
    path("task/delete/<str:uuid>/", TaskAPIView.as_view()),
    path("task/<str:uuid>/", TaskAPIView.as_view()),
    path("schema/", SpectacularAPIView.as_view()),
]
