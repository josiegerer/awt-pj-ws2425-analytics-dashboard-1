from django.http import JsonResponse
from authentification.views import verify_admin_token_annotation, verify_instructor_token_annotation, verify_learner_token_annotation
from dashboard.xapi_services import UserXAPIService, XAPIService
from xapi.xapi_utils import construct_verb_id, filter_statements_by_instructor_email, filter_statements_by_object_id, filter_statements_by_course_id, get_all_actors_emails_used, get_all_courses, get_all_objects_ids_used, get_all_objects_names_used, get_all_user_names, get_all_verbs_ids_used, get_all_verbs_name_used, get_duration_of_activities, get_durations_of_tests_for_user, get_id, get_name_of_verb_by_id, get_object_name, get_object_name_by_id, get_open_activities, get_score, get_start_end_times_of_activities, get_statements_in_last_days, filter_statements_by_verb_id, get_statements_of_specfic_user_by_email, get_statements_with_specific_hour, sort_statements_by_timestamp
from datetime import datetime, timedelta

xapi_service = XAPIService(cache_duration=300) 
user_xapi_service=UserXAPIService(cache_duration=300) 


@verify_admin_token_annotation
def get_search_count_for_each_activity(request):
    """
    Retrieve the count of search activities for each activity from xAPI statements.
    This function fetches xAPI statements, filters them by the "searched" verb, and counts the occurrences
    of each activity ID within the filtered statements. The result is returned as a JSON response.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        JsonResponse: A JSON response containing the search count for each activity or an error message.
    """
    
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
    """
    Get the count of active users for a given timeslot.
    This function fetches xAPI statements, filters them by a specified time period and verb,
    and then counts the unique users who have initialized actions within that period.
    Args:
        request (HttpRequest): The HTTP request object.
        **kwargs: Additional keyword arguments. Expected to contain:
            - 'days' (int, optional): The number of days to look back for filtering statements. Defaults to 30.
    Returns:
        JsonResponse: A JSON response containing the count of active users or an error message.
    Raises:
        Exception: If any error occurs during the process, it returns a JSON response with the error message and a 500 status code.
    """
    
    try:
        statements = xapi_service.fetch_statements()

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
    """
    Retrieve the count of active users for each subcourse within a specified timeslot.
    This function fetches xAPI statements, filters them based on the provided number of days,
    and then calculates the number of unique active users for each subcourse.
    Args:
        request (HttpRequest): The HTTP request object.
        **kwargs: Arbitrary keyword arguments. Expected to contain 'days' which specifies the 
                  number of days to look back for filtering statements. Defaults to 30 days if not provided.
    Returns:
        JsonResponse: A JSON response containing a dictionary with subcourse IDs as keys and the 
                      count of unique active users as values. In case of an error, returns a JSON 
                      response with an error message and a 500 status code.
    Raises:
        Exception: If any error occurs during the process, it is caught and returned in the JSON response.
    """
    
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
    """
    Retrieves the count of active users for each subcourse of an instructor within a specified timeslot.
    Args:
        request (HttpRequest): The HTTP request object containing the instructor's email.
        **kwargs: Additional keyword arguments.
            - days (int, optional): The number of days to look back for activity. Defaults to 30.
    Returns:
        JsonResponse: A JSON response containing the count of active users for each subcourse.
            Format:
            {
                "activeUsersBySubcourse": {
                    "subcourse_id_1": active_user_count_1,
                    "subcourse_id_2": active_user_count_2,
                    ...
                }
            }
            In case of an error, returns a JSON response with an error message and a 500 status code.
    """
    
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
    """
    Handle the request to get all courses.
    This view function fetches xAPI statements using the xapi_service, processes them to get all courses,
    and returns the total number of courses in a JSON response.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        JsonResponse: A JSON response containing the total number of courses or an error message with status 500.
    """
    
    
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
    """
    Retrieve the total count of unique users based on xAPI statements.
    This view function fetches xAPI statements using the xapi_service, extracts unique user emails,
    and returns the total count of these unique users in a JSON response.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        JsonResponse: A JSON response containing the total count of unique users or an error message.
    Raises:
        Exception: If an error occurs during the process, a JSON response with the error message and a 500 status code is returned.
    """
    
    
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
    """
    Fetches a list of all activity IDs from xAPI statements and returns them as a JSON response.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        JsonResponse: A JSON response containing a list of all activity IDs or an error message.
    """
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
    """
    Retrieve the count of all unique activity objects from xAPI statements.
    This view function fetches xAPI statements using the xapi_service, extracts unique object IDs,
    and returns the count of these unique objects in a JSON response.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        JsonResponse: A JSON response containing the total count of unique objects or an error message.
        - If successful, the response contains a JSON object with the key "totalObjects" and the count as its value.
        - If an error occurs, the response contains a JSON object with the key "error" and the error message as its value,
          and the HTTP status code is set to 500.
    """
    
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
    """
    Retrieve the total number of unique users for a specific hour.
    This function fetches statements using the xAPI service, filters them by the specified hour,
    and then extracts the unique user emails from the filtered statements. The total number of
    unique users is returned as a JSON response.
    Args:
        request (HttpRequest): The HTTP request object.
        **kwargs: Arbitrary keyword arguments. Expected to contain 'hour' which specifies the hour to filter statements by.
    Returns:
        JsonResponse: A JSON response containing the total number of unique users for the specified hour.
                      If an error occurs, a JSON response with the error message and a 500 status code is returned.
    """
    
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
    """
    Fetches and returns the number of active users for each hour of the current day.
    This function retrieves xAPI statements, filters them by the current date, and counts the number of unique active users for each hour. The result is returned as a JSON response.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        JsonResponse: A JSON response containing the number of active users for each hour of the current day.
        If an error occurs, a JSON response with the error message and a 500 status code is returned.
    """
    
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
    
