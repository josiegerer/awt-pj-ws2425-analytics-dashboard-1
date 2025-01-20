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
from dashboard.views import get_active_users_count_for_timeslot, get_all_activities_count, get_all_courses_count, get_all_user_count, get_all_user_for_hour, get_average_score_for_activities
from lti import views
from authentification.views import refresh_token_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lti/launch/', views.launch),
    path('lti/login/', views.login, name='lti-login'),
    path('lti/', include('lti_provider.urls')),
    path('token/refresh/', refresh_token_view, name='token_refresh'),
    #path('/popularityOfResources/<str:keyword>'),
    path('activeUser/<int:days>',get_active_users_count_for_timeslot),
    path('totalCourses',get_all_courses_count),
    path('totalActivities',get_all_activities_count),
    path('totalUsers',get_all_user_count),
    path('popularTimes/<int:hour>',get_all_user_for_hour),
    path('assessmentPerformance',get_average_score_for_activities)
    #path('/totalCourses'),
    #path
]
