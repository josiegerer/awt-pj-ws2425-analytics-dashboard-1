"""
URL configuration for analyticDashboardDjangoApp project

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

## Adding Function so the administator of LMS can configure the LRS tool
## Two options are available: Using our own LRS or using an external LRS

## Creating endpoints for own LRS get and post requests 



from django.contrib import admin
from django.urls import include, path
from xapi.views import  get_all_objects_of_attribute, get_all_statement_for_learner,  get_all_statements, get_all_statements_for_instructor, get_statements_of_last_days_by_timestamp
from lti import views
from authentification.views import refresh_token_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lti/launch/', views.launch),
    path('lti/login/', views.login, name='lti-login'),
    path('lti/', include('lti_provider.urls')),
    path('token/refresh/', refresh_token_view, name='token_refresh'),
    path('lrs', get_all_statements, name='get_all_statements'),
    path('lrs/lastdays/<int:lastdays>/', get_statements_of_last_days_by_timestamp, name='get_statements_of_last_30days'),
    path('lrs/attributes/<str:attribute>/', get_all_objects_of_attribute, name='get_all_attributes'),
    path('lrs/learner/', get_all_statement_for_learner, name='get_all_statements_for_learner'),
    path('lrs/instructor/', get_all_statements_for_instructor)
]
