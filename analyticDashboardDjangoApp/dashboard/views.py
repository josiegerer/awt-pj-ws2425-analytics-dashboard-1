
#Number of searches conducted on specific keyword
from django.http import JsonResponse
from authentification.views import verify_admin_token_annotation, verify_instructor_token_annotation, verify_learner_token_annotation
from dashboard.xapi_services import UserXAPIService, XAPIService
from xapi.lrs_utils import  fetch_xapi_statements_from_db_for_user, fetch_xapi_statements_from_db, fetch_xapi_statements_from_db
from xapi.xapi_utils import construct_activity_id, construct_verb_id, filter_statements_by_instructor_email, filter_statements_by_object_id, filter_statements_by_course_id, get_all_actors_emails_used, get_all_courses, get_all_objects_ids_used, get_all_objects_names_used, get_all_user_names, get_all_verbs_ids_used, get_all_verbs_name_used, get_duration_of_activities, get_durations_of_tests_for_user, get_id, get_name_of_verb_by_id, get_object_name, get_object_name_by_id, get_open_activities, get_score, get_statements_in_last_days, filter_statements_by_verb_id, get_statements_of_specfic_user_by_email, get_statements_with_specific_hour, sort_statements_by_timestamp
from datetime import datetime, timedelta

xapi_service = XAPIService(cache_duration=300) 
user_xapi_service=UserXAPIService(cache_duration=300) 


@verify_admin_token_annotation
def get_search_count_for_each_activity(request):
            try:
                statements = xapi_service.fetch_statements()
                verb_id = construct_verb_id("searched")
                statements_filtered_by_verb = filter_statements_by_verb_id(statements, verb_id)
                search_count_by_activity = {}

                for statement in statements_filtered_by_verb:
                    activity_id = statement['statement_payload']['object']['id']
                    if activity_id not in search_count_by_activity:
                        search_count_by_activity[activity_id] = 0
                    search_count_by_activity[activity_id] += 1

                responseJson = {"searchCount": search_count_by_activity}
                return JsonResponse(responseJson, safe=False)
            except Exception as e:
                return JsonResponse({
                    "error": str(e)
                }, status=500)
@verify_admin_token_annotation       
def get_active_users_count_for_timeslot(request, **kwargs):
    try:
        statements = xapi_service.fetch_statements()
        # Save statements to a JSON file
      
        days = str(kwargs.get('days', 30))
        # Filter statements by time period
        statements_filtered_by_time = get_statements_in_last_days(statements, days)
        # Filter statements by verb initialized
        statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_time, construct_verb_id("initialized"))
   
        unique_users = get_all_actors_emails_used(statements_filtered_by_verb)
        
        print("Unique users:", unique_users)

        responseJson = {"activeUser": len(unique_users)}
        
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
        
@verify_admin_token_annotation
def get_active_users_count_for_timeslot_of_subcourses(request, **kwargs):
    try:
        statements = xapi_service.fetch_statements()
        days = str(kwargs.get('days', 30))
        statements_filtered_by_time = get_statements_in_last_days(statements, days)
        all_subcourses = get_all_courses(statements_filtered_by_time)
        active_users_by_subcourse = {}

        for subcourse_id in all_subcourses:
            statements_filtered_by_subcourse_id = filter_statements_by_course_id(statements_filtered_by_time, subcourse_id)
            unique_users = get_all_actors_emails_used(statements_filtered_by_subcourse_id)
            active_users_by_subcourse[subcourse_id] = len(unique_users)

        responseJson = {"activeUsersBySubcourse": active_users_by_subcourse}
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)

@verify_instructor_token_annotation
def get_active_users_count_for_timeslot_for_instructor_subcourses(request, **kwargs):
    try:
        statements = user_xapi_service.fetch_statements_for_user(request.email)
        days = str(kwargs.get('days', 30))
        statements_filtered_by_time = get_statements_in_last_days(statements, days)
        all_subcourses = get_all_courses(statements_filtered_by_time)
        active_users_by_subcourse = {}

        for subcourse_id in all_subcourses:
            statements_filtered_by_subcourse_id = filter_statements_by_course_id(statements_filtered_by_time, subcourse_id)
            unique_users = get_all_actors_emails_used(statements_filtered_by_subcourse_id)
            active_users_by_subcourse[subcourse_id] = len(unique_users)

        responseJson = {"activeUsersBySubcourse": active_users_by_subcourse}
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)

@verify_admin_token_annotation   
def get_all_courses_request(request):
    try:
        statements = xapi_service.fetch_statements()
        all_courses= get_all_courses(statements)

        responseJson = {"totalCourses": all_courses}
        
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
@verify_admin_token_annotation        
def get_all_user_count(request):
    try:
        statements = xapi_service.fetch_statements()
        unique_users= get_all_actors_emails_used(statements)
        responseJson = {"totalUsers": len(unique_users)}
        
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
@verify_admin_token_annotation
def get_list_of_all_activities(request):
    try:
        statements = xapi_service.fetch_statements()
        all_objects = get_all_objects_ids_used(statements)

        responseJson = {"activities": all_objects}
        
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
        
def get_all_activities_count(request):
    try:
        statements = xapi_service.fetch_statements()
        unique_objects = get_all_objects_ids_used(statements)

        responseJson = {"totalObjects": len(unique_objects)}
        
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
        
