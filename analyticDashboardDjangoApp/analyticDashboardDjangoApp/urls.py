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
from dashboard.views import  active_hours_in_the_current_week_for_learner, count_verbs_for_all_activities_for_learner, get_active_users_count_for_timeslot, get_active_users_count_for_timeslot_for_instructor_subcourses, get_active_users_count_for_timeslot_of_subcourses, get_active_users_for_each_hour_today, get_activitiy_completion_and_assigned_for_instructor,get_activity_completion_and_assigned_for_subcourses, get_all_activities_summary, get_all_courses_request, get_all_object_names_and_ids, get_all_user_count, get_all_visits_of_all_activities_of_instructor, get_all_visits_of_all_activities_of_learner, get_attempts_until_passed_for_learner, get_average_score_for_all_subcourses_for_instructor, get_average_timespent_for_all_activities_for_instructor, get_initialization_streak_for_learner, get_last_rating_of_user_for_each_activity, get_list_of_all_activities, get_mean_rating_for_all_activities_for_instructor, get_parent_of_all_parents, get_parents_of_all_activities, get_passed_and_failed_tests_for_instructor, get_passed_and_failed_tests_for_learner, get_scoring_progress_array, get_search_count_for_each_activity, get_time_spent_in_activities_for_learner, is_activity_scored_for_learner, learning_efficiency_for_learner
from lti import views
from authentification.views import refresh_token_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lti/launch/', views.launch),
    path('lti/login/', views.login, name='lti-login'),
    path('lti/', include('lti_provider.urls')),
    path('token/refresh/', refresh_token_view, name='token_refresh'),
    path('activeUser/<int:days>',get_active_users_count_for_timeslot),
    path('totalCourses',get_all_courses_request),
    path('totalActivities',get_list_of_all_activities),
    path('totalUsers',get_all_user_count),
    path('searchCount',get_search_count_for_each_activity),
    path('popularTimes',get_active_users_for_each_hour_today),
    path('assessmentPerformance',get_all_activities_summary),
    path('activityRatings/instructor',get_mean_rating_for_all_activities_for_instructor),
    path('activityRatings/learner', get_last_rating_of_user_for_each_activity),
    path('timeSpentOnActivities/instructor',get_average_timespent_for_all_activities_for_instructor),
    path('timeSpentOnActivities/learner',get_time_spent_in_activities_for_learner),
    path('activityRevisits',get_all_visits_of_all_activities_of_instructor),
    path('assessmentAveragesofCourses',get_average_score_for_all_subcourses_for_instructor),
    path('courseCompletionRate', get_activitiy_completion_and_assigned_for_instructor),
    path('activeUserSubcours/<int:days>/instructor',get_active_users_count_for_timeslot_for_instructor_subcourses),
    path('activeUserSubcours/<int:days>/admin',get_active_users_count_for_timeslot_of_subcourses),
    path('courseCompletionRate/learner', get_activity_completion_and_assigned_for_subcourses),
    path('dailyAverageScoreofTheWeek',get_scoring_progress_array),
    path('assessmentAttempts', is_activity_scored_for_learner),
    path('attemptsUntilPassed', get_attempts_until_passed_for_learner),
    path('activityEngagement', count_verbs_for_all_activities_for_learner),
    path('passRate/instructor', get_passed_and_failed_tests_for_instructor),
    path('passRate/learner', get_passed_and_failed_tests_for_learner),
    path('learningEffectiveness',learning_efficiency_for_learner ),
    path('activeHoursThisWeek',active_hours_in_the_current_week_for_learner),
    path('getNameForActivityId/<str:language>',get_all_object_names_and_ids),
    path('getNameForActivityId',get_all_object_names_and_ids),
    path('parentsOfActivities', get_parents_of_all_activities),
    path('parentsOfParents', get_parent_of_all_parents),
    path('dailyStreak',get_initialization_streak_for_learner),
    path('activityRevists/learner',get_all_visits_of_all_activities_of_learner)
    # 
    #
    #path
]
