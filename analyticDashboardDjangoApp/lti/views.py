from django.shortcuts import render
from lti_provider.views import get_tool_conf, get_launch_data_storage, ExtendedDjangoMessageLaunch, DjangoOIDCLogin, get_launch_url
from lti_provider.views import LTILandingPage
from django.views.decorators.http import require_POST
from django.conf import settings
import pprint
from django.views.decorators.csrf import csrf_exempt
import jwt
from datetime import datetime, timedelta

@csrf_exempt  # Allow CSRF exemption for LTI launch
@require_POST
def launch(request):
    # Get LTI configuration and message launch objects
    landing_url_template = settings.LTI_TOOL_CONFIGURATION['landing_url']
    tool_conf = get_tool_conf()
    launch_data_storage = get_launch_data_storage()
    message_launch = ExtendedDjangoMessageLaunch(
        request, tool_conf, launch_data_storage=launch_data_storage)
    message_launch_data = message_launch.get_launch_data()

    # Extract course context and build the landing URL
    domain = request.get_host()
    try:
        course_context = message_launch_data.get('https://purl.imsglobal.org/spec/lti/claim/context', {}).get('id', 'unknown_course')
        landing_url = landing_url_template.format(request.scheme, domain, course_context)
    except KeyError:
        landing_url = landing_url_template.format(request.scheme, domain, 'unknown_course')

    # Determine user roles and privileges
    is_auth_ta = None
    roles = message_launch_data.get('https://purl.imsglobal.org/spec/lti/claim/roles', [])
    if settings.LTI_TOOL_CONFIGURATION.get('allow_ta_access', False):
        is_auth_ta = any('teachingassistant' in role.lower() for role in roles)
    
    pprint.pprint(message_launch_data)

    # Get user information
    user_name = message_launch_data.get('given_name', '') + ' ' + message_launch_data.get('family_name', '')
    user_email = message_launch_data.get('email', 'Unknown Email')
    if not user_name.strip():
        user_name = message_launch_data.get('name', 'Unknown User')

    # Generate access and refresh tokens for the frontend
    access_payload = {
        "sub": message_launch_data.get('sub'),  # User ID
        "roles": roles,
        "context_id": course_context,
        "exp": datetime.utcnow() + timedelta(hours=1),  # Access token expires in 1 hour
        "name": user_name,
        "email": user_email,
    }
    refresh_payload = {
        "sub": message_launch_data.get('sub'),  # User ID
        "exp": datetime.utcnow() + timedelta(days=30),  # Refresh token expires in 30 days
    }
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')

    # Debugging: Log launch data for troubleshooting
    print("Launch Data:", message_launch_data)
    print("Roles:", roles)
    print("landing_url:", landing_url)

    # Render the landing page template with context data
    return render(request, 'lti_provider/landing_page.html', {
        'landing_url': landing_url,
        'page_title': settings.LTI_TOOL_CONFIGURATION.get('title', 'Default Title'),
        'is_deep_link_launch': message_launch.is_deep_link_launch(),
        'launch_data': message_launch_data,
        'launch_id': message_launch.get_launch_id(),
        'curr_user_name': user_name,
        'curr_user_email': user_email,
        'is_instructor': 'http://purl.imsglobal.org/vocab/lis/v2/institution/person#Instructor' in roles,
        'is_administrator': 'http://purl.imsglobal.org/vocab/lis/v2/institution/person#Administrator' in roles,
        'is_auth_ta': is_auth_ta,
        'access_token': access_token,  # Pass the generated access token to the frontend
        'refresh_token': refresh_token,  # Pass the generated refresh token to the frontend
    })

def login(request):
    tool_conf = get_tool_conf()
    launch_data_storage = get_launch_data_storage()
    oidc_login = DjangoOIDCLogin(
        request, tool_conf, launch_data_storage=launch_data_storage)
    target_link_uri = get_launch_url(request) 
    
    return oidc_login\
        .enable_check_cookies()\
        .redirect(target_link_uri)