"""exclusionoracle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from rules import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('rules/', views.RulesView.as_view()),
    path('rules/tree/<path:surt_string>', views.tree),
    path('rule/<int:pk>/', views.RuleView.as_view()),
    path('decide/', views.decide),
]