@verify_admin_token_annotation    
def get_all_activities_summary(request):
    """
    Fetches and summarizes activity data from xAPI statements.
    This function retrieves xAPI statements, processes them to extract activity
    data, and computes summaries for each activity, including total visits,
    average score, and average time spent. The results are returned as a JSON response.
    Args:
        request: The HTTP request object.
    Returns:
        JsonResponse: A JSON response containing the summary of activities or an error message.
    """
    
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
                durations += get_duration_of_activities(statements_filtered_by_user)
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
        
@verify_instructor_token_annotation    
def get_all_activities_summary_for_instructor(request):
    """
    Retrieve a summary of all activities for a specific instructor.
    This function fetches xAPI statements, filters them by the instructor's email,
    and then processes these statements to generate a summary of activities. The summary
    includes the total visits, average score, and average time spent on each activity.
    Args:
        request (HttpRequest): The HTTP request object containing the instructor's email.
    Returns:
        JsonResponse: A JSON response containing the summary of activities or an error message.
    The response JSON structure:
    {
        "activitiesSummary": [
            {
                "activityId": str,
                "totalVisits": int,
                "averageScore": float,
                "averageTimeSpent": float
            },
            ...
        ]
    }
    Error Response:
    {
        "error": str
    }
    """
    
    try:
        statements =  xapi_service.fetch_statements()
        statements_of_instructor = filter_statements_by_instructor_email(statements, request.email)
        all_activities = get_all_objects_ids_used(statements_of_instructor)
        activities_summary = []

        for activity_id in all_activities:
            # Get the total visits
            statements_filtered_by_object_id = filter_statements_by_object_id(statements_of_instructor, activity_id)
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
                durations += get_duration_of_activities(statements_filtered_by_user)
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
        
@verify_instructor_token_annotation
def get_average_timespent_for_all_activities_for_instructor(request):
    """
    Calculate the average time spent on all activities for an instructor.
    This function fetches xAPI statements for a given instructor, extracts all activity IDs,
    and calculates the average time spent on each activity by all users.
    Args:
        request (HttpRequest): The HTTP request object containing the instructor's email.
    Returns:
        JsonResponse: A JSON response containing a summary of activities with their average time spent.
    The JSON response has the following structure:
        {
            "activitiesSummary": [
                {
                    "activityId": str,
                    "averageTime": float
                },
                ...
            ]
        }
    """
   
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

