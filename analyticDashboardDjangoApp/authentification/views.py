from datetime import datetime, timedelta
import json
import jwt
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.conf import settings
from functools import wraps

list_of_admin_ids = [
'http://purl.imsglobal.org/vocab/lis/v2/institution/person#Administrator',
'http://purl.imsglobal.org/vocab/lis/v2/membership#Administrator',
'http://purl.imsglobal.org/vocab/lis/v2/system/person#Administrator',
'http://purl.imsglobal.org/vocab/lis/v2/system/person#AccountAdmin']

list_of_instructor_ids = [
'http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor',
'http://purl.imsglobal.org/vocab/lis/v2/institution/person#Instructor',
     
]

list_of_learner_ids = [
    'http://purl.imsglobal.org/vocab/lis/v2/membership#Learner',
    'http://purl.imsglobal.org/vocab/lis/v2/institution/person#Learner'
]


@require_POST
def refresh_token_view(request):
    """
    Endpoint to refresh the access token using a valid refresh token.
    """
    try:
        # Parse the refresh token from the request body
        refresh_token = request.POST.get('refresh_token') or json.loads(request.body.decode('utf-8')).get('refresh_token')
        print("Received refresh token:", refresh_token)
        decoded_refresh_token = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])

        # Verify the token is not expired
        if datetime.utcnow() > datetime.fromtimestamp(decoded_refresh_token['exp']):
            return JsonResponse({'error': 'Refresh token expired'}, status=401)

        # Generate a new access token
        access_payload = {
            "sub": decoded_refresh_token['sub'],
            "exp": datetime.utcnow() + timedelta(hours=1),  # Access token expires in 1 hour
        }
        new_access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')

        return JsonResponse({
            'access_token': new_access_token
        })
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Refresh token expired'}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({'error': 'Invalid refresh token'}, status=401)


def verify_learner_token_annotation(view_func):
    """
    Decorator to verify if a token is valid before allowing access to the view.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization', '').split('Bearer ')[-1]
        try:
            token = token.replace(" ", "")
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # Check if token is expired
            if datetime.utcnow() > datetime.fromtimestamp(decoded_token['exp']):
                return JsonResponse({'error': 'Token expired'}, status=401)
        
            roles = decoded_token.get('roles', [])
            if not any(role in list_of_learner_ids for role in roles):
                return JsonResponse({'error': 'Instructor privileges required'}, status=403)
            request.user = decoded_token  # Attach the token data to the request
            request.email = decoded_token.get('email')  # Attach the email to the request
            return view_func(request, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)

    return _wrapped_view

def verify_admin_token_annotation(view_func):
    """
    Decorator to verify if an admin token is valid before allowing access to the view.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization', '').split('Bearer ')[-1]
        token = token.replace(" ", "")
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # Check if token is expired
            if datetime.utcnow() > datetime.fromtimestamp(decoded_token['exp']):
                return JsonResponse({'error': 'Token expired'}, status=401)
            # Check if the user is an admin
            roles = decoded_token.get('roles', [])
            if not any(role in list_of_admin_ids for role in roles):
                return JsonResponse({'error': 'Admin privileges required'}, status=403)
            request.user = decoded_token  # Attach the token data to the request
            request.email = decoded_token.get('email')  # Attach the email to the request
            return view_func(request, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)

    return _wrapped_view


def verify_instructor_or_admin_token_annotation(view_func):
    """
    Decorator to verify if an instructor or admin token is valid before allowing access to the view.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization', '').split('Bearer ')[-1]
        token = token.replace(" ", "")
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # Check if token is expired
            if datetime.utcnow() > datetime.fromtimestamp(decoded_token['exp']):
                return JsonResponse({'error': 'Token expired'}, status=401)
            # Check if the user is an instructor or admin
            roles = decoded_token.get('roles', [])
            if not any(role in list_of_instructor_ids + list_of_admin_ids for role in roles):
                return JsonResponse({'error': 'Instructor or Admin privileges required'}, status=403)
            request.user = decoded_token  # Attach the token data to the request
            request.email = decoded_token.get('email')  # Attach the email to the request
            return view_func(request, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)

    return _wrapped_view
def verify_instructor_token_annotation(view_func):
    """
    Decorator to verify if an instructor token is valid before allowing access to the view.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization', '').split('Bearer ')[-1]
        token.replace(" ", "")
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # Check if token is expired
            if datetime.utcnow() > datetime.fromtimestamp(decoded_token['exp']):
                return JsonResponse({'error': 'Token expired'}, status=401)
            # Check if the user is an instructor
            roles = decoded_token.get('roles', [])
            if not any(role in list_of_instructor_ids for role in roles):
                return JsonResponse({'error': 'Instructor privileges required'}, status=403)
            request.user = decoded_token  # Attach the token data to the request
            request.email = decoded_token.get('email')  # Attach the email to the request
            print(request.email)
            return view_func(request, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)

    return _wrapped_view  