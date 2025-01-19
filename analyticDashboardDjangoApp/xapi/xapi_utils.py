from datetime import datetime, timedelta



def filter_statements_by_verb_id(statements, verb_id):
    """
    Filters xAPI statements by a specific verb.
    
    :param statements: List of xAPI statements.
    :param verb_id: The verb ID to filter by.
    :return: List of filtered xAPI statements.
    """
    filtered_statements = [statement for statement in statements if statement.get("verb", {}).get("id") == verb_id]
    return filtered_statements

def construct_verb_id(verb_name):
    """
    Constructs the ID of a verb by its name.
    
    :param verb_name: The name of the verb.
    :return: The ID of the verb.
    """
    
    return f"http://adlnet.gov/expapi/verbs/{verb_name}"

def filter_statements_by_course_id(statements, subcourse_id):
    """
    Filters xAPI statements by a specific subcourse ID.
    
    :param statements: List of xAPI statements.
    :param subcourse_id: The subcourse ID to filter by.
    :return: List of filtered xAPI statements.
    """
    filtered_statements = [statement for statement in statements if statement.get("context", {}).get("contextActivities", {}).get("parent", [{}])[0].get("id") == subcourse_id]
    return filtered_statements

def construct_activity_id(activity_name):
    """
    Constructs the ID of an activity by its name.
    
    :param activity_name: The name of the activity.
    :return: The ID of the activity.
    """
    return f"http://example.com/activities/{activity_name}"

def filter_statements_by_object_id(statements, object_id):
    """
    Filters xAPI statements by a specific object ID.
    
    :param statements: List of xAPI statements.
    :param object_id: The object ID to filter by.
    :return: List of filtered xAPI statements.
    """
    filtered_statements = [statement for statement in statements if statement.get("object", {}).get("id") == object_id]
    return filtered_statements

def filter_statements_by_instructor_email(statements, email):
    """
    Filters xAPI statements by a specific instructor's email.
    
    :param statements: List of xAPI statements.
    :param email: The email of the instructor to filter by.
    :return: List of filtered xAPI statements.
    """
    filtered_statements = [statement for statement in statements if statement.get("context", {}).get("instructor", {}).get("mbox") == f"mailto:{email}"]
    return filtered_statements

def get_statements_in_last_days(statements, days):
    """
    Filters xAPI statements by a specific time period in days.
    
    :param statements: List of xAPI statements.
    :param days: The number of days to filter by.
    :return: List of filtered xAPI statements.
    """
    filtered_statements = []
    current_time = datetime.utcnow()
    time_threshold = current_time - timedelta(days=days)

    for statement in statements:
        timestamp_str = statement.get("timestamp")
        if timestamp_str:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            if timestamp >= time_threshold:
                filtered_statements.append(statement)

    return filtered_statements

        
def get_statements_with_specific_hour(statements, hour):
    """
    Filters xAPI statements that have a specific hour in their timestamp.
    
    :param statements: List of xAPI statements.
    :param hour: The specific hour to filter by (0-23).
    :return: List of filtered xAPI statements.
    """
    hour = hour % 24
    
    filtered_statements = []

    for statement in statements:
        timestamp_str = statement.get("timestamp")
        if timestamp_str:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            if timestamp.hour == hour:
                filtered_statements.append(statement)

    return filtered_statements

def get_statements_of_specfic_user_by_email(statements, email):
    """
    Filters xAPI statements by a specific user's email.
    
    :param statements: List of xAPI statements.
    :param email: The email of the user to filter by.
    :return: List of filtered xAPI statements.
    """
    filtered_statements = [statement for statement in statements if statement.get("actor", {}).get("mbox") == f"mailto:{email}"]
    return filtered_statements


def sort_statements_by_timestamp(statements):
    """
    Sorts xAPI statements by their timestamp in ascending order.
    
    :param statements: List of xAPI statements.
    :return: List of sorted xAPI statements.
    """
    sorted_statements = sorted(statements, key=lambda x: x.get("timestamp", ""))
    return sorted_statements