@verify_instructor_token_annotation
def get_all_visits_of_all_activities_of_instructor(request):
    """
    Retrieve the number of visits for all activities associated with a specific instructor.
    This function fetches xAPI statements, filters them by the instructor's email, and then
    counts the number of 'initialized' verb occurrences for each activity associated with the instructor.
    Args:
        request (HttpRequest): The HTTP request object containing the instructor's email.
    Returns:
        JsonResponse: A JSON response containing a list of activities with their corresponding visit counts.
        The response format is:
        {
            "activitiesVisits": [
                {
                    "activityId": str,
                    "visits": int
                },
                ...
            ]
        }
    """
    
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
    """
    Retrieve the number of visits for all activities performed by a specific learner.
    This function fetches xAPI statements, filters them by the learner's email, 
    and then counts the number of 'initialized' verb occurrences for each activity 
    the learner has interacted with.
    Args:
        request (HttpRequest): The HTTP request object containing the learner's email.
    Returns:
        JsonResponse: A JSON response containing a list of activities with their 
                      corresponding visit counts.
    """
    
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


@verify_instructor_token_annotation
def get_average_score_for_all_subcourses_for_instructor(request):
    """
    Calculate the average score for all subcourses for a given instructor.
    This function fetches xAPI statements for the instructor identified by the email in the request,
    filters the statements by subcourse and verb (scored), and calculates the average score for each subcourse.
    The results are returned as a JSON response.
    Args:
        request (HttpRequest): The HTTP request object containing the instructor's email.
    Returns:
        JsonResponse: A JSON response containing the average scores for each subcourse or an error message.
    Raises:
        Exception: If any error occurs during the process, an error message is returned in the JSON response.
    """
    
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
        
@verify_learner_token_annotation
def get_time_spent_in_activities_for_learner(request):
    """
    Calculate the total time spent by a learner in various activities and return the details in a JSON response.
    Args:
        request (HttpRequest): The HTTP request object containing the learner's email.
    Returns:
        JsonResponse: A JSON response containing the duration spent on each activity and the total time spent.
        The response has the following structure:
        {
            "activities": [
                {
                    "activityId": str,
                    "duration": float  # Duration in minutes
                },
                ...
            ],
            "totalTime": float  # Total time in minutes
    """
    
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
    """
    Fetches and processes xAPI statements for a given instructor to determine the number of users assigned and completed activities.
    Args:
        request (HttpRequest): The HTTP request object containing the instructor's email.
    Returns:
        JsonResponse: A JSON response containing a summary of activities with the number of users assigned and completed.
    The response JSON structure:
    {
        "activitiesSummary": [
            {
                "activityId": str,
                "assigned": int,
                "completed": int
            },
            ...
        ]
    }
    """
    
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