def get_all_user_for_hour(request, **kwargs):
    try:
        statements = xapi_service.fetch_statements()
        hour = int(kwargs.get('hour', 0))
        
        # Filter statements by specific hour
        statements_filtered_by_hour = get_statements_with_specific_hour(statements, hour)
        unique_users = get_all_actors_emails_used(statements_filtered_by_hour)

        responseJson = {"totalUsers": len(unique_users)}
        
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
        
def get_active_users_for_each_hour_today(request):
    try:
        statements = xapi_service.fetch_statements()
        current_date = datetime.now().date()
        
        active_users_by_hour = {hour: set() for hour in range(24)}
        
        for statement in statements:
            timestamp = statement['timestamp']
            if timestamp.date() == current_date:
                hour = timestamp.hour
                actor_email = statement['statement_payload']['actor']['mbox']
                active_users_by_hour[hour].add(actor_email)
        
        responseJson = {
            "activeUsersByHour": {hour: len(users) for hour, users in active_users_by_hour.items()}
        }
        
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
    
def get_average_score_for_activities(request, **kwargs):
    statements = xapi_service.fetch_statements()
    activity_id = request.GET.get('activityId')
    print(activity_id)
    statements_filtered_by_object_id = filter_statements_by_object_id(statements, activity_id)
    
    staments_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_object_id, construct_verb_id("scored"))
    
    total_score = 0
    count = 0
    
    for statement in staments_filtered_by_verb:
        if 'statement_payload' in statement and 'result' in statement['statement_payload'] and 'score' in statement['statement_payload']['result']:
            total_score += statement['statement_payload']['result']['score']['raw']
            count += 1
    
    average_score = total_score / count if count > 0 else 0
    
    responseJson = {"averageScore": average_score}
@verify_admin_token_annotation    
def get_all_activities_summary(request):
    try:
        statements = xapi_service.fetch_statements()
        all_activities = get_all_objects_ids_used(statements)
        activities_summary = []

        for activity_id in all_activities:
            # Get the total visits
            statements_filtered_by_object_id = filter_statements_by_object_id(statements, activity_id)
            total_visits = len(statements_filtered_by_object_id)

            # Get the average score
            statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_object_id, construct_verb_id("scored"))
            total_score = sum(statement['statement_payload']['result']['score']['raw'] for statement in statements_filtered_by_verb if 'statement_payload' in statement and 'result' in statement['statement_payload'] and 'score' in statement['statement_payload']['result'])
            average_score = total_score / len(statements_filtered_by_verb) if statements_filtered_by_verb else 0

            # Get the average time spent
            all_user_emails = get_all_actors_emails_used(statements_filtered_by_object_id)
            total_time = 0
            user_count = 0
            for email in all_user_emails:
                statements_filtered_by_user = get_statements_of_specfic_user_by_email(statements_filtered_by_object_id, email)
                durations = get_durations_of_tests_for_user(statements_filtered_by_user)
                total_time += sum(duration['duration'].total_seconds() / 60 for duration in durations)
                user_count += 1
            average_time = total_time / user_count if user_count > 0 else 0

            activities_summary.append({
                "activityId": activity_id,
                "totalVisits": total_visits,
                "averageScore": average_score,
                "averageTimeSpent": average_time
            })

        responseJson = {"activitiesSummary": activities_summary}
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
    
def get_average_timespent_for_activities(request):
    statements = xapi_service.fetch_statements()
    activity_id = request.GET.get('activityId')
    
    statements_filtered_by_object_id = filter_statements_by_object_id(statements, activity_id)
    
    all_user_emails = get_all_actors_emails_used(statements_filtered_by_object_id)
    
    total_time = 0
    user_count = 0
    
    for email in all_user_emails:
        statements_filtered_by_user = get_statements_of_specfic_user_by_email(statements_filtered_by_object_id, email)
        durations = get_durations_of_tests_for_user(statements_filtered_by_user)
        total_time += sum(durations)
        user_count += 1
    
    average_time = total_time / user_count if user_count > 0 else 0
    
    responseJson = {"averageTime": average_time}
    
    return JsonResponse(responseJson, safe=False)

def get_average_timespent_for_tests(request):
    statements = xapi_service.fetch_statements()
    activity_id = request.GET.get('activityId')
    
    statements_filtered_by_object_id = filter_statements_by_object_id(statements, activity_id)
    
    all_user_emails = get_all_actors_emails_used(statements_filtered_by_object_id)
     
    total_time = 0
    user_count = 0
    
    for email in all_user_emails:
        statements_filtered_by_user = get_statements_of_specfic_user_by_email(statements_filtered_by_object_id, email)
        durations = get_durations_of_tests_for_user(statements_filtered_by_user)
        total_time += sum(durations["duration"])
        user_count += 1
    
    average_time = total_time / user_count if user_count > 0 else 0
    
    responseJson = {"averageTime": average_time}
    
    return JsonResponse(responseJson, safe=False)

def get_average_timespent_for_all_activities(request):
    statements = xapi_service.fetch_statements()
    all_activities = get_all_objects_ids_used(statements)
    activities_summary = []

    for activity_id in all_activities:
        statements_filtered_by_object_id = filter_statements_by_object_id(statements, activity_id)
        all_user_emails = get_all_actors_emails_used(statements_filtered_by_object_id)
        
        total_time = 0
        user_count = 0
        
        for email in all_user_emails:
            statements_filtered_by_user = get_statements_of_specfic_user_by_email(statements_filtered_by_object_id, email)
            durations = get_durations_of_tests_for_user(statements_filtered_by_user)
            total_time += sum(durations["duration"])
            user_count += 1
        
        average_time = total_time / user_count if user_count > 0 else 0
        
        activities_summary.append({
            "activityId": activity_id,
            "averageTime": average_time
        })

    responseJson = {"activitiesSummary": activities_summary}
    
    return JsonResponse(responseJson, safe=False)

