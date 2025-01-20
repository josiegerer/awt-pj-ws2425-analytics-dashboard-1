
#Number of searches conducted on specific keyword
from django.http import JsonResponse
from dashboard.xapi_service import XAPIService
from xapi.lrs_utils import  fetch_xapi_statements_from_db, fetch_xapi_statements_from_db
from xapi.xapi_utils import construct_activity_id, construct_verb_id, filter_statements_by_instructor_email, filter_statements_by_object_id, filter_statements_by_course_id, get_all_actors_emails_used, get_all_courses, get_all_objects_ids_used, get_all_user_names, get_all_verbs_ids_used, get_duration_of_activities, get_durations_of_tests_for_user, get_open_activities, get_statements_in_last_days, filter_statements_by_verb_id, get_statements_of_specfic_user_by_email, get_statements_with_specific_hour, sort_statements_by_timestamp
from datetime import datetime, timedelta

xapi_service = XAPIService(cache_duration=300) 

def get_popularity_of_resources(request, **kwargs):
    try:
        statements = xapi_service.fetch_statements()
        keyword = str(kwargs.get('keyword', 'actor'))
        verb_id = construct_verb_id("searched")
        object_id = construct_activity_id(keyword)
        # Filter statements by verb searched
        statements_filtered_by_id = filter_statements_by_verb_id(statements, verb_id)
        # Filter statements by object id
        statements_filtered_by_object_id = filter_statements_by_object_id(statements_filtered_by_id, object_id)

        responseJson = {"searchCount": len(statements_filtered_by_object_id)}

        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
        
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

def get_all_courses_count(request):
    try:
        statements = xapi_service.fetch_statements()
        all_courses= get_all_courses(statements)

        responseJson = {"totalCourses": len(all_courses)}
        
        return JsonResponse(responseJson, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
        
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
    
    return JsonResponse(responseJson, safe=False)
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
    
    all_user_emails = get_all_actors_emails_used(statements)
     
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

def get_all_vists_of_activity(request):
    statements = xapi_service.fetch_statements()
    activity_id = request.GET.get('activityId')
    
    statements_filtered_by_object_id = filter_statements_by_object_id(statements, activity_id)
    
    statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_object_id, construct_verb_id("initialized"))
    
    responseJson = {"visits": len(statements_filtered_by_verb)}
    
    return JsonResponse(responseJson, safe=False)

def get_average_score_for_subcourse(request):
    statements= xapi_service.fetch_statements()
    activity_id = request.GET.get('courseId')
    statements_filtered_by_subcourse_id =filter_statements_by_course_id(statements, activity_id)
    staments_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_subcourse_id, construct_verb_id("scored"))
    total_score = 0
    count = 0
    for statement in staments_filtered_by_verb:
        if 'result' in statement and 'score' in statement['result']:
            total_score += statement['result']['score']['raw']
            count += 1
    average_score = total_score / count if count > 0 else 0
    responseJson = {"averageScore": average_score}
    return JsonResponse(responseJson, safe=False)

def get_activitiy_completion_and_assigned(request):
    statements = xapi_service.fetch_statements()
    activity_id = request.GET.get('activityId')
    
    statements_filtered_by_object = filter_statements_by_object_id(statements,activity_id)
    all_users_of_filtered_statements = get_all_actors_emails_used(statements_filtered_by_object)
    statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_object, construct_verb_id("completed"))
    all_users_who_completed = get_all_actors_emails_used(statements_filtered_by_verb)
    
    responseJson = {"assigned": len(all_users_of_filtered_statements),
                    "completed": len(all_users_who_completed)}
                               

    return JsonResponse(responseJson, safe=False)

def get_active_user_in_cours_in_last_days(request,**kwargs):
    statements = xapi_service.fetch_statements()
    days = str(kwargs.get('days', 0))
    subcourse_id= request.GET.get('courseId')
    statements_filtered_by_time = get_statements_in_last_days(statements, days)
    statements_filtered_by_subcourse_id = filter_statements_by_course_id(statements_filtered_by_time, subcourse_id)
    unique_users =  get_all_actors_emails_used(statements_filtered_by_subcourse_id)
    responseJson = {"activeUser": len(unique_users)}
    return JsonResponse(responseJson, safe=False)

