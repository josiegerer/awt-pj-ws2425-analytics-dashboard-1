
from datetime import datetime, timedelta, timezone
import json
from django.http import JsonResponse
from authentification.views import verify_admin_token_annotation, verify_instructor_token_annotation, verify_learner_token_annotation
from xapi.lrs_utils import get_xapi_statements

@verify_admin_token_annotation
def get_all_statements(request):
    try:
        params = {}
        if 'limit' in request.GET:
            params['limit'] = request.GET['limit']
        
        if 'from' in request.GET:
            params['from'] = request.GET['from']
            
        statements = get_xapi_statements(params)
        
        if 'more' in statements:
            statements['paginationParams'] = statements['more'].replace('/xapi/statements', '')
        del statements['more']
        
        return JsonResponse(statements, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)

@verify_admin_token_annotation       
def get_statements_of_last_days_by_timestamp(request,**kwargs):
    try:
        params = {}
        if 'limit' in request.GET:
            params['limit'] = request.GET['limit']
        
        if 'from' in request.GET:
            params['from'] = request.GET['from']
            
        last_days = int(kwargs.get('lastdays', 30))  # Default to 30 days if not provided
        statements_data = get_xapi_statements(query_params=params)
        statements = statements_data.get('statements')
        if not isinstance(statements, list):
            raise ValueError("Statements should be a list.")

        # Calculate the time range
        now = datetime.now(timezone.utc)
        since_time = now - timedelta(days=last_days)

        # Filter statements for the specified number of days
        print("Hallo")
        filtered_statements={'statements': []}
        for statement in statements:
            timestamp = statement.get('timestamp')
            if not timestamp:
                raise ValueError("Missing 'timestamp' in statement.")
            
            try:
                statement_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                print(statement_time)
                if statement_time > since_time:
                    filtered_statements['statements'].append(statement)
            except ValueError:
                raise ValueError(f"Invalid timestamp format: {timestamp}")
        print("Hallo")    
        if 'more' in statements:
            filtered_statements['paginationParams'] = statements['more'].replace('/xapi/statements', '')
            
        
        print(filtered_statements)
        
        return JsonResponse(filtered_statements, safe=False)

    except ValueError as ve:
        return JsonResponse({"error": f"ValueError: {str(ve)}"}, status=400)
    except KeyError as ke:
        return JsonResponse({"error": f"KeyError: {str(ke)}"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)

@verify_admin_token_annotation
def get_all_objects_of_attribute(request, **kwargs):
    try:
        params = {}
        if 'limit' in request.GET:
            params['limit'] = request.GET['limit']
        
        if 'from' in request.GET:
            params['from'] = request.GET['from']
            
        attribute = str(kwargs.get('attribute', 'actor'))  # Default to 'actor' if not provided
        # Fetch xAPI statements
        statements_data = get_xapi_statements()
        statements = statements_data.get('statements')

        # Validate the statements
        if not isinstance(statements, list):
            return JsonResponse({"error": "Invalid data format: 'statements' must be a list."}, status=400)

        # Extract objects from statements
        objects = { 'statements': [] }
        seen_objects = []

        for statement in statements:
            obj = statement.get(attribute)
            if obj is None:
                return JsonResponse({"error": f"Invalid statement: missing '{attribute}' key."}, status=400)

            if obj not in seen_objects:
                seen_objects.append(obj)
                objects["statements"].append(obj)
        if 'more' in statements:
            objects['paginationParams'] = statements['more'].replace('/xapi/statements', '')
      
        return JsonResponse(objects, safe=False)

    except ValueError as ve:
        return JsonResponse({"error": f"ValueError: {str(ve)}"}, status=400)
    except KeyError as ke:
        return JsonResponse({"error": f"KeyError: {str(ke)}"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)


@verify_learner_token_annotation
def get_all_statement_for_learner(request):
    try:
        
        actor = {"mbox":"mailto:"+email}
        params = {"agent": json.dumps(actor)}
        
        if 'limit' in request.GET:
            params['limit'] = request.GET['limit']
        
        if 'from' in request.GET:
            params['from'] = request.GET['from']
            
        email= request.email
        print(email)
        
        statements = get_xapi_statements(params)
        if 'more' in statements:
            statements['paginationParams'] = statements['more'].replace('/xapi/statements', '')
        del statements['more']
        return JsonResponse(statements, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)

@verify_instructor_token_annotation
def get_all_statements_for_instructor(request):
    try:
        params = {}
        print("Hallo")
        if 'limit' in request.GET:
            params['limit'] = request.GET['limit']
        
        if 'from' in request.GET:
            params['from'] = request.GET['from']
     
        statements = get_xapi_statements()
        print("Test")
        filtered_statements = []
        email= request.email
        print(email)
        for statement in statements.get('statements', []):
            context = statement.get('context', {})
            instructor = context.get('instructor', {})
            if instructor.get('mbox') == 'mailto:'+email:
               filtered_statements.append(statement)
        statements['statements'] = filtered_statements
        
        
   
        if 'more' in statements:
            statements['paginationParams'] = statements['more'].replace('/xapi/statements', '')
        del statements['more']

        return JsonResponse(statements, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)