@verify_instructor_token_annotation
def get_average_timespent_for_all_activities_for_instructor(request):
    statements = user_xapi_service.fetch_statements_for_user(request.email)
    all_activities = get_all_objects_ids_used(statements)
    activities_summary = []
    
    for activity_id in all_activities:
        statements_filtered_by_object_id = filter_statements_by_object_id(statements, activity_id)
        all_user_emails = get_all_actors_emails_used(statements_filtered_by_object_id)
        total_time = 0
        user_count = 0
        
        for email in all_user_emails:
            statements_filtered_by_user = get_statements_of_specfic_user_by_email(statements_filtered_by_object_id, email)
            durations = get_durations_of_tests_for_user(statements_filtered_by_user)
            durations += get_duration_of_activities(statements_filtered_by_user)
            total_time += sum(duration["duration"].total_seconds() / 60 for duration in durations)
            user_count += 1
        
        average_time = total_time / user_count if user_count > 0 else 0
        
        activities_summary.append({
            "activityId": activity_id,
            "averageTime": average_time
        })

    responseJson = {"activitiesSummary": activities_summary}
    
    return JsonResponse(responseJson, safe=False)

@verify_learner_token_annotation
def get_average_timespent_for_all_activities_for_learner(request):
    email = request.email
    statements = user_xapi_service.fetch_statements_for_user(email)
    all_activities = get_all_objects_ids_used(statements)
    activities_summary = []
    
    for activity_id in all_activities:
        statements_filtered_by_object_id = filter_statements_by_object_id(statements, activity_id)
        statements_filtered_by_user = get_statements_of_specfic_user_by_email(statements_filtered_by_object_id, email)
        durations = get_durations_of_tests_for_user(statements_filtered_by_user)
        durations += get_duration_of_activities(statements_filtered_by_user)
        
        total_time = sum(duration["duration"].total_seconds() / 60 for duration in durations)
        user_count = 1 if durations else 0
        
        average_time = total_time / user_count if user_count > 0 else 0
        
        activities_summary.append({
            "activityId": activity_id,
            "averageTime": average_time
        })

    responseJson = {"activitiesSummary": activities_summary}
    
    return JsonResponse(responseJson, safe=False)
@verify_instructor_token_annotation
def get_all_visits_of_all_activities_of_instructor(request):
    instructor_email = request.email
    statements = xapi_service.fetch_statements()
    statements_of_instructor = filter_statements_by_instructor_email(statements, instructor_email)
    all_activities = get_all_objects_ids_used(statements_of_instructor)
    activities_visits = []

    for activity_id in all_activities:
        statements_filtered_by_object_id = filter_statements_by_object_id(statements_of_instructor, activity_id)
        statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_object_id, construct_verb_id("initialized"))
        activities_visits.append({
            "activityId": activity_id,
            "visits": len(statements_filtered_by_verb)
        })

    responseJson = {"activitiesVisits": activities_visits}
    return JsonResponse(responseJson, safe=False)

@verify_learner_token_annotation
def get_all_visits_of_all_activities_of_learner(request):
    email = request.email
    statements = xapi_service.fetch_statements()
    statements_of_learner = get_statements_of_specfic_user_by_email(statements, email)
    all_activities = get_all_objects_ids_used(statements_of_learner)
    activities_visits = []

    for activity_id in all_activities:
        statements_filtered_by_object_id = filter_statements_by_object_id(statements_of_learner, activity_id)
        statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_object_id, construct_verb_id("initialized"))
        activities_visits.append({
            "activityId": activity_id,
            "visits": len(statements_filtered_by_verb)
        })

    responseJson = {"activitiesVisits": activities_visits}
    return JsonResponse(responseJson, safe=False)
def get_all_activities(request):
    try:
        statements = xapi_service.fetch_statements()
        all_activities = get_all_objects_ids_used(statements)
        activities = []

        for activity_id in all_activities:
            activity = {
                "activityId": activity_id,
                "totalVisits": len(filter_statements_by_object_id(statements, activity_id)),
                "averageScore": get_average_score_for_activity(statements, activity_id),
                "averageTimeSpent": get_average_time_spent_for_activity(statements, activity_id)
            }
            activities.append(activity)

        responseJson = {"activities": activities}
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)

def get_average_score_for_activity(statements, activity_id):
    statements_filtered_by_object_id = filter_statements_by_object_id(statements, activity_id)
    statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_object_id, construct_verb_id("scored"))
    total_score = sum(statement['result']['score']['raw'] for statement in statements_filtered_by_verb if 'result' in statement and 'score' in statement['result'])
    return total_score / len(statements_filtered_by_verb) if statements_filtered_by_verb else 0

def get_average_time_spent_for_activity(statements, activity_id):
    statements_filtered_by_object_id = filter_statements_by_object_id(statements, activity_id)
    all_user_emails = get_all_actors_emails_used(statements_filtered_by_object_id)
    total_time = 0
    user_count = 0

    for email in all_user_emails:
        statements_filtered_by_user = get_statements_of_specfic_user_by_email(statements_filtered_by_object_id, email)
        durations = get_durations_of_tests_for_user(statements_filtered_by_user)
        total_time += sum(durations)
        user_count += 1

    return total_time / user_count if user_count > 0 else 0