def get_list_of_activities_of_instructor(request):
    instructor_email = request.email
    statements = xapi_service.fetch_statements()
    statements_of_instructor = filter_statements_by_instructor_email(statements, instructor_email)
    all_objects = get_all_objects_ids_used(statements_of_instructor)
    responseJson = {"activities": all_objects}
    return JsonResponse(responseJson, safe=False)

def get_list_of_activities_of_learner(request):
    email = request.email
    statements = xapi_service.fetch_statements()
    statements_of_learner = get_statements_of_specfic_user_by_email(statements, email)
    all_objects = get_all_objects_ids_used(statements_of_learner)
    responseJson = {"activities": all_objects}
    return JsonResponse(responseJson, safe=False)

def get_activity_completion_and_assigned_for_learner(request):
    email= request.email
    activity_id = request.GET.get('activityId')
    statements = xapi_service.fetch_statements()
    statements_of_learner=get_statements_of_specfic_user_by_email(statements, email)
    
    
    statements_filtered_by_object = filter_statements_by_object_id(statements_of_learner,activity_id)
    all_users_of_filtered_statements = get_email_of_all_users(statements_filtered_by_object)
    statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_object, construct_verb_id("completed"))
    responseJson = {"assigned": len(all_users_of_filtered_statements),
                    "completed": len(statements_filtered_by_verb)}
    return JsonResponse(responseJson, safe=False)
    
                  
def get_scoring_progress_array(request):
    
    # Macht keinen Sinn
    email= request.email
    statements = xapi_service.fetch_statements()
    statements_of_learner=get_statements_of_specfic_user_by_email(statements, email)
    
    statements_filtered_by_verb = filter_statements_by_verb_id(statements_of_learner, construct_verb_id("scored"))
    scores_by_day = {}
    responseJson = {"score": []}
    
    for statement in statements_filtered_by_verb:
        if 'result' in statement and 'score' in statement['result']:
            timestamp = statement['timestamp'][:10]  # Extract the date part
            if timestamp not in scores_by_day:
                scores_by_day[timestamp] = {'total_score': 0, 'count': 0}
            scores_by_day[timestamp]['total_score'] += statement['result']['score']['raw']
            scores_by_day[timestamp]['count'] += 1
    
    for day, data in scores_by_day.items():
        average_score = data['total_score'] / data['count'] if data['count'] > 0 else 0
        responseJson["score"].append({'date': day, 'averageScore': average_score})
    
    return JsonResponse(responseJson, safe=False)

def is_activity_completed_for_learner(request):
    email= request.email
    activity_id = request.GET.get('activityId')
    statements = xapi_service.fetch_statements()
    statements_of_learner=get_statements_of_specfic_user_by_email(statements, email)
    statements_filtered_by_object = filter_statements_by_object_id(statements_of_learner,activity_id)
    statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_object, construct_verb_id("completed"))
    responseJson = {"passed": len(statements_filtered_by_verb) > 0}
    return JsonResponse(responseJson, safe=False)

def get_attempts_until_passed_for_learner(request):
    email = request.email
    activity_id = request.GET.get('activityId')
    statements = xapi_service.fetch_statements()
    statements_of_learner = get_statements_of_specfic_user_by_email(statements, email)
    statements_filtered_by_object = filter_statements_by_object_id(statements_of_learner, activity_id)
    sorted_statements = sort_statements_by_timestamp(statements_filtered_by_object)

    attempts = 0
    completed = False

    for statement in sorted_statements:
        if statement['verb']['id'] == construct_verb_id("scored"):
            attempts += 1
        elif statement['verb']['id'] == construct_verb_id("completed"):
            completed = True
            break

    responseJson = {"attempts": attempts if completed else 0}
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
    statements = xapi_service.fetch_statements()
    statements_of_learner = get_statements_of_specfic_user_by_email(statements, email)
    sorted_statements = sort_statements_by_timestamp(statements_of_learner)
    durations = get_duration_of_activities(sorted_statements)
    total_time = sum(duration["duration"] for duration in durations.values())
    
    responseJson = {
        "activities:": durations,
        "totalTime": total_time
    }
    
    return JsonResponse(responseJson, safe=False)