def get_durations_of_tests_for_user(statements):
    """
    Extracts the durations of tests for a user from xAPI statements.
    
    :param statements: List of xAPI statements.
    :return: List of durations of the tests for the user.
    """
    durations = []
    test_start = None
    
    sorted_statements=sort_statements_by_timestamp(statements)

    for statement in sorted_statements:
        object_id = statement.get("object", {}).get("id")
        verb_id = statement.get("verb", {}).get("id")
        if verb_id == construct_verb_id("scored"):
            test_start = datetime.strptime(statement.get("timestamp"), "%Y-%m-%dT%H:%M:%S.%fZ")
        elif verb_id in [construct_verb_id("failed"), construct_verb_id("completed")]:
            if test_start:
                test_end = datetime.strptime(statement.get("timestamp"), "%Y-%m-%dT%H:%M:%S.%fZ")
                duration = test_end - test_start
                durations.append({
                    "score": statement.get("result", {}).get("score", {}).get("raw"),
                    "duration": duration,
                    "result": "failed" if verb_id == construct_verb_id("failed") else "completed",
                    "object_id": object_id,
                    "timestamp": statement.get("timestamp")
                })
                test_start = None  # Reset for the next test

    return durations

def get_duration_of_activities(statements):
    """
    Extracts the durations of tests for a user from xAPI statements.
    
    :param statements: List of xAPI statements.
    :return: List of durations of the tests for the user.
    """
    durations = []
    test_start = None
    sorted_statements=sort_statements_by_timestamp(statements)
    for statement in sorted_statements:
        verb_id = statement.get("verb", {}).get("id")
        activity_id = statement.get("object", {}).get("id")
        if verb_id == construct_verb_id("initialized"):
            test_start = datetime.strptime(statement.get("timestamp"), "%Y-%m-%dT%H:%M:%S.%fZ")
        elif verb_id in [construct_verb_id("exited")]:
            if test_start:
                test_end = datetime.strptime(statement.get("timestamp"), "%Y-%m-%dT%H:%M:%S.%fZ")
                duration = test_end - test_start
                durations.append({
                    "activityId": activity_id,
                    "duration": duration,
                    "test_start": test_start,
                    "test_end": test_end,
                })
                test_start = None  # Reset for the next test

    return durations
    
def get_all_user_names(statements):
 unique_users = set()
 for statement in statements:
        unique_users.add(statement['actor']['name'])
 return list(unique_users)   

def get_all_verbs_ids_used(statements):
    """
    Extracts all unique verbs used in xAPI statements.
    
    :param statements: List of xAPI statements.
    :return: Set of all unique verbs used.
    """
    verbs = set()
    
    for statement in statements:
        verb_id = statement.get("verb", {}).get("id")
        if verb_id:
            verbs.add(verb_id)
    
    return list(verbs)

def get_all_objects_ids_used(statements):
    """
    Extracts all unique objects used in xAPI statements.
    
    :param statements: List of xAPI statements.
    :return: Set of all unique objects used.
    """
    objects = set()
    
    for statement in statements:
        object_id = statement.get("object", {}).get("id")
        if object_id:
            objects.add(object_id)
    
    return list(objects)

def get_all_actors_emails_used(statements):
    """
    Extracts all unique actors' emails used in xAPI statements.
    
    :param statements: List of xAPI statements.
    :return: Set of all unique actors' emails used.
    """
    emails = set()
    
    for statement in statements:
        mbox = statement.get("actor", {}).get("mbox")
        if mbox:
            email = mbox.replace("mailto:", "")
            emails.add(email)
    
    return list(emails)
    
def get_all_courses(statements):
    """
    Extracts all unique courses used in xAPI statements.
    
    :param statements: List of xAPI statements.
    :return: Set of all unique courses used.
    """
    courses = set()
    
    for statement in statements:
        course_id = statement.get("context", {}).get("contextActivities", {}).get("parent", [{}])[0].get("id")
        if course_id:
            courses.add(course_id)
    
    return list(courses)

def get_open_activities(statements):
    """
    Extracts all open activities from xAPI statements that are initialized but have no scored event.
    
    :param statements: List of xAPI statements.
    :return: List of open activities.
    """
    open_activities = []
    open_activity_ids = set()
    scored_activity_ids = set()
    
    for statement in statements:
        verb_id = statement.get("verb", {}).get("id")
        activity_id = statement.get("object", {}).get("id")
        
        if verb_id == construct_verb_id("initialized"):
            if activity_id not in scored_activity_ids:
                open_activity_ids.add(activity_id)
        elif verb_id == construct_verb_id("scored"):
            if activity_id in open_activity_ids:
                open_activity_ids.remove(activity_id)
            scored_activity_ids.add(activity_id)
    
    open_activities = list(open_activity_ids)
    return open_activities