@verify_instructor_token_annotation
def get_average_score_for_all_subcourses_for_instructor(request):
    try:
        statements_of_instructor=user_xapi_service.fetch_statements_for_user(request.email)
        all_subcourses = get_all_courses(statements_of_instructor)
        subcourses_scores = []

        for subcourse_id in all_subcourses:
            statements_filtered_by_subcourse_id = filter_statements_by_course_id(statements_of_instructor, subcourse_id)
            statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_subcourse_id, construct_verb_id("scored"))
            print(statements_filtered_by_verb)
            total_score = 0
            count = 0

            for statement in statements_filtered_by_verb:
                score = get_score(statement)
                if score is not None:
                    total_score += score
                    count += 1

            average_score = total_score / count if count > 0 else 0
            subcourses_scores.append({
                "subcourseId": subcourse_id,
                "averageScore": average_score
            })

        responseJson = {"subcoursesScores": subcourses_scores}
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
        
@verify_instructor_token_annotation
def active_hours_in_the_current_week_for_instructor(request):

    statements_of_instructor=user_xapi_service.fetch_statements_for_user(request.email)
    current_date = datetime.now()
    start_of_week = current_date - timedelta(days=current_date.weekday())
    statements_filtered_by_week = [
        statement for statement in statements_of_instructor
        if start_of_week.date() <= statement['timestamp'].date() <= (start_of_week + timedelta(days=6)).date()
    ]
    active_hours = [{"day": (start_of_week + timedelta(days=i)).strftime('%A'), "hours": [{"hour": h, "timeSpent": 0} for h in range(24)]} for i in range(7)]
    
    durations = get_duration_of_activities(statements_filtered_by_week)
    for duration_info in durations:
        test_start = duration_info['test_start']
        test_end = duration_info['test_end']
        current_time = test_start
        while current_time < test_end:
            next_hour = (current_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
            if next_hour > test_end:
                next_hour = test_end
            duration = (next_hour - current_time).total_seconds() / 60  # Convert duration to minutes
            statement_date = current_time.date()
            day_index = (statement_date - start_of_week.date()).days
            if 0 <= day_index < 7:  # Ensure day_index is within range
                hour = current_time.hour
                active_hours[day_index]["hours"][hour]["timeSpent"] += duration
            current_time = next_hour
    
    responseJson = {"activeHours": active_hours}
    
    return JsonResponse(responseJson, safe=False)

def get_all_subcourses(request):
    try:
        statements = xapi_service.fetch_statements()
        all_subcourses = get_all_courses(statements)

        responseJson = {"totalSubcourses": all_subcourses}
        
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)

@verify_learner_token_annotation
def get_time_spent_in_activities_for_learner(request):
    email = request.email
    statements = user_xapi_service.fetch_statements_for_user(email)
    all_activities = get_all_objects_ids_used(statements)
    activities_duration = []
    total_time = 0

    for activity_id in all_activities:
        statements_filtered_by_object = filter_statements_by_object_id(statements, activity_id)
        durations = get_durations_of_tests_for_user(statements_filtered_by_object)
        durations += get_duration_of_activities(statements_filtered_by_object)
        
        activity_time = sum(duration["duration"].total_seconds() / 60 for duration in durations)
        total_time += activity_time
        
        activities_duration.append({
            "activityId": activity_id,
            "duration": activity_time
        })

    responseJson = {
        "activities": activities_duration,
        "totalTime": total_time
    }
    
    return JsonResponse(responseJson, safe=False)
@verify_instructor_token_annotation
def get_activitiy_completion_and_assigned_for_instructor(request):
    statements = user_xapi_service.fetch_statements_for_user(request.email)
    all_activities = get_all_objects_ids_used(statements)
    all_verbs = get_all_verbs_ids_used(statements)
    print(all_activities)
    print(all_verbs)
    activities_summary = []

    for activity_id in all_activities:
        statements_filtered_by_object = filter_statements_by_object_id(statements, activity_id)
        all_users_of_filtered_statements = get_all_actors_emails_used(statements_filtered_by_object)
      
        statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_object, construct_verb_id("completed"))
        all_users_who_completed = get_all_actors_emails_used(statements_filtered_by_verb)

        activities_summary.append({
            "activityId": activity_id,
            "assigned": len(all_users_of_filtered_statements),
            "completed": len(all_users_who_completed)
        })

    responseJson = {"activitiesSummary": activities_summary}
    return JsonResponse(responseJson, safe=False)

def get_active_users_in_all_courses_in_last_days(request, **kwargs):
    try:
        statements = xapi_service.fetch_statements()
        days = str(kwargs.get('days', 0))
        statements_filtered_by_time = get_statements_in_last_days(statements, days)
        all_courses = get_all_courses(statements_filtered_by_time)
        
        active_users_by_course = {}
        
        for course_id in all_courses:
            statements_filtered_by_course_id = filter_statements_by_course_id(statements_filtered_by_time, course_id)
            unique_users = get_all_actors_emails_used(statements_filtered_by_course_id)
            active_users_by_course[course_id] = len(unique_users)
        
        responseJson = {"activeUsersByCourse": active_users_by_course}
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)