@verify_learner_token_annotation
def get_activity_completion_and_assigned_for_subcourses(request):
    """
    Retrieves the activity completion and assigned activities for subcourses for a given user.
    This function fetches xAPI statements for the user identified by the email in the request,
    processes these statements to determine the number of activities assigned and completed
    for each subcourse, and returns a summary in JSON format.
    Args:
        request (HttpRequest): The HTTP request object containing the user's email.
    Returns:
        JsonResponse: A JSON response containing a summary of assigned and completed activities
                      for each subcourse. The response has the following structure:
                      {
                          "subcoursesSummary": [
                              {
                                  "subcourseId": <subcourse_id>,
                                  "assignedActivities": <number_of_assigned_activities>,
                                  "completedActivities": <number_of_completed_activities>
                              },
                              ...
                          ]
                      }
    """
    
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
    """
    Retrieve the scoring progress array for a user based on their email.
    This function fetches xAPI statements for a user, filters them by the "scored" verb,
    and calculates the average score per day. The results are returned as a JSON response.
    Args:
        request (HttpRequest): The HTTP request object containing the user's email.
    Returns:
        JsonResponse: A JSON response containing the average score per day in the format:
                      {
                          "score": [
                              {"date": "YYYY-MM-DD", "averageScore": float},
                              ...
                          ]
                      }
    """
    
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
def is_activity_scored_for_learner(request):
    """
    Determines if activities are scored for a specific learner based on their email.
    This function fetches xAPI statements, filters them by the learner's email, and checks if 
    each activity within the learner's subcourses has been scored. The result is returned as 
    a JSON response indicating which activities have been scored.
    Args:
        request (HttpRequest): The HTTP request object containing the learner's email.
    Returns:
        JsonResponse: A JSON response containing a dictionary where the keys are activity IDs 
                      and the values are booleans indicating whether the activity has been scored.
    """
    
    email = request.email
    statements = xapi_service.fetch_statements()
    statements_of_learner = get_statements_of_specfic_user_by_email(statements, email)
    all_subcourses = get_all_courses(statements_of_learner)
    all_activities = []

    for subcourse_id in all_subcourses:
        statements_filtered_by_subcourse = filter_statements_by_course_id(statements, subcourse_id)
        all_activities += get_all_objects_ids_used(statements_filtered_by_subcourse)
        
    activities_scored = {}

    for activity_id in all_activities:
        statements_filtered_by_object = filter_statements_by_object_id(statements_of_learner, activity_id)
        statements_filtered_by_verb = filter_statements_by_verb_id(statements_filtered_by_object, construct_verb_id("scored"))
        activities_scored[activity_id] = len(statements_filtered_by_verb) > 0

    responseJson = {"activitiesScored": activities_scored}
    return JsonResponse(responseJson, safe=False)
@verify_learner_token_annotation
def get_attempts_until_passed_for_learner(request):
    """
    Retrieves the number of attempts a learner took to pass each activity.
    This function fetches xAPI statements for a given user, filters and sorts them by activity,
    and counts the number of attempts until the learner has completed each activity. The results
    are returned as a JSON response.
    Args:
        request (HttpRequest): The HTTP request object containing the learner's email.
    Returns:
        JsonResponse: A JSON response containing a dictionary where the keys are activity IDs
                      and the values are the number of attempts taken to pass the activity.
                      If an activity is not completed, the value will be 0.
    """
    
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


@verify_learner_token_annotation
def get_passed_and_failed_tests_for_learner(request):
    """
    Retrieves the number of passed, failed, and open tests for a learner based on their email.
    Args:
        request (HttpRequest): The HTTP request object containing the learner's email.
    Returns:
        JsonResponse: A JSON response containing the counts of passed, failed, and open tests.
        The JSON response has the following structure:
        {
            "passed": int,  # Number of tests passed by the learner
            "failed": int,  # Number of tests failed by the learner
            "open": int     # Number of open activities/tests for the learner
    """
    
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
    """
    Retrieve the number of passed, failed, and open tests for each learner under a specific instructor.
    Args:
        request (HttpRequest): The HTTP request object containing the instructor's email.
    Returns:
        JsonResponse: A JSON response containing the results for each learner, including the number of passed, failed, and open tests.
    The response JSON structure is as follows:
    {
        "userResults": {
            "learner_email_1": {
                "passed": int,
                "failed": int,
                "open": int
            },
            "learner_email_2": {
                "passed": int,
                "failed": int,
                "open": int
            },
            ...
    """
    
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