def get_passed_and_failed_tests_for_learner(request):
    email = request.email
    statements = xapi_service.fetch_statements()
    statements_of_learner = get_statements_of_specfic_user_by_email(statements, email)
    sorted_statements = sort_statements_by_timestamp(statements_of_learner)
    open_statements= get_open_activities(statements_of_learner)
    durations = get_durations_of_tests_for_user(sorted_statements)
    passed = sum(duration["result"] == "completed" for duration in durations.values())
    failed = sum(duration["result"] == "failed" for duration in durations.values())
    open_activities = len(open_statements)
    responseJson = {
        "passed": passed,
        "failed": failed,
        "open": open_activities
    }
    
    return JsonResponse(responseJson, safe=False)

def get_passed_and_failed_tests_for_instructor(request):
    instructor_email = request.email
    statements = xapi_service.fetch_statements()
    all_user_emails = get_email_of_all_users(statements)
    statements_of_instructor = filter_statements_by_instructor_email(statements, instructor_email)
    user_results = {}

    for email in all_user_emails:
        statements_of_learner = get_statements_of_specfic_user_by_email(statements_of_instructor, email)
        # Filter statements by instructor
        
        sorted_statements = sort_statements_by_timestamp(statements_of_learner)
        open_statements = get_open_activities(statements_of_learner)
        durations = get_durations_of_tests_for_user(sorted_statements)
        passed = sum(duration["result"] == "completed" for duration in durations.values())
        failed = sum(duration["result"] == "failed" for duration in durations.values())
        open_activities = len(open_statements)
        
        user_results[email] = {
            "passed": passed,
            "failed": failed,
            "open": open_activities
        }

    responseJson = {"userResults": user_results}
    return JsonResponse(responseJson, safe=False)

def get_rating_of_activity_for_learner(request):
    email = request.email
    activity_id = request.GET.get('activityId')
    statements = xapi_service.fetch_statements()
    statements_of_learner = get_statements_of_specfic_user_by_email(statements, email)
    statements_filtered_by_object = filter_statements_by_object_id(statements_of_learner, activity_id)
    statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_object, construct_verb_id("rated"))
    statement_sort=sort_statements_by_timestamp(statements_filtered_by_verb)
    
    if statement_sort:
        last_rating = statements_filtered_by_verb[-1]['result']['score']['raw']
    else:
        last_rating = 0
    
    responseJson = {"lastRating": last_rating}
    return JsonResponse(responseJson, safe=False)

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
            last_rating = sorted_statements[-1]['result']['score']['raw']
        else:
            last_rating = 0
        
        user_ratings[email] = last_rating

    responseJson = {"userRatings": user_ratings}
    return JsonResponse(responseJson, safe=False)

def learning_efficiency_for_learner(request):
    email = request.email
    activity_id = request.GET.get('activityId')
    statements = xapi_service.fetch_statements()
    statements_of_learner = get_statements_of_specfic_user_by_email(statements, email)
    statements_filtered_by_object = filter_statements_by_object_id(statements_of_learner, activity_id)
    sorted_statements = sort_statements_by_timestamp(statements_filtered_by_object)
    durations = get_durations_of_tests_for_user(sorted_statements)
    scores=[]
    for duration in durations:
        object= {
            "duration": duration["duration"],
            "score": duration["score"],
            "timestamp": duration["timestamp"]
        }
        scores.append(object)
  
    responseJson = {"scores": scores}
    return JsonResponse(responseJson, safe=False)

def active_hours_in_the_current_week_for_learner(request):
    statements = xapi_service.fetch_statements()
    email = request.user.email  # Corrected to access email from authenticated user
    statements_of_learner = get_statements_of_specfic_user_by_email(statements, email)
    
    current_date = datetime.now()
    start_of_week = current_date - timedelta(days=current_date.weekday())
    
    statements_filtered_by_week = [
        statement for statement in statements_of_learner
        if datetime.strptime(statement['timestamp'][:10], '%Y-%m-%d') >= start_of_week
    ]
    
    active_hours = [{"day": (start_of_week + timedelta(days=i)).strftime('%A'), "hours": [{"hour": h, "timeSpent": 0} for h in range(24)]} for i in range(7)]
    
    durations = get_duration_of_activities(statements_filtered_by_week)
    for duration_info in durations:
        test_start = datetime.strptime(duration_info['test_start'], '%Y-%m-%dT%H:%M:%S')
        test_end = datetime.strptime(duration_info['test_end'], '%Y-%m-%dT%H:%M:%S')
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