def get_list_of_activities_of_instructor(request):
    statements_of_instructor=user_xapi_service.fetch_statements_for_user(request.email)
    all_objects = get_all_objects_ids_used(statements_of_instructor)
    responseJson = {"activities": all_objects}
    return JsonResponse(responseJson, safe=False)

def get_list_of_activities_of_learner(request):
    email = request.email
    statements = user_xapi_service.fetch_statements_for_user(email)
    statements_of_learner = get_statements_of_specfic_user_by_email(statements, email)
    all_objects = get_all_objects_ids_used(statements_of_learner)
    responseJson = {"activities": all_objects}
    return JsonResponse(responseJson, safe=False)

@verify_learner_token_annotation
def get_activity_completion_and_assigned_for_subcourses(request):
    email = request.email
    statements = user_xapi_service.fetch_statements_for_user(email)
    all_subcourses = get_all_courses(statements)
    subcourses_summary = []

    for subcourse_id in all_subcourses:
        statements_filtered_by_subcourse = filter_statements_by_course_id(statements, subcourse_id)
        all_activities = get_all_objects_ids_used(statements_filtered_by_subcourse)
        assigned_activities = len(all_activities)

        completed_activities = 0
        for activity_id in all_activities:
            statements_filtered_by_activity = filter_statements_by_object_id(statements_filtered_by_subcourse, activity_id)
            statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_activity, construct_verb_id("completed"))
            if len(statements_filtered_by_verb) > 0:
                completed_activities += 1

        subcourses_summary.append({
            "subcourseId": subcourse_id,
            "assignedActivities": assigned_activities,
            "completedActivities": completed_activities
        })

    responseJson = {"subcoursesSummary": subcourses_summary}
    return JsonResponse(responseJson, safe=False)
          
          
@verify_learner_token_annotation        
def get_scoring_progress_array(request):
    email = request.email
    statements = user_xapi_service.fetch_statements_for_user(email)
    statements_filtered_by_verb = filter_statements_by_verb_id(statements, construct_verb_id("scored"))
    scores_by_day = {}
    responseJson = {"score": []}
    
    for statement in statements_filtered_by_verb:
        if get_score(statement) is not None:
            timestamp = statement['timestamp']
            date_str = timestamp.strftime('%Y-%m-%d')
            if date_str not in scores_by_day:
                scores_by_day[date_str] = {'total_score': 0, 'count': 0}
            scores_by_day[date_str]['total_score'] += get_score(statement)
            scores_by_day[date_str]['count'] += 1
    
    for day, data in scores_by_day.items():
        average_score = data['total_score'] / data['count'] if data['count'] > 0 else 0
        responseJson["score"].append({'date': day, 'averageScore': average_score})
    
    return JsonResponse(responseJson, safe=False)

@verify_learner_token_annotation
def is_activity_completed_for_learner(request):
    email = request.email
    statements = user_xapi_service.fetch_statements_for_user(email)
    all_activities = get_all_objects_ids_used(statements)
    activities_completion = {}

    for activity_id in all_activities:
        statements_filtered_by_object = filter_statements_by_object_id(statements, activity_id)
        statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_object, construct_verb_id("completed"))
        activities_completion[activity_id] = len(statements_filtered_by_verb) > 0

    responseJson = {"activitiesCompletion": activities_completion}
    return JsonResponse(responseJson, safe=False)
@verify_learner_token_annotation
def is_activity_scored_for_learner(request):
    email = request.email
    statements = user_xapi_service.fetch_statements_for_user(email)
    all_activities = get_all_objects_ids_used(statements)
    activities_scored = {}

    for activity_id in all_activities:
        statements_filtered_by_object = filter_statements_by_object_id(statements, activity_id)
        statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_object, construct_verb_id("scored"))
        activities_scored[activity_id] = len(statements_filtered_by_verb) > 0

    responseJson = {"activitiesScored": activities_scored}
    return JsonResponse(responseJson, safe=False)
@verify_learner_token_annotation
def get_attempts_until_passed_for_learner(request):
    email = request.email
    statements = user_xapi_service.fetch_statements_for_user(email)
    all_activities = get_all_objects_ids_used(statements)
    attempts_until_passed = {}

    for activity_id in all_activities:
        statements_filtered_by_object = filter_statements_by_object_id(statements, activity_id)
        sorted_statements = sort_statements_by_timestamp(statements_filtered_by_object)

        attempts = 0
        completed = False
        

        for statement in sorted_statements:
            if get_id(statement,'verb') == construct_verb_id("scored"):
                attempts += 1
            elif get_id(statement,'verb')  == construct_verb_id("completed"):
                print(f"Activity: {get_id(statement,'object')}")
                completed = True
                break

        attempts_until_passed[activity_id] = attempts if completed else 0

    responseJson = {"attemptsUntilPassed": attempts_until_passed}
    return JsonResponse(responseJson, safe=False)

def count_each_verb_for_learner(request):
    email = request.email
    statements = xapi_service.fetch_statements()
    statements_of_learner = get_statements_of_specfic_user_by_email(statements, email)
    all_verbs = get_all_verbs_ids_used(statements)
    verbs = {}

    for statement in statements_of_learner:
        activity_id = statement['object']['id']
        verb_id = statement['verb']['id']
        if activity_id not in verbs:
            verbs[activity_id] = {verb: 0 for verb in all_verbs}
        if verb_id not in verbs[activity_id]:
            verbs[activity_id][verb_id] = 0
        verbs[activity_id][verb_id] += 1

    responseJson = {"verbs": verbs}
    return JsonResponse(responseJson, safe=False)