@verify_instructor_token_annotation
def get_rating_of_all_users_for_instructor(request):
    """
    Retrieve the average rating of all users for a specific instructor.
    This function processes xAPI statements to calculate the average rating given by each user
    to a specified instructor. The ratings are extracted from the statements and averaged for
    each user.
    Args:
        request (HttpRequest): The HTTP request object containing the instructor's email.
    Returns:
        JsonResponse: A JSON response containing a dictionary with user emails as keys and their
                      corresponding average ratings as values.
    """
    
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
    """
    Retrieve the last rating of a user for each activity.
    This function fetches the xAPI statements for a user based on their email,
    filters the statements to include only those with the verb "rated", sorts
    them by timestamp, and then extracts the last rating for each activity.
    Args:
        request (HttpRequest): The HTTP request object containing the user's email.
    Returns:
        JsonResponse: A JSON response containing the last ratings for each activity.
                    The response structure is:
                    {
                        "lastRatings": {
                            "activity_id_1": {
                                "score": <score>,
                                "timestamp": <timestamp>
                            },
                            "activity_id_2": {
                                "score": <score>,
                                "timestamp": <timestamp>
                            },
                            ...
    """
   
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
    """
    Calculate the mean rating for all activities associated with a specific instructor.
    This function fetches xAPI statements, filters them by the instructor's email, and then calculates the mean rating
    for each activity the instructor is associated with. The ratings are aggregated and returned as a JSON response.
    Args:
        request (HttpRequest): The HTTP request object containing the instructor's email.
    Returns:
        JsonResponse: A JSON response containing the mean ratings for all activities associated with the instructor.
                      If an error occurs, a JSON response with the error message and a 500 status code is returned.
    Raises:
        Exception: If any error occurs during the processing of the statements or calculation of the mean ratings.
    """
    
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
    """
    Calculate and return the learning efficiency for a learner based on their xAPI statements.
    This function fetches xAPI statements for a user, processes the statements to calculate the 
    duration of tests and activities, and combines these durations to compute efficiency scores 
    for each activity. The results are returned as a JSON response.
    Args:
        request (HttpRequest): The HTTP request object containing the user's email.
    Returns:
        JsonResponse: A JSON response containing the efficiency scores for each activity.
    """
    
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
    """
    Calculate the active hours for a learner in the current week based on xAPI statements.
    This function fetches the xAPI statements for the authenticated user, filters them to include only those
    within the current week, and calculates the active hours for each day of the week. The active hours are
    returned as a JSON response.
    Args:
    request (HttpRequest): The HTTP request object containing the authenticated user's information.
    Returns:
    JsonResponse: A JSON response containing the active hours for each day of the current week.
                    The structure of the response is as follows:
                    {
                        "activeHours": [
                            {
                                "day": "Monday",
                                "hours": [
                                    {"hour": 0, "timeSpent": 0},
                                    {"hour": 1, "timeSpent": 0},
                                    ...
                                    {"hour": 23, "timeSpent": 0}
                            },
                            ...
                            {
                                "day": "Sunday",
                                "hours": [
                                    {"hour": 0, "timeSpent": 0},
                                    {"hour": 1, "timeSpent": 0},
                                    ...
                                    {"hour": 23, "timeSpent": 0}
                            }
                    }
    """
   
    email = request.user['email']  # Corrected to access email from authenticated user
    statements_of_learner =  user_xapi_service.fetch_statements_for_user(email)
    
    current_date = datetime.now()
    start_of_week = current_date - timedelta(days=current_date.weekday())
    
    statements_filtered_by_week = [
        statement for statement in statements_of_learner
        if start_of_week.date() <= statement['timestamp'].date() <= (start_of_week + timedelta(days=6)).date()
    ]
    
    active_hours = [{"day": (start_of_week + timedelta(days=i)).strftime('%A'), "hours": [{"hour": h, "timeSpent": 0} for h in range(24)]} for i in range(7)]
    
    durations = get_start_end_times_of_activities(statements_filtered_by_week)
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
    """
    Count the occurrences of each verb for all activities performed by a specific learner.
    This function fetches xAPI statements, filters them by the learner's email, and then counts the occurrences of each verb for all activities the learner has engaged in. The results are returned as a JSON response.
    Args:
        request (HttpRequest): The HTTP request object containing the learner's email.
    Returns:
        JsonResponse: A JSON response containing a dictionary where keys are activity IDs and values are dictionaries of verb counts for each activity.
    """
    
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
    """
    Fetches xAPI statements and extracts parent activities for each child activity.
    This function retrieves xAPI statements using the `xapi_service.fetch_statements()` method,
    processes each statement to identify parent activities, and constructs a dictionary mapping
    each child activity to its parent activities. The result is returned as a JSON response.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        JsonResponse: A JSON response containing a dictionary with child activity IDs as keys
                      and lists of parent activity IDs as values. If an error occurs, a JSON
                      response with an error message and a 500 status code is returned.
    """
    
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
    """
    Fetches xAPI statements and extracts the parent activities from each statement.
    Then, it maps each parent activity to its corresponding parent of parents.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        JsonResponse: A JSON response containing a dictionary with parent activities
                      mapped to their respective parent of parents. If an error occurs,
                      a JSON response with the error message and a 500 status code is returned.
    Raises:
        Exception: If an error occurs during the processing of xAPI statements.
    """
    
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
    """
    Calculate the initialization streak for a learner based on their xAPI statements.
    This function fetches the xAPI statements for a user identified by their email,
    filters the statements to include only those with the verb "initialized" and 
    timestamps before today, sorts them by timestamp, and calculates the streak of 
    consecutive days the learner has initialized.
    Args:
        request (HttpRequest): The HTTP request object containing the user's email.
    Returns:
        JsonResponse: A JSON response containing the initialization streak and the 
                      last date of initialization.
    """
    
    email = request.email
    statements = user_xapi_service.fetch_statements_for_user(email)
    statements_filtered_by_verb1 = filter_statements_by_verb_id(statements, construct_verb_id("initialized"))
    today = datetime.now().date()
    statements_filtered_by_verb = [statement for statement in statements_filtered_by_verb1 if statement['timestamp'].date() < today]
    sorted_statements = sort_statements_by_timestamp(statements_filtered_by_verb)
    
    streak = 0
    last_date = None
    
    for statement in sorted_statements:
        current_date = statement['timestamp'].date()
        if last_date is None or current_date == last_date + timedelta(days=1):
            streak += 1
        else:
            streak = 1
        last_date = current_date
    
    responseJson = {"initializationStreak": streak, "lastDate": last_date}
    return JsonResponse(responseJson, safe=False)