def time_spent_on_each_activity_for_learner(request):
    email = request.email
    statements = user_xapi_service.fetch_statements_for_user(email)
    durations = get_duration_of_activities(statements)
    total_time = sum(duration["duration"] for duration in durations.values())
    
    responseJson = {
        "activities:": durations,
        "totalTime": total_time
    }
    
    return JsonResponse(responseJson, safe=False)
@verify_learner_token_annotation
def get_passed_and_failed_tests_for_learner(request):
    email = request.email
    statements = xapi_service.fetch_statements()
    statements_of_user = get_statements_of_specfic_user_by_email(statements, email)
    
    all_subcourses = get_all_courses(statements_of_user)
    all_activities = []

    for subcourse_id in all_subcourses:
        statements_filtered_by_subcourse = filter_statements_by_course_id(statements, subcourse_id)
        all_activities_of_subcourse = get_all_objects_ids_used(statements_filtered_by_subcourse)
        all_activities += all_activities_of_subcourse
        
    durations = get_durations_of_tests_for_user(statements_of_user)
    passed = sum(duration["result"] == "completed" for duration in durations)
    failed = sum(duration["result"] == "failed" for duration in durations)
    open_activities = len(all_activities)-passed
    responseJson = {
        "passed": passed,
        "failed": failed,
        "open": open_activities
    }
    
    return JsonResponse(responseJson, safe=False)

@verify_instructor_token_annotation
def get_passed_and_failed_tests_for_instructor(request):
    instructor_email = request.email
    statements = xapi_service.fetch_statements()
    all_user_emails = get_all_actors_emails_used(statements)
    statements_of_instructor = filter_statements_by_instructor_email(statements, instructor_email)
    user_results = {}


    for email in all_user_emails:
        statements_of_learner = get_statements_of_specfic_user_by_email(statements_of_instructor, email)
        # Filter statements by instructor
        
        sorted_statements = sort_statements_by_timestamp(statements_of_learner)
        activities = get_all_objects_ids_used(statements_of_instructor)
        print(activities)
        durations = get_durations_of_tests_for_user(sorted_statements)
        passed = sum(duration["result"] == "completed" for duration in durations)
        failed = sum(duration["result"] == "failed" for duration in durations)
        open_activities = len(activities) - passed
        
        user_results[email] = {
            "passed": passed,
            "failed": failed,
            "open": open_activities
        }

    responseJson = {"userResults": user_results}
    return JsonResponse(responseJson, safe=False)

def get_last_rating_for_all_activities(request):
    email = request.email
    statements = user_xapi_service.fetch_statements_for_user(email)
    all_activities = get_all_objects_ids_used(statements)
    activities_ratings = []

    for activity_id in all_activities:
        statements_filtered_by_object = filter_statements_by_object_id(statements, activity_id)
        statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_object, construct_verb_id("rated"))
        sorted_statements = sort_statements_by_timestamp(statements_filtered_by_verb)
        
        if sorted_statements:
            last_rating = sorted_statements[-1]['result']['score']['raw']
            timestamp = sorted_statements[-1]['timestamp']
        else:
            last_rating = 0
            timestamp = None
        
        activities_ratings.append({
            "activityId": activity_id,
            "lastRating": last_rating,
            "timestamp": timestamp
        })

    responseJson = {"activitiesRatings": activities_ratings}
    return JsonResponse(responseJson, safe=False)

@verify_instructor_token_annotation
def get_rating_of_all_users_for_instructor(request):
    instructor_email = request.email
    statements = xapi_service.fetch_statements()
    all_user_emails = get_all_actors_emails_used(statements)
    statements_of_instructor = filter_statements_by_instructor_email(statements, instructor_email)
    user_ratings = {}

    for email in all_user_emails:
        statements_of_learner = get_statements_of_specfic_user_by_email(statements_of_instructor, email)
        statements_filtered_by_verb = filter_statements_by_verb_id(statements_of_learner, construct_verb_id("rated"))
        sorted_statements = sort_statements_by_timestamp(statements_filtered_by_verb)
        
        if sorted_statements:
            ratings = [get_score(statement) for statement in sorted_statements]
            mean_rating = sum(ratings) / len(ratings)
        else:
            mean_rating = 0
        
        user_ratings[email] = mean_rating

    responseJson = {"userRatings": user_ratings}
    return JsonResponse(responseJson, safe=False)

@verify_learner_token_annotation
def get_last_rating_of_user_for_each_activity(request):
     email = request.email
     statements = user_xapi_service.fetch_statements_for_user(email)
     statements_filtered_by_verb = filter_statements_by_verb_id(statements, construct_verb_id("rated"))
     sorted_statements = sort_statements_by_timestamp(statements_filtered_by_verb)
    
     last_ratings = {}
     for statement in sorted_statements:
        activity_id = get_id(statement, "object")
        if activity_id not in last_ratings:
            last_ratings[activity_id] = {
                "score": get_score(statement),
                "timestamp": statement['timestamp']
            }
    
     responseJson = {"lastRatings": last_ratings}
    
     return JsonResponse(responseJson, safe=False)

@verify_instructor_token_annotation
def get_mean_rating_for_all_activities_for_instructor(request):
    try:
        instructor_email = request.email
        statements = xapi_service.fetch_statements()
        statements_of_instructor = filter_statements_by_instructor_email(statements, instructor_email)
        all_activities = get_all_objects_ids_used(statements_of_instructor)
        activities_ratings = []

        for activity_id in all_activities:
            statements_filtered_by_object = filter_statements_by_object_id(statements_of_instructor, activity_id)
            statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_object, construct_verb_id("rated"))
            total_rating = 0
            count = 0

            for statement in statements_filtered_by_verb:
                if 'result' in statement['statement_payload'] and 'score' in statement['statement_payload']['result']:
                    total_rating += statement['statement_payload']['result']['score']['raw']
                    count += 1

            mean_rating = total_rating / count if count > 0 else 0
            activities_ratings.append({
                "activityId": activity_id,
                "meanRating": mean_rating
            })

        responseJson = {"activitiesRatings": activities_ratings}
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)

@verify_learner_token_annotation
def learning_efficiency_for_learner(request):
    email = request.email
    statements = user_xapi_service.fetch_statements_for_user(email)
    all_activities = get_all_objects_ids_used(statements)
    activities_efficiency = []

    for activity_id in all_activities:
        
        statements_filtered_by_object = filter_statements_by_object_id(statements, activity_id)
        sorted_statements = sort_statements_by_timestamp(statements_filtered_by_object)
        durations_of_tests = get_durations_of_tests_for_user(sorted_statements)
        durations_of_activities = get_duration_of_activities(sorted_statements)

        # Combine durations of tests and activities
        for test_duration in durations_of_tests:
            print(test_duration)
            for activity_duration in durations_of_activities:
                if test_duration['object_id'] == activity_duration['activityId']:
                    test_duration['duration'] += activity_duration['duration']
                    break
        scores = []
        for duration in durations_of_tests:
            scores.append({
                "duration": duration["duration"].total_seconds() / 60,  # Convert duration to minutes
                "score": duration["score"],
                "timestamp": duration["timestamp"]
            })
        
        activities_efficiency.append({
            "activityId": activity_id,
            "scores": scores
        })

    responseJson = {"activitiesEfficiency": activities_efficiency}
    return JsonResponse(responseJson, safe=False)

@verify_learner_token_annotation
def active_hours_in_the_current_week_for_learner(request):
    email = request.user['email']  # Corrected to access email from authenticated user
    statements_of_learner =  user_xapi_service.fetch_statements_for_user(email)
    
    current_date = datetime.now()
    start_of_week = current_date - timedelta(days=current_date.weekday())
    
    statements_filtered_by_week = [
        statement for statement in statements_of_learner
        if start_of_week.date() <= statement['timestamp'].date() <= (start_of_week + timedelta(days=6)).date()
    ]
    
    active_hours = [{"day": (start_of_week + timedelta(days=i)).strftime('%A'), "hours": [{"hour": h, "timeSpent": 0} for h in range(24)]} for i in range(7)]
    
    durations = get_duration_of_activities(statements_filtered_by_week)
    for duration_info in durations:
        test_start = duration_info['test_start']
        test_end = duration_info['test_end']
        current_time = test_start
        while current_time < test_end:
            next_hour = (current_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
            if next_hour > test_end:
                next_hour = test_end
            duration = (next_hour - current_time).total_seconds() / 60  # Convert duration to minutes
            statement_date = current_time.date()
            day_index = (statement_date - start_of_week.date()).days
            if 0 <= day_index < 7:  # Ensure day_index is within range
                hour = current_time.hour
                active_hours[day_index]["hours"][hour]["timeSpent"] += duration
            current_time = next_hour
    
    responseJson = {"activeHours": active_hours}
    
    return JsonResponse(responseJson, safe=False)
@verify_learner_token_annotation
def count_verbs_for_all_activities_for_learner(request):
    email = request.email
    statements = xapi_service.fetch_statements()
    statements_of_learner = get_statements_of_specfic_user_by_email(statements, email)
    all_activities = get_all_objects_ids_used(statements_of_learner)
    all_verbs = get_all_verbs_name_used(statements)
    verbs_count = {}

    for activity_id in all_activities:
        statements_filtered_by_activity = filter_statements_by_object_id(statements_of_learner, activity_id)
        verbs_count[activity_id] = {verb: 0 for verb in all_verbs}
        for statement in statements_filtered_by_activity:
            verb_id = get_name_of_verb_by_id(statement)
            if verb_id in verbs_count[activity_id]:
                verbs_count[activity_id][verb_id] += 1

    responseJson = {"verbsCount": verbs_count}
    return JsonResponse(responseJson, safe=False)

def get_all_object_names_and_ids(request, **kwargs):
    try:
        language = str(kwargs.get('language', "de-DE"))
        
        statements = xapi_service.fetch_statements()
        all_objects = get_all_objects_ids_used(statements)
        object_names_and_ids = []

        for object_id in all_objects:
            object_name = get_object_name_by_id(statements, object_id,language)
            object_names_and_ids.append({
                "objectId": object_id,
                "objectName": object_name
            })

        responseJson = {"objects": object_names_and_ids}
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)

def get_parents_of_all_activities(request):
    try:
        statements = xapi_service.fetch_statements()
        activity_parents = {}

        def get_parents(statement):
            parents = []
            if 'context' in statement['statement_payload'] and 'contextActivities' in statement['statement_payload']['context']:
                context_activities = statement['statement_payload']['context']['contextActivities']
                if 'parent' in context_activities:
                    parent_activities = context_activities['parent']
                    for parent in parent_activities:
                        parents.append(parent['id'])
            return parents

        for statement in statements:
            child_activity_id = statement['statement_payload']['object']['id']
            parent_activity_ids = get_parents(statement)
            if parent_activity_ids:
                if child_activity_id not in activity_parents:
                    activity_parents[child_activity_id] = parent_activity_ids
                else:
                    # Ensure the sequence of parent IDs is consistent
                    for parent_id in parent_activity_ids:
                        if parent_id not in activity_parents[child_activity_id]:
                            activity_parents[child_activity_id].append(parent_id)

        responseJson = {"activityParents": activity_parents}
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
        
def get_parent_of_all_parents(request):
    try:
        statements = xapi_service.fetch_statements()
        parent_of_parents = {}

        def get_parents(statement):
            parents = []
            if 'context' in statement['statement_payload'] and 'contextActivities' in statement['statement_payload']['context']:
                context_activities = statement['statement_payload']['context']['contextActivities']
                if 'parent' in context_activities:
                    parent_activities = context_activities['parent']
                    for parent in parent_activities:
                        parents.append(parent['id'])
            return parents

        for statement in statements:
            parent_activity_ids = get_parents(statement)
            if parent_activity_ids:
                for parent_id in parent_activity_ids:
                    parents=get_parents(statement)
                    if parent_id =="http://example.com/activities/Grundlagen_der_Baumpflege":
                            print(parents)
                    parent_of_parents[parent_id] = parents[-1]
                        

        responseJson = {"parentOfParents": parent_of_parents}
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
        
@verify_learner_token_annotation
def get_initialization_streak_for_learner(request):
    email = request.email
    statements = user_xapi_service.fetch_statements_for_user(email)
    statements_filtered_by_verb = filter_statements_by_verb_id(statements, construct_verb_id("initialized"))
    sorted_statements = sort_statements_by_timestamp(statements_filtered_by_verb)

    if not sorted_statements:
        return JsonResponse({"streak": 0, "lastDate": None}, safe=False)

    streak = 1
    last_streak = 1
    last_date = sorted_statements[0]['timestamp'].date()
    
    for i in range(1, len(sorted_statements)):
        current_date = sorted_statements[i]['timestamp'].date()
        
        if (current_date - last_date).days == 1:
            streak += 1
        elif current_date != last_date:
            last_streak = streak
            streak = 1  # Neustart der Streak

        last_date = current_date

    return JsonResponse({"lastStreak": last_streak, "lastDate": last_date.strftime("%Y-%m-%d")}, safe=False)

@verify_learner_token_annotation
def get_time_spent_daily_for_last_week(request):
    email = request.email
    statements = user_xapi_service.fetch_statements_for_user(email)
    current_date = datetime.now().date()
    start_date = current_date - timedelta(days=6)
    
    time_spent_daily = [{"day": (start_date + timedelta(days=i)).strftime('%A'), "minutes": 0} for i in range(7)]
    
    statements_filtered_by_week = [
        statement for statement in statements
        if start_date <= statement['timestamp'].date() <= current_date
    ]
    
    durations = get_duration_of_activities(statements_filtered_by_week)
    for duration_info in durations:
        test_start = duration_info['test_start']
        test_end = duration_info['test_end']
        current_time = test_start
        while current_time < test_end:
            next_hour = (current_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
            if next_hour > test_end:
                next_hour = test_end
            duration = (next_hour - current_time).total_seconds() / 60  # Convert duration to minutes
            statement_date = current_time.date()
            day_index = (statement_date - start_date).days
            if 0 <= day_index < 7:  # Ensure day_index is within range
                time_spent_daily[day_index]["minutes"] += duration
            current_time = next_hour
    
    responseJson = {"timeSpentDaily": time_spent_daily}
    return JsonResponse(responseJson, safe=False)

@verify_learner_token_annotation
def get_assigned_and_completed_activities_for_learner(request):
    email = request.email
    statements = xapi_service.fetch_statements()
    statements_of_learner = get_statements_of_specfic_user_by_email(statements, email)
    all_subcourses = get_all_courses(statements_of_learner)
    subcourses_summary = []

    for subcourse_id in all_subcourses:
        statements_filtered_by_subcourse = filter_statements_by_course_id(statements_of_learner, subcourse_id)
        statements_filtered_by_sucourse_all = filter_statements_by_course_id(statements, subcourse_id)
        all_activities = get_all_objects_ids_used(statements_filtered_by_sucourse_all)
        total_assessments = len(all_activities)
        completed_assessments = 0
        assessments = []

        for activity_id in all_activities:
            statements_filtered_by_activity = filter_statements_by_object_id(statements_filtered_by_subcourse, activity_id)
            statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_activity, construct_verb_id("completed"))
            status = "passed" if len(statements_filtered_by_verb) > 0 else "not passed"
            if status == "passed":
                completed_assessments += 1
            assessments.append({
                "activityId": activity_id,
                "status": status
            })

        progress = (completed_assessments / total_assessments) * 100 if total_assessments > 0 else 0
        subcourses_summary.append({
            "name": subcourse_id,
            "progress": progress,
            "completedAssessments": completed_assessments,
            "totalAssessments": total_assessments,
            "assessments": assessments
        })

    responseJson = {"subcourses": subcourses_summary}
    return JsonResponse(responseJson, safe=False)