@verify_learner_token_annotation
def get_time_spent_daily_for_last_week(request):
    """
    Calculate the time spent daily for the last week based on user activity statements.
    This function fetches user activity statements for the past week, calculates the time spent
    on activities each day, and returns the result as a JSON response.
    Args:
        request (HttpRequest): The HTTP request object containing the user's email.
    Returns:
        JsonResponse: A JSON response containing the time spent daily for the last week.
        The response has the following structure:
        {
            "timeSpentDaily": [
                {"day": "Monday", "minutes": 120},
                {"day": "Tuesday", "minutes": 90},
                ...
        }
    """
    
    email = request.email
    statements = user_xapi_service.fetch_statements_for_user(email)
    current_date = datetime.now().date()
    start_date = current_date - timedelta(days=6)
    
    time_spent_daily = [{"day": (start_date + timedelta(days=i)).strftime('%A'), "minutes": 0} for i in range(7)]
    
    statements_filtered_by_week = [
        statement for statement in statements
        if start_date <= statement['timestamp'].date() <= current_date
    ]
       
    durations = get_start_end_times_of_activities(statements_filtered_by_week)
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
    """
    Retrieve assigned and completed activities for a learner based on their email.
    This function fetches xAPI statements, filters them by the learner's email, and processes
    the statements to determine the progress of the learner in various subcourses. It calculates
    the total number of assessments, the number of completed assessments, and the progress
    percentage for each subcourse. The results are returned as a JSON response.
    Args:
        request (HttpRequest): The HTTP request object containing the learner's email.
    Returns:
        JsonResponse: A JSON response containing the summary of subcourses with their respective
                      progress, completed assessments, total assessments, and individual assessment statuses.
    """